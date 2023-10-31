# coding: utf-8

from __future__ import annotations

import glob
import sys
import os
import io
import argparse
import subprocess
from datetime import datetime as DateTime
from inspect import stack, getframeinfo
from textwrap import dedent
from ruamel.std.pathlib import Path
import ruamel.yaml
from ruamel.yaml.split import YamlDocStreamSplitter, split

from typing import Any, Union, Optional, List, Tuple


Bugs = """\
- check empty documents. E.g. !python that only has code in !pre, and !stdout
  without any introductory text
"""

ToDo = """\
- some mechanism to show the name, leave option for 'skipping'/'converting'
  comment and push out newline later. Test incombination with verbosity
- specify Python interpreter, or create virtualenv + package installs, in a better
  way than using RYD_PYTHON env var.
- formalize temporary directory
- store (prefixed) program, only execute when !stdout is requested.
- parse messages like:
  README.rst:72: (ERROR/3) Inconsistent literal block quoting.
  and show output context
- zoom in on errors that have no line number: `some name <>`__
- document handling of :: in RST, and need for |+ in stdraw
- describe yaml comments after `|+ # `
- support code-block directive  http://rst2pdf.ralsina.me/handbook.html#syntax-highlighting
- list structure of the .ryd file
- process documents using xyz:prog  matching the document tag xyz by rt piping through prog
- why do toplevel LiteralScalarString dumps have |2, it is not even correct!
= consider moving to plugin system
"""


class RydExecError(Exception):
    pass


class RydFile:
    def __init__(self, path, ryd_cmd, verbose=0):
        self._path = path
        self._out_name = None  # set by the convertor
        self._ryd_cmd = ryd_cmd
        self._yaml = self._ryd_cmd.yaml
        self._verbose = verbose
        self._doc_iterator = None
        self._docs_ok = True
        self._rt_ok = True

    def ordering(self):
        if not (res := self.frontmatter.get('order')):
            return None
        return [Path(x) for x in res]

    @property
    def frontmatter(self):
        try:
            return self._frontmatter
        except AttributeError:
            pass
        splitter = YamlDocStreamSplitter(self._path, verbose=self._verbose)
        it = self._doc_iterator = splitter.iter()
        _, cx, start_line = it.next(self._yaml)  # document metadata
        # potentially deal with old .ryd version and set convertor
        if 0.199 < float(cx['version']) < 0.201:
            if 'output' in cx:
                text = cx['output']
                print('should change "output: {text} in metadata to "text: {text}"')
            else:
                text = cx['text']
            if text == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor2 as Conv  # NOQA
            elif text == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor2 as Conv  # NOQA
            elif text == 'md':
                from ryd._convertor.markdown import MarkdownConvertor2 as Conv  # NOQA
        elif 0.099 < float(cx['version']) < 0.101:
            if cx['output'] == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor as Conv  # NOQA
            elif cx['output'] == 'md':
                from ryd._convertor.markdown import MarkdownConvertor as Conv  # NOQA
            elif cx['output'] == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor as Conv  # NOQA
            else:
                raise NotImplementedError
        assert Conv is not None
        self.convertor = Conv(self._ryd_cmd, self._yaml, cx, self._path)
        self._frontmatter = cx
        return cx

    def process(
        self, rt: bool = False, verbose: int = 0
    ):  # -> Union[Tuple[None, None], Tuple[dict[Any, Any], Path]]:
        convertor = self.convertor
        if not convertor.check():
            return False
        while not self._doc_iterator.done():
            y = self._doc_iterator.next()
            y, sln = y
            if not convertor.check_document(y, line=sln):
                self._docs_ok = False
                continue
            if not self._docs_ok:
                continue
            # print('yf', y)
            try:
                x = self._yaml.load(y)
            except Exception as e:
                raise
                if convertor.check_document(y, check_error=True, line=sln):
                    self._docs_ok = False
                else:
                    print(f'====== doc =====\n{y.decode("utf-8")}\n=======================')
                    print('exception', e)
                    raise  # no error_check succeeded
                self._docs_ok = False
            if rt:
                if not convertor.roundtrip(x, y):
                    rt_ok = False
                continue
            # print('x', repr(x))
            if not convertor(x):  # already up-to-date
                sys.stdout.flush()
                # ToDo you cannot return here, the PDF might not be generated because
                # of some rst2pdf issue
                return False
        if not self._docs_ok:
            return False
        if convertor.updated:
            if verbose > 0:
                print('updated')
        return True

    def write(self, rt: bool = False, verbose: int = 0):
        if rt:
            if rt_ok:
                self.convertor.roundtrip_write(path, self._yaml, cx)
        else:
            self._out_name = self.convertor.write()
        return self._out_name

class RYD:
    """
    both processes commandline as well as potential "global" storage for converted files
    """
    def __init__(self, args: argparse.Namespace, config: Optional[Any] = None) -> None:
        self._args = args
        self._config = config
        self._name_printed = False
        self._current_path: Union[Path, None] = None
        self.data = {
            'toc': {},  # path to list of tuple (level, str)
        }
        self.set_environ()

    def set_environ(self):
        changes_path = Path('CHANGES')
        if not changes_path.exists():
            return
        # see _tag/changelog.py or ruamel.file.changes
        yaml = ruamel.yaml.YAML(typ='safe', pure=True)
        for k, v in yaml.load(changes_path).items():
            if k == 'NEXT':
                continue
            self.data['version'] = os.environ['VERSION'] = k[0]
            self.data['date'] = os.environ['DATE'] = str(k[1])
            break

    def convert_subcommand(self) -> None:
        # res will consist of a mapping of Path(.ryd) -> (mapping frontmatter, Path(.md/.rst))
        if not self._args.old:
            res = self.convert_all_ordered(self._args.file, verbose=self._args.verbose)
        else:
            res = self.convert_all(self._args.file, verbose=self._args.verbose)
        if self._args.generate_mkdocs_config:
            self.generate_mkdocs_config(res, path=Path(self._args.generate_mkdocs_config))

    def generate_mkdocs_config(self, res: dict[Any, Any], path: Path) -> bool:
        for v in res.values():
            if 'mkdocs' in v[0]:
                data =  v[0]['mkdocs']
                if 'site_name' not in data:
                    data['site_name'] = Path(os.getcwd()).stem
                self.yaml.dump(data, path)
                return True
        return False

    def convert_all_ordered(self, file_names: list[Any], verbose: int=0) -> dict[Any, Any]:
        # create a list of all the filenames, expanding directories and those containing '*'
        # at the place they are specified
        # if there is a single directory, change into that directory and expand

        # this can be used to track doulbe call of ryd in dv, if readme is not generated
        # with open('/var/tmp/ryd.log', 'a') as fp:
        #     print(f'{DateTime.now():%Y-%m-%d %H:%M:%S} ryd {file_names}', file=fp)
        ret_val = {}
        old_dir = None
        expanded_mapping = {}
        if len(file_names) == 1 and os.path.isdir(file_names[0]):
            old_dir = os.getcwd()
            os.chdir(file_names[0])
            for ryd_name in sorted(Path('.').glob('*.ryd')):
                expanded_mapping[ryd_name] = RydFile(ryd_name, ryd_cmd=self, verbose=verbose)
        elif len(file_names) == 1:
            ryd_name = Path(file_names[0])
            # if str(ryd_name.parent) != '.':
            #     old_dir = os.getcwd()
            #     os.chdir(ryd_name.parent)
            #     ryd_name = Path(ryd_name.name)
            expanded_mapping[ryd_name] = RydFile(ryd_name, ryd_cmd=self, verbose=verbose)
        else:
            raise NotImplementedError
        ordered = list(expanded_mapping.keys())
        for path, fm in expanded_mapping.items():
            found = None
            if (res := fm.ordering()):
                if found is not None:
                    raise NotImplementedError(f'multiple orderings: {found}, {path}')
                found = path
                ordered = res
            # print(fm._path, fm.frontmatter)
            ret_val[path] = (fm.frontmatter, None)
        unordered = [p for p in expanded_mapping if p not in ordered]
        # print(f'{ordered=}')
        # print(f'{unordered=}')
        docs_with_error = []
        for path in ordered + unordered:
            if not expanded_mapping[path].process(verbose=1):
                docs_with_error.append(path)
        # print(f'{self.data["toc"]=}')
        if docs_with_error:
            if self._args.verbose > 1:
                 print(f'{docs_with_error=}, not generating')
            return {}
        for path in ordered + unordered:
            outname = expanded_mapping[path].write()
            # print(f'{outname=}')
        if old_dir is not None:
            if file_names[0] == '_doc':
                for ryd_name, val in expanded_mapping.items():
                    print('ryd_name', ryd_name)
                    if ryd_name.name == 'README.ryd' and val._out_name is not None:
                        parent_dir_readme = Path(old_dir) / val._out_name
                        parent_dir_readme.unlink(missing_ok=True)
                        val._out_name.copy(parent_dir_readme)
            os.chdir(old_dir)
        # for k, v in ret_val.items():
        #    print(repr(k), v)
        return ret_val

    def convert_all(self, file_names: list[Any], verbose: int=0) -> dict[Any, Any]:
        ret_val = {}
        for file_name in file_names:
            self._name_printed = False
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    exp_path_name = Path(exp_file_name)
                    res = self.convert_one(exp_path_name, verbose=verbose)
                    ret_val[exp_path_name] = res
                continue
            path_name = Path(file_name)
            if path_name.is_dir():
                old_dir = os.getcwd()
                os.chdir(path_name)
                for ryd_name in Path('.').glob('*.ryd'):
                    res = self.convert_one(ryd_name, verbose=verbose)
                    ret_val[ryd_name] = res
                os.chdir(old_dir)
            else:
                res = self.convert_one(path_name, verbose=verbose)
                ret_val[path_name] = res
        for k, v in ret_val.items():
           print(repr(k), v)
        return ret_val

    def clean(self) -> None:
        for file_name in self._todo():
            self.convert_one(file_name, clean=True)

    def _todo(self) -> list[Path]:
        todo = []
        for file_name in self._args.file:
            self._name_printed = False
            if file_name[0] == '*':
                for exp_file_name in sorted(Path('.').glob(file_name)):
                    todo.append(exp_file_name)
                continue
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    todo.append(Path(exp_file_name))
                continue
            todo.append(Path(file_name))
        # print('todo', todo)
        return todo

    def name(self) -> None:
        """print name of file only once (either verbose or on error)"""
        # print('name', self._name_printed)
        if self._name_printed:
            return
        self._name_printed = True
        print(self._current_path)

    @property
    def yaml(self) -> ruamel.yaml.YAML:
        try:
            return self._yaml  # type: ignore
        except AttributeError:
            pass
        self._yaml = res = ruamel.yaml.YAML()
        return res

    def convert_one(
        self, path: Path, clean: bool = False, rt: bool = False, verbose: int = 0
    ) -> Union[Tuple[None, None], Tuple[dict[Any, Any], Path]]:
        sys.stdout.flush()
        if self._current_path is None and not path.exists():
            print('unknown command, or file:', path)
            sys.exit(1)
        self._current_path = path
        if verbose > 0:
            self.name()
        Conv: Any = None
        ys = YamlDocStreamSplitter(path, verbose=verbose)
        it = ys.iter()
        _, cx, sln = it.next(self.yaml)  # document metadata
        if 0.199 < float(cx['version']) < 0.201:
            if 'output' in cx:
                text = cx['output']
                print('should change "output: {text} in metadata to "text: {text}"')
            else:
                text = cx['text']
            if text == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor2 as Conv  # NOQA
            elif text == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor2 as Conv  # NOQA
            elif text == 'md':
                from ryd._convertor.markdown import MarkdownConvertor2 as Conv  # NOQA
        elif 0.099 < float(cx['version']) < 0.101:
            if cx['output'] == 'rst':
                from ryd._convertor.restructuredtext import RestructuredTextConvertor as Conv  # NOQA
            elif cx['output'] == 'md':
                from ryd._convertor.markdown import MarkdownConvertor as Conv  # NOQA
            elif cx['output'] == 'so':
                from ryd._convertor.stackoverflow import StackOverflowConvertor as Conv  # NOQA
            else:
                raise NotImplementedError
        assert Conv is not None
        convertor = Conv(self, self.yaml, cx, path)
        if clean:
            convertor.clean()
            return None, None
        if not convertor.check():
            return None, None
        docs_ok = True
        rt_ok = True
        while not it.done():
            y = it.next()
            # if y is None:
            #     break
            y, sln = y
            if not convertor.check_document(y, line=sln):
                docs_ok = False
                continue
            if not docs_ok:
                continue
            # print('yf', y)
            try:
                x = self.yaml.load(y)
            except Exception as e:
                raise
                if convertor.check_document(y, check_error=True, line=sln):
                    docs_ok = False
                else:
                    print(f'====== doc =====\n{y.decode("utf-8")}\n=======================')
                    print('exception', e)
                    raise  # no error_check succeeded
                docs_ok = False
            if rt:
                if not convertor.roundtrip(x, y):
                    rt_ok = False
                continue
            # print('x', repr(x))
            if not convertor(x):  # already up-to-date
                sys.stdout.flush()
                # ToDo you cannot return here, the PDF might not be generated because
                # of some rst2pdf issue
                return None, None
        if not docs_ok:
            return None, None
        if convertor.updated:
            if verbose > 0:
                print('updated')
        if rt:
            if rt_ok:
                convertor.roundtrip_write(path, self.yaml, cx)
            out_name = None
        else:
            out_name = convertor.write()
        return cx, out_name

    def from_rst(self) -> None:
        from .loadrst import LoadRST

        file_names = [Path(f) for f in self._args.file]
        if self._args.output and len(file_names) != 1:
            print('you can only have one argument if --output is set')
            return

        for file_name in file_names:
            ryd_name = Path(self._args.output) if self._args.output else file_name.with_suffix('.ryd')
            if ryd_name.exists() and not self._args.force:
                print('skipping', ryd_name)
                continue
            rst = LoadRST(file_name)
            rst.analyse_sections()
            print('writing', ryd_name)
            with ryd_name.open('w') as fp:
                fp.write(dedent("""\
                ---
                version: 0.2
                text: rst
                fix_inline_single_backquotes: true
                # post: pdf
                --- |
                """))  # NOQA
                fp.write(rst.update_sections())

    def roundtrip(self) -> None:
        for file_name in self._todo():
            self.convert_one(file_name, rt=True)

    def serve_subcommand(self) -> None:
        mkdocs_yaml = Path('.mkdocs.yaml')
        mkdocs_yaml_cleanup = False
        doc_path = Path('_doc')
        if doc_path.exists():
            res = self.convert_all_ordered([str(doc_path)], verbose=self._args.verbose)
            if not mkdocs_yaml.exists():
                mkdocs_yaml_cleanup = True
                if not self.generate_mkdocs_config(res, mkdocs_yaml):
                    print(f'did not generate {mkdocs_yaml}')
                    return
        cmd = ['mkdocs', 'serve', '-f', '.mkdocs.yaml', '--clean']
        if self._args.verbose > 0:
            cmd.append('-v')
        os.system(' '.join(cmd))
        if mkdocs_yaml_cleanup:
            mkdocs_yaml.unlink()

    def rst_md(self) -> None:
        todo = list(self._todo())
        print('todo', todo)
        for expanded_path in todo:
            self.rst_md_one(Path(expanded_path), verbose=self._args.verbose)

    def rst_md_one(
        self, path: Path, *, verbose: int = 0,
    ) -> None:
        sys.stdout.flush()
        # if self._current_path is None and not path.exists():
        #     print('unknown command, or file:', path)
        #     sys.exit(1)
        self._current_path = path  # needed for self.name()
        if verbose > 0:
            self.name()
        yaml = ruamel.yaml.YAML()
        print('file', path.name)
        out = path # .with_suffix('.ryd.new')
        buf = io.BytesIO()
        pandoc = ['pandoc', '--from', 'rst', '--to', 'markdown']
        meta = True
        for doc, data, line_nr in split(path, yaml=yaml):
            if meta:
                meta = False
                assert data['text'] == 'rst'
                data['text'] = 'md'
                data['pdf'] = False
                try:
                    del data['fix_inline_single_backquotes']
                except KeyError:
                    pass
                yaml.dump(data, buf)
                continue
            # print(doc.decode('utf-8'), line_nr)
            tag = getattr(data, '_yaml_tag', None)
            # print(tag, type(doc), type(data), line_nr)
            if isinstance(data, ruamel.yaml.scalarstring.LiteralScalarString) and tag is None:
                # this is an non-tagged document, thus rst
                # print(repr(doc[:200]), line_nr)
                # print(doc.decode('utf-8')[:200], line_nr)
                # print(str(data)[:200], line_nr)
                # print(type(str(data)))
                res = subprocess.run(pandoc, input=str(data), encoding='utf-8', capture_output=True)
                buf.write(b'--- |\n')
                md_out = self.md_rewrite(res.stdout)
                # print(md_out[:200])
                buf.write(md_out.encode('utf-8'))
            else:
                buf.write(doc)
        out.write_bytes(buf.getvalue())

    def md_rewrite(self, s: str) -> str:
        return s

        # SPECIAL = '#*=+^"'
        # lines = s.splitlines()
        # for idx, line in enumerate(lines):
        #     if len(line) > 2 and line[0] in SPECIAL and line[0] == line[1] and line[0] == line[2]:
        #         try:
        #             underline, rest = line.split(None, 1)
        #         except:
        #             underline, rest = line, ''
        #         print('line', repr(underline), repr(rest))
        #         if idx + 1 < len(lines):
        #             if rest and lines[idx+1].startswith(underline):
        #                 lines[idx] = f'# {rest}'
        #                 lines[idx+1] = ''
        #                 continue
        # return '\n'.join(lines) + '\n'


