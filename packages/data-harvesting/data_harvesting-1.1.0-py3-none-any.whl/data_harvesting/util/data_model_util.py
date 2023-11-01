# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
Utility around dealing with unhide data files on disk
"""
import json
import os
from pathlib import Path
from typing import Optional
from typing import Union

from rdflib import Graph
from SPARQLWrapper import DIGEST
from SPARQLWrapper import POST
from SPARQLWrapper import SPARQLWrapper

from data_harvesting.aggregator import Aggregator
from data_harvesting.data_model import derive_metadata
from data_harvesting.data_model import LinkedDataObject


def convert_json_unhide(
    filepath: Union[Path, str], metadata: Optional[dict] = None, overwrite: bool = True, infrmt='jsonld'
):
    """
    Convert the given jsonld file or all files in a given directory to an unhide data type with some metadata
    this is useful to convert already harvested data on disk without running new versions of the
    harvesters again.

    for now we expect jsonld files only.

    # TODO or better just expect a file list, instead of dir or single file...
    """
    if isinstance(filepath, str):
        src = Path(filepath)
    else:
        src = filepath

    if src.is_dir():
        src_files = list(src.glob(f'**/*.{infrmt}'))
    elif src.is_file():
        src_files = [src]
    else:
        msg = f'Source file path provided for converting to unhide data, does not exists or is not a file or dir: {src}'
        raise ValueError(msg)

    for src in src_files:
        with open(src, 'rb') as fileo:
            data = json.load(fileo)  # try except this
        if metadata is None:
            ldo = LinkedDataObject(original=data, derived=data)
        else:
            metadata2 = derive_metadata()
            metadata2.update(metadata)
            ldo = LinkedDataObject(original=data, derived=data, metadata=metadata2)
        # now same linked data Object under same path
        if overwrite:
            name = str(src.stem) + '.json'
            dest = src.parent / name
        else:
            name = str(src.stem) + '_unhide' + '.json'
            dest = src.parent / name

        ldo.serialize(destination=dest)


def apply_aggregator(filepath, config=None, overwrite=True):
    """Apply data uplifting to a given unhide file on disk with the current aggregator and its
    configuration. This is useful to migrate unhide data if the configuration changed or if the
    aggregator changed
    """
    if isinstance(filepath, str):
        src = Path(filepath)
    else:
        src = filepath

    if src.is_dir():
        src_files = list(src.glob('**/*.json'))
    elif src.is_file():
        src_files = [src]
    else:
        msg = f'Source file path provided for uplifting, does not exists or is not a file or dir: {src}'
        raise ValueError(msg)

    agg = Aggregator(config_path=config)
    for src in src_files:
        print(src)
        ldo = LinkedDataObject.from_filename(src)
        #ld = ld_from_filename(src)

        uplifted = agg.apply_to(ldo)

        if overwrite:
            dest = src
        else:
            name = str(src.stem) + '_uplifted' + '.json'
            dest = src.parent / name
        print(dest)
        uplifted.serialize(destination=dest)


def upload_data(
    unhide_data: LinkedDataObject,
    graph_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    username: Optional[str] = None,
    passwd: Optional[str] = None
):
    """Upload unhide data to the triple store"""

    # if connection details are None, try to extract them from the configuration
    # file or environement variables
    if graph_name is None:
        graph_name = os.environ.get('DEFAULT_GRAPH', None)

    if endpoint_url is None:
        endpoint_url = os.environ.get('SPARQL_ENDPOINT', None)

    # This is not save, do better
    if username is None:
        username = os.environ.get('DBA_USER', None)

    if passwd is None:
        passwd = os.environ.get('DBA_PASSWORD', None)

    if endpoint_url is None:
        raise ValueError(
            'The sparql endpoint has to be provided under endpoint_url, or set through the env as SPARQL_ENDPOINT.'
        )

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setHTTPAuth(DIGEST)
    if (username is not None) and passwd is not None:
        sparql.setCredentials(username, passwd)
    sparql.setMethod(POST)
    graph_dic = unhide_data.derived  # jsonld dict
    graph = Graph()
    graph.namespace_manager.bind('schema', 'http://schema.org/')  # this is an unhide specific line,
    # maybe make this an kwarg
    graph.parse(data=json.dumps(graph_dic), format='json-ld')
    triples = ''
    for sub, pre, obj in graph.triples((None, None, None)):  # pylint: disable=not-an-iterable
        triple = f'{sub.n3()} {pre.n3()} {obj.n3()} . '
        triples += triple
    query = 'INSERT IN GRAPH <%s> { %s }' % (graph_name, triples)
    sparql.setQuery(query)
    results = sparql.query()
    if results.response.getcode() == 200:
        print('Your database was successfully updated ... ()' + str(len(graph)) + ') triple(s) have been added.')


def upload_data_filepath(
    filepath: Union[Path, str],
    infrmt: str = 'json',
    graph_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    username: Optional[str] = None,
    passwd: Optional[str] = None
) -> None:
    """Upload a data from a given filepath, can be a file or a directory of
    """
    if isinstance(filepath, str):
        src = Path(filepath)
    else:
        src = filepath

    if src.is_dir():
        src_files = list(src.glob(f'**/*.{infrmt}'))
    elif src.is_file():
        src_files = [src]
    else:
        msg = f'Source file path provided for uploading does not exists or is not a file or dir: {src}'
        raise ValueError(msg)

    for src in src_files:  # TODO Implement Bulk upload....
        unhide_data = LinkedDataObject.from_filename(src)
        upload_data(
            unhide_data=unhide_data, graph_name=graph_name, endpoint_url=endpoint_url, username=username, passwd=passwd
        )
