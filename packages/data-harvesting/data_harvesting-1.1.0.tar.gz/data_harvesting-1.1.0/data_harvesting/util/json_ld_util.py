# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""This module contains utility to process and handle, validate json-ld data """
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

from pyld import jsonld
from pyshacl import validate as shacl_validate
from rdflib import Graph
from rdflib.plugins.sparql.results.csvresults import CSVResultSerializer

from data_harvesting.util.url_util import hash_url
#from itertools import chain

# validating jsonlD is not so clear:
# there is framing https://www.w3.org/TR/json-ld-framing/ and for example in R this https://codemeta.github.io/codemetar/articles/validation-in-json-ld.html
# For rdf data there is shacl. where one can define shapes for validation, which are kind of
# schema graphs
# these might also be used to do some logic operation stuff like inference of new triples


def validate_jsonld_simple(jsonld_data: dict) -> bool:
    """
    Test if the integrety of the json-ld file is right,
    i.e we do not validate the content of an instance like the schema does

    Returns True if it validates
    returns False if not
    """

    context = jsonld_data.get('@context', None)
    if context is None:
        print('Missing context, so probably no or broken json-LD data given')
        return False

    instance = deepcopy(jsonld_data)
    # perform some roundturn json-LD operation to see if they work
    # TODO check if they are proper
    # Check if URIs are resolvable...
    instance = jsonld.expand(instance)
    instance = jsonld.compact(instance, context)

    # maybe also flatten the jsonLD to get all keys in general

    # check if we end with the same
    diffk: set = set(instance.keys()) - set(jsonld_data.keys())
    if len(diffk) != 0:
        print(f'The following keys are not supported: {diffk}')
        return False

    return True


def valdiate_from_file(filepath: Path, file_format='json-ld', options: Optional[dict] = None):
    """validate a given file"""
    data_graph = Graph()
    data_graph.parse(filepath, format=file_format)
    return validate(data_graph, options=options)


def validate(graph: Graph, validate_against: Optional[Graph] = None, options: Optional[dict] = None):
    """Validate a given rdf graph with shacl"""

    if validate_against is None:
        validate_against = Graph()
        # default is unhide specific
        # if not they should be downloaded, also they should be read once somewhere else and used from
        # there..
        # /data_harvesting/external_schemas/*
        basepath = Path(__file__).parent.parent.resolve() / 'external_schemas'
        schema_org = basepath / 'schemaorg-current-https.jsonld'
        codemeta = basepath / 'schema-codemeta.jsonld'
        if schema_org.exists():
            validate_against.parse(schema_org, format='json-ld')
        if codemeta.exists():
            validate_against.parse(codemeta, format='json-ld')
        # add other unhide specific things, ... or use only certain terms if class is given or so
    if options is None:
        options = {}
    vali = shacl_validate(graph, shacl_graph=validate_against, **options)
    conforms, results_graph, results_text = vali

    return conforms, vali


def convert(
    filepath: Path,
    destfilepath: Optional[Path] = None,
    informat: str = 'json-ld',
    outformat: str = 'ttl',
    overwrite: bool = False
) -> None:
    """
    convert a given graph file to a different format using rdflib
    """
    name = filepath.name.rstrip(filepath.suffix)
    destfilepath = destfilepath or Path(f'./{name}.{outformat}').resolve()

    if not overwrite and destfilepath.exists():
        return

    graph = Graph()
    graph.parse(filepath, format=informat)
    if outformat == 'csv':
        convert_to_csv(graph, destination=destfilepath)
    else:
        graph.serialize(destination=destfilepath, format=outformat)
    return


def convert_to_csv(graph: Graph, query: Optional[str] = None, destination: Union[Path, str] = 'converted.csv'):
    """Convert results of a sparql query of a given graph to to a csv file

    Default query results:
    link table. Source | link_type | Target
    """

    default_edge_query = """
    PREFIX schema: <http://schema.org/>
    SELECT DISTINCT ?Source ?Type ?Target
    WHERE {
      ?Source ?Type ?Target .
    }
    """
    # ?sType ?tType
    #  ?source a ?sType .
    #  ?target a ?tType .
    #  FILTER((?sType) IN (schema:Person, schema:Organization, schema:Dataset, schema:SoftwareSourceCode, schema:Document))
    #  FILTER((?tType) IN (schema:Person, schema:Organization, schema:Dataset, schema:SoftwareSourceCode, schema:Document))
    #}
    #"""

    query = query or default_edge_query
    results = graph.query(query)
    csv_s = CSVResultSerializer(results)
    with open(destination, 'wb') as fileo:
        csv_s.serialize(fileo)


def gen_id(data: dict) -> str:
    """
    generate an hash from piece of data, should just depend on the data
    """
    datarepr = json.dumps(data, sort_keys=True)
    hash_v = hashlib.md5(datarepr.encode('utf-8'))

    return hash_v.hexdigest()


# Add URIs and types, this is used for a custom skolemization of blank nodes.
def add_missing_uris(
    data: Union[List[dict], dict],
    path_prefix: str,
    main_id: Optional[str] = None,
    rek_count: int = 0,
    alternative_ids: Optional[List[str]] = None
) -> Union[List[dict], dict]:
    """
    Add for each for each entity an internal id corresponding to the given prefix
    and the internal jsonpath (since jsonpath is bad for urls we use the xpath syntax)

    if it has an @id then sameAs is added
    further rules, if there is a url contentUrl identifier or email present, this becomes the id
    instead and our custom id is put in sameAs

    prefix example: _https://helmholtz-metadaten.de/.well-known/genid/<main_id>/jsonfilepath/#hash

    without <main_id> one can easily generate id for the same data, but which is not the same, for
    example two persons with the same name, where just the name is given...

    """
    # To avoid mutable as default value, through this is not so nice...
    if alternative_ids is None:
        alternative_ids = ['identifier', 'contentUrl', 'url']

    # For now we do this rekursive, iterative might be safer
    id_path = path_prefix
    f_data = data.copy()

    def _add_missing_uris(
        new_data: dict, path_prefix: str = path_prefix, alternative_ids=alternative_ids, id_path=id_path
    ) -> dict:
        """
        Takes and Returns a dict always
        """
        same_as = new_data.get('sameAs', [])
        hash_v = gen_id(new_data)
        id_path = f'{id_path}/{hash_v}'
        if '@id' in new_data:
            if id_path not in same_as:
                same_as.append(id_path)
                new_data['sameAs'] = same_as
        else:
            found = False
            for term in alternative_ids:
                if term in new_data:
                    new_data['@id'] = new_data[term]
                    found = True
                    break  # Only use the first one, so there is an order we want to replace ids by others terms
            if not found:
                new_data['@id'] = id_path

        for key, val in new_data.items():
            if key == 'sameAs':
                continue
            id_path = path_prefix + f'/{key}'
            if isinstance(val, dict):
                new_data[key] = add_missing_uris(val, id_path, rek_count=rek_count + 1)  # rekursion
            elif isinstance(val, str):  # str is also list
                new_data[key] = val
            elif isinstance(val, list):
                new_entry: list = []
                for i, entry in enumerate(val):
                    if isinstance(entry, str):
                        new_entry.append(entry)
                    else:
                        prefix = path_prefix + f'/{key}_{i}'
                        new_entry.append(add_missing_uris(entry, prefix, rek_count=rek_count + 1))  # rekursion
                new_data[key] = new_entry
            else:
                new_data[key] = val
        return new_data

    # if several nodes are given we have a list else a dict
    if isinstance(f_data, list):
        list_new_data: List[dict] = []
        for item in f_data:
            # we extent the main id of the source in the prefix
            if rek_count == 0 and (main_id is None):
                main_id = item.get('@id', None)  # this is needed for some functions
            if main_id is not None:
                path_prefix = path_prefix + '/' + hash_url(main_id)[:13]
                # we hash the id, since these are potentially long PIDS
                main_id = None
            new_item = _add_missing_uris(item, path_prefix=path_prefix)
            list_new_data.append(new_item)
        f_data = list_new_data
    else:
        # we extent the main id of the source in the prefix
        if rek_count == 0 and (main_id is None):
            main_id = f_data.get('@id', None)  # this is needed for some functions
        if main_id is not None:
            path_prefix = path_prefix + '/' + hash_url(main_id)[:13]
            # we hash the id, since these are potentially long PIDS
            main_id = None
        f_data = _add_missing_uris(f_data, path_prefix=path_prefix)
    return f_data


# This is currently not used, it was succeeded by a sparql update
def add_missing_types(data: dict, type_map: Optional[List[dict]] = None) -> dict:
    """
    Add @types to data where it can be known for sure.
    TODO: There should be a general solution for this on the
    semantic/reasoner level, i.e schema.org allows for some reasoning, other rules could be stated by us

    like schema.org author, creator and contributor get type @Person or @organization
    the affiliation key is only allowed for a Person

    example type_map = [{'type': 'Person', 'keys': ['author', 'creator', 'contributor'], 'if_present' : 'affiliation'}]
    """

    if type_map is None:
        type_map = [{'type': 'Person', 'keys': ['author', 'creator', 'contributor'], 'if_present': 'affiliation'}]
    # If 'affiliation' present, type is a person
    new_data = data.copy()

    def add_type(data_d: Union[dict, list, str], mapping: dict) -> Union[dict, list, str]:
        """Add type"""
        if not isinstance(data_d, dict):
            return data_d
        if not '@type' in data_d.keys():
            condition = mapping.get('if_present', '')  # empty string is false
            if condition:
                if condition in data_d.keys():
                    data_d['@type'] = mapping.get('type')
        return data_d

    for key, val in new_data.items():  # Currently Only first level, maybe we have to do rekursion
        for mapping in type_map:
            if key in mapping.get('keys', []):
                if isinstance(val, list):
                    new_data[key] = [add_type(entry, mapping) for entry in val]
                elif isinstance(val, dict):
                    new_data[key] = add_type(val, mapping)
                else:
                    new_data[key] = val

    return new_data


# complete affiliations and organizations
# organizations with the same name should become the same id
# there should be a list of HGF orgas with ROARs.
# Also if a name of an org contains the name of a org with roar, this new org, should be created and
# linked to the org with the roar. like (Forschungszentrum Jülich GmbH, PGI-7)


def complete_affiliations(data: dict, roar_id_dict: dict, re3data_dict: dict, blank_node_identifier='_:N'):
    """
    Completes the given affiliation and organization where possible.

    roar_dict={ror_id1:{metadata}, ror_id2:{metadata}}
    the roar_id_dict is the inverse, of that. i.e: {'name': [roar_ids], 'grid_id': roar_id}

    for example:
    "affiliation": "Helmholtz-Zentrum Dresden-Rossendorf",
    - > "affiliation": {'@id': 'roar', '@type': organization 'name': "Helmholtz-Zentrum Dresden-Rossendorf"}

    more information about it should be somewhere else in the graph, we just want to link it to the right id

    example 2: (same for publisher, and includedInDataCatalog)
    "provider": {"@type": "Organization", "name": "J\u00fclich DATA"},
    ->  "provider": {"@type": "Organization", "name": "J\u00fclich DATA", '@id': 'http://doi.org/10.17616/R31NJMYC'},


    """
    raise NotImplementedError


def update_key(data: dict, key: Union[str, int], val_dict: dict, overwrite: bool = False):
    """
    Update the metadata of a certain key with a certain dict

    if the provider is already present, then we might want to complete the metadata, that it is linked correctly

    example:
    val = {
        "@id": " http://doi.org/10.17616/R31NJMYC",
        "@type": "Organization",
        "name": "J\u00fclich DATA"}

    """
    orgi = data.get(key, {})
    new = orgi
    if isinstance(orgi, list):
        for i, entry in enumerate(orgi):
            if isinstance(entry, dict):
                # todo
                pass
    if isinstance(orgi, dict):
        new = orgi
        if overwrite:
            new.update(val_dict)  # shallow merge for now
        else:
            for nkey, val in val_dict.items():
                if nkey not in orgi.keys():
                    new[nkey] = val
    data[key] = new
    return data
