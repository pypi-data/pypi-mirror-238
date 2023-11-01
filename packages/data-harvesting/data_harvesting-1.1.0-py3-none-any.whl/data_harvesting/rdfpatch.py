# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
Module containing the RDFPatch class, as well as some methods around it, which are useful to
generate and work with patches for rdf data.
"""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Annotated
from typing import Callable
from typing import cast
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic.functional_serializers import PlainSerializer
from pydantic.functional_validators import PlainValidator
from rdflib import Graph
from rdflib import Literal
from rdflib import URIRef
from rdflib.compare import graph_diff

from data_harvesting.util.pid_util import generate_uuid
#from pydantic.functional_validators import AfterValidator


def generate_patch(graph_key='graph') -> Callable:
    """
    Generate a rdf patch for a given function which inputs a graph and outputs a graph.
    This function is meant to be used as a decorator generator.

    In order to find the graphs the input graph has to be the first argument to the function func,
    or a kwarg with the key provided by graph_key, default 'graph'.
    Also to find the output graph it requires the return value or the first return value to be a graph


    returns function
    raises ValueError
    """
    def generate_patch_decorator(func, graph_key='graph'):
        """
        The actual decorator
        """
        def _generate_patch(*args, **kwargs):
            """
            returns the results of func plus a patch in front
            """
            # deepcopy because graph is parsed per reference, often this will lead then to
            # the output graph == input graph after function execution
            if graph_key in kwargs:
                graph = deepcopy(kwargs[graph_key])
            else:
                if len(args) > 0:
                    if isinstance(args[0], Graph):
                        graph = deepcopy(args[0])
                    else:
                        raise ValueError(
                            f'No input graph found! Has to be provided first argument, or a kwargs {graph_key}!'
                        )

            results = func(*args, **kwargs)

            out_graph = None
            if isinstance(results, Graph):
                out_graph = results
            elif isinstance(results, list):
                if len(results) > 0:
                    if isinstance(results[0], Graph):
                        out_graph = results[0]
            if out_graph is None:
                raise ValueError('No output graph found! Has to single return or first return!')

            in_both, in_first, in_second = graph_diff(graph, out_graph)

            # this might be error prone, try except or else?
            #serializable_args = (str(arg) for arg in args)
            #serializable_kwargs = {key: str(val) for key, val in kwargs.items()}
            metadata = {
                'function_module': func.__module__,
                'function_name': func.__name__,
                # It would be nice to store more metadata on the input, but currently I do not know how
                # to make sure that the patch stays serializable. i.e everything simple data types.
                # very often we have Graphs, which causes a problem wit pydantic
                #'function_args': serializable_args,
                #'function_kwargs': serializable_kwargs,
                'creation_time': datetime.now().isoformat(),
                'uuid': str(generate_uuid())
            }
            patch = generate_patch_from_graph(in_first, in_second, metadata=metadata)

            return patch, results

        return _generate_patch

    return generate_patch_decorator


def derive_patchmetadata() -> dict:
    """
    Derive metadata from the data and complete it

    # currently data is not needed
    """
    now = datetime.now().isoformat()
    metadata = {'created_at': now, 'last_modified_at': now, 'uuid': str(generate_uuid())}
    return metadata


# This is used as type hint to define a pydantic field for rdfgraphs:


def to_rdfgraph(obj: Union[Graph, str]) -> Graph:
    """Load an rdflib graph from a given ttl string"""
    if isinstance(obj, Graph):
        return obj

    graph = Graph()
    if obj.strip():
        graph.parse(data=obj)  # be more careful here, much can go wrong ;-)
    return graph


def from_rdfgraph(graph: Union[Graph, str]) -> str:
    """Serializer for an rdflib graph returns and serialized graph as a ttl string"""
    # not sure if the string is ever needed
    if isinstance(graph, Graph):
        ret = graph.serialize(format='ttl')
    else:
        ret = graph
    return cast(str, ret)


RdflibGraphType = Annotated[Graph,
                            PlainValidator(to_rdfgraph),
                            PlainSerializer(from_rdfgraph),
                            Field(default_factory=Graph)]


class RDFPatch(BaseModel):
    """
    This class represents a RDF patch

    Created, since one could not parse the Jena Patch format into a simple RDF graph and
    rdf-delta is in java (https://github.com/afs/rdf-delta).

    If there is a other common way already out there this should be used instead
    for example see: https://www.w3.org/TR/ldpatch/

    and https://github.com/pchampin/ld-patch-py (LGPL).
    There are other formats one could serialize a patch to. These do not overlap in power.
    Problems with the current implementation of this:
    - Merging of a stack of RDFPatches would not work properly by the current 'several graph' design,
    since the order of the transactions matters...

    """
    #names: list = ['addprefix', 'deleteprefix', 'add_triples', 'delete_triples']
    #addprefix: RdflibGraphType
    #deleteprefix: RdflibGraphType
    add_triples: RdflibGraphType
    delete_triples: RdflibGraphType
    metadata: dict = Field(default_factory=derive_patchmetadata)

    class ConfigDict:
        validate_assignment = True
        validate_default = True

    def serialize(self, destination: Path):
        """
        Serialize the file to a json document, while the graph data is stored in a specific format
        """
        total_json = self.model_dump_json()
        with open(destination, 'w', encoding='utf-8') as fileo:
            fileo.write(total_json)

    @classmethod
    def from_filename(cls, filename: Path):
        """Initialize/Load LinkedDataObject from filename"""
        if not filename.is_file():
            raise ValueError(f'Source file path provided: {filename} is not a file, or does not exist.')
        with open(filename, 'r', encoding='utf-8') as fileo:
            data = fileo.read()
        instance = cls.model_validate_json(data)
        return instance

    def to_json(self):
        """
        Returns a json object representation of the patch
        """
        return self.model_dump()


def parse_string_triple(triple_string: list) -> tuple:
    """
    Convert <http://example/SubClass> <http://www.w3.org/2000/01/rdf-schema#label> "SubClass"
    to URIRef("http://example/SubClass"),  rdf.label, Literal("SubClass")
    :param triple_string: [description]
    :type triple_string: str
    :return: [description]
    :rtype: rdflib.triple
    """
    def _get_type(string):
        """
        """
        if not isinstance(string):
            return string
        if string.startswith('<'):
            # URIRef or namespace
            transform = URIRef(string)
            #transform =
        else:
            transform = Literal(string)
        return transform

    triple = tuple(_get_type(entry) for entry in triple_string)
    print(triple)
    return triple


# What about patch sequences? then the current class is not sufficient. since graph, can not captures
# order


def generate_patch_from_graph(in_first: Graph, in_second: Graph, metadata=None) -> RDFPatch:
    """
    Generate a rdf patch for a given graph difference

    :param in_first: a graph, set of triples containing triples only in the first/input graph
        from a diff, i.e. these were deleted
    :type in_first: Graph
    :param in_first: a graph, set of triples containing triples only in the second/output graph
        from a diff, i.e. these were added
    :type in_first: Graph

    old patch_format: Format in which the patch shall be returned, default 'jena'
        see: https://jena.apache.org/documentation/rdf-patch/, or
        https://github.com/afs/rdf-delta
    now property of RDFpatch, as serialization option

    """
    patch_id = generate_uuid()  # maybe hash the changes instead?
    if metadata is None:  # because pydantic sets the default of it if not there
        pat = RDFPatch(add_triples=in_second, delete_triples=in_first)
    else:
        pat = RDFPatch(metadata=metadata, add_triples=in_second, delete_triples=in_first)

    # TODO: maybe return None if the patch is empty?
    return pat


def apply_patch(graph: Graph, patch: RDFPatch) -> Graph:
    """
    Apply a given patch to a graph
    Since a patch is written a specific backend triple store like jena, this provides a way to apply
    the patch through python to a given graph outside of the backened
    """
    # todo implement PA
    #EX = Namesspace('')
    #o_graph.bind()
    o_graph = graph + patch.add_triples - patch.delete_triples
    return o_graph


def revert_patch(graph: Graph, patch: RDFPatch) -> Graph:
    """
    Apply a given patch to a graph
    Since a patch is written a specific backend triple store like jena, this provides a way to apply
    the patch through python to a given graph outside of the backened
    """
    # todo implement PA
    o_graph = graph - patch.add_triples + patch.delete_triples
    return o_graph
