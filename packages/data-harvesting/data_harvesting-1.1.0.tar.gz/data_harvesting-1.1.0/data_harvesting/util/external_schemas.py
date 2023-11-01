# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
Utility to download, load and process external schemas needed for example validation
"""
from pathlib import Path

import requests
from rdflib import Graph

EXTERNAL_SCHEMAS_FOLDER = Path(__file__).resolve().parent.parent / 'external_schema'
KNOWN_SCHEMAS = {
    'schema_org': 'https://schema.org/version/latest/schemaorg-current-https.jsonld',
    'schema_org_shacl': 'https://datashapes.org/schema.jsonld',
    'codemeta': 'https://doi.org/10.5063/schema/codemeta-2.0'
}


def load_external_schema(schema_name: str = 'schema_org_shacl') -> Graph:
    """
    Read a schema from file if it is there, otherwise download it and cache
    """

    if schema_name not in KNOWN_SCHEMAS:
        raise ValueError(f'Schema: {schema_name} not known. Could not be loaded.')

    schema_path = EXTERNAL_SCHEMAS_FOLDER / f'{schema_name}.jsonld'

    if not schema_path.exists():
        data = requests.get(KNOWN_SCHEMAS[schema_name], timeout=(10, 100)).text  #content
        with open(schema_path, 'w', encoding='utf-8') as fileo:
            fileo.write(data)

    schema = Graph().parse(schema_path)

    return schema
