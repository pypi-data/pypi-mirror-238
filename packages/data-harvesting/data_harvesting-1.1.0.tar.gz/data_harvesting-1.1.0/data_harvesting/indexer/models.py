# -*- coding: utf-8 -*-
"""This module contains the Att class"""
from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Union


@dataclass(order=True)
class Att:
    """Att class, basic to string mapping"""
    prefix: Optional[str]
    value: Optional[Union[List, str]]  #Any
    name: Optional[str] = None

    @property
    def key(self):
        return '_'.join([s for s in (self.prefix, self.name) if s])

    @property
    def as_dict(self):
        return {
            'prefix': self.prefix or '',
            'value': self.value,
            'name': self.name or '',
        }
