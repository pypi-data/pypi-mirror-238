# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
Module containing the Data model for linked data close to the unhide projects needs,
which wraps the original data stored metadata and provenance data
together with derived data for the actual graph.
"""
import json
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from typing import Annotated
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pyshacl import validate as shacl_validate
from rdflib import Graph

from data_harvesting.rdfpatch import RDFPatch
from data_harvesting.util.external_schemas import load_external_schema
from data_harvesting.util.pid_util import generate_uuid

SCHEMA_ORG_SHAPE = load_external_schema('schema_org_shacl')


def derive_metadata() -> dict:
    """
    Derive metadata from the data and complete it

    # currently data is not needed
    """
    now = datetime.now().isoformat()
    metadata = {
        'created_at': now,
        'last_modified_at': now,
        'uuid': str(generate_uuid()),
        'data_harvesting_version': version('data-harvesting')
    }
    return metadata


class LinkedDataObject(BaseModel):
    """
    Representation of a json-ld file with Original data, derived data, and metadata including provenance

    {
    metadata: {}
    original: {}
    derived: {}
    patch_stack: []
    }
    Each LinkedDataObject usually has a representative file on disk or data object in an object store
    The derived data will make it into the a combined graph (like the Unhide graph).

    # Comments:
    # Provenance might/should be tract somewhere externally, like through a workflow manager (AiiDA)
    # One might also use this or write a base class which can abstract from the actual storage,
    # like if it is stored on disk, or in an objectstore or some other database
    # Apply filter prior serialization, to allow for removal of certain internal data
    """
    metadata: Annotated[dict, Field(default_factory=derive_metadata)]
    original: Union[List[dict], dict]
    derived: Annotated[Union[List[dict], dict], Field(default_factory=lambda: [])]
    patch_stack: Annotated[List[RDFPatch], Field(default_factory=lambda: [])]

    class ConfigDict:
        validate_assignment = True
        validate_default = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.derived:
            if len(self.patch_stack) == 0:
                self.derived = self.original

    def serialize(self, destination: Path):
        """
        Serialize the file to a json document, while the graph data is stored in a specific format
        """
        total_json = self.model_dump()
        with open(destination, 'w', encoding='utf-8') as fileo:
            json.dump(total_json, fileo, indent=4, separators=(', ', ': '), sort_keys=True)
        #    fileo.write(total_json)

    @classmethod
    def from_filename(cls, filename: Path):
        """Initialize/Load LinkedDataObject from filename"""
        if not filename.is_file():
            raise ValueError(f'Source file path provided: {filename} is not a file, or does not exist.')
        with open(filename, 'r', encoding='utf-8') as fileo:
            data = fileo.read()
        instance = cls.model_validate_json(data)
        return instance

    @classmethod
    def from_dict(cls, data: dict):
        """Initialize/Load LinkedDataObject from a given dict"""
        instance = cls.model_validate(data)
        return instance

    def validate_rdf(self, shape_graph: Optional[Graph] = None, original_only: bool = False, verbose: bool = True):
        """
        Do a shacl validation on the original data and derived

        todo get the default shape graph
        =SCHEMA_ORG_SHAPE
        """
        shape_graph = shape_graph or SCHEMA_ORG_SHAPE
        orgi_graph = Graph()
        orgi_graph.parse(data=json.dumps(self.original), format='json-ld')
        val_org = shacl_validate(orgi_graph, shacl_graph=shape_graph)
        conforms, results_graph, results_text = val_org
        if verbose:
            print(results_text)
        if not original_only:
            de_graph = Graph()
            de_graph.parse(data=json.dumps(self.derived), format='json-ld')
            val = shacl_validate(de_graph, shacl_graph=shape_graph)
            conforms_de, results_graph, results_text = val
            conforms = conforms and conforms_de
        if verbose:
            print(results_text)

        return conforms


'''
def upload_to_database(data, database_endpoint: str):
    """
    Upload the derived data content to a given database
    """
    raise NotImplementedError


def upload_file_to_database(filepath, database_endpoint: str):
    """
    Upload the derived data content to a given database
    """
    raise NotImplementedError


def update_database(patch_stack, database_endpoint: str):
    """
    Apply the patch stack to a given database
    """
    raise NotImplementedError
'''
