# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
This module contains functions to change a graph in certain ways
"""
from pathlib import Path
from typing import List

from rdflib import Graph

from data_harvesting.rdfpatch import generate_patch


@generate_patch()
def apply_update(graph: Graph, sparql_update: str, **kwargs) -> Graph:
    """
    Apply a given sparql_update to a given graph

    we may not need this but use apply_update_stack per default
    """
    graph.update(sparql_update, **kwargs)
    return graph


@generate_patch()
def apply_update_stack(graph: Graph, sparql_stack: List[str], **kwargs) -> Graph:
    """
    Apply a given list of sparql_updates to a given graph
    """
    for update in sparql_stack:
        graph.update(update, **kwargs)  # no reuse of apply_update since we avoid the patches

    return graph


def get_update_from_file(filepath: Path):
    """
    Read a sparql update string from file
    """
    with open(filepath, 'r', encoding='utf-8') as fileo:
        update_string = fileo.read()
    return update_string


def update_from_template(template: str, replace: List[tuple]):
    """
    Format a given template string by replacing certain string with other values

    replace is a list of tuple with length two, where the first entry is what should be replaced in
    the second entry specifies with what
    """
    update_string = template
    for changes in replace:
        update_string.replace(changes[0], changes[1])

    return update_string
