# -*- coding: utf-8 -*-
"""This module contains common functions for the indexer"""
from collections.abc import Iterable


def flatten(lis):
    """Flat a given list"""
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for subitem in item:
                yield subitem
            continue
        yield item
