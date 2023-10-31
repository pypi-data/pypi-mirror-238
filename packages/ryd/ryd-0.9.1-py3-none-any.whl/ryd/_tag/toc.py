# coding: 'utf-8'

from __future__ import annotations

import os
from ryd._tag._handler import BaseHandler
import ruamel.yaml
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ryd._convertor._base import ConvertorBase
else:
    ConvertorBase = Any


class Toc(BaseHandler):
    def __init__(self, convertor: ConvertorBase) -> None:
        super().__init__(convertor)

    def __call__(self, d: Any) -> None:
        """
        insert an index
        mkdocs local expands this and buttons (default hidden) for 2nd level:
           <a class="reference internal" href="overview/">Overview</a>
        for readthedocs you need (within <ul>:
           <li><a href="https://yaml.readthedocs.io/en/latest/basicuse/">Basic Usage</a></li>
        """
        self.c.add_toc(self.c._ryd.data['toc'], data=d)
        return
