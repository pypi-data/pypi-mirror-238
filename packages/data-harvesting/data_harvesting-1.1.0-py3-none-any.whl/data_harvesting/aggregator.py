# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
Module containing the Aggregator class, which performs uplifting and data enrichments on
unhide data
"""
import importlib
import json
from datetime import datetime
from pathlib import Path

from rdflib import Graph

from data_harvesting import get_config
from data_harvesting import get_config_path
from data_harvesting.data_model import LinkedDataObject
from data_harvesting.util.sparql_util import apply_update
from data_harvesting.util.sparql_util import get_update_from_file

#from pprint import pprint
#from data_harvesting.rdfpatch import from_rdfgraph

#from pyld import jsonld


# We clearly separate aggregation function from the data object. Since data itself should not change
class Aggregator:
    """
    Class to aggregate LinkedDataObjects, or databases by predefined sparql updates within a given config file,
    and or in addition to given operations. All operations are the stack.

    The stack can have the form:
    [({metadata}, sparqlupdatestring), (function, {kwargs})]

    Comments:
    # Add prov-o terms to data.
    """

    # read from config file which operations to apply
    #
    def __init__(self, stack=None, config_path=get_config_path(), use_config: bool = True):
        """
        Initialize a Aggregator instance and read an update stack from a given config file
        """
        self.stack_config: list = []
        if stack is None:
            stack = []
        if use_config:
            self.set_config(config_path=config_path)

        full_stack = self.stack_config + stack
        self.stack = full_stack

    def set_config(self, config_path=get_config_path()):
        """
        Set sources and harvester specific config from a given config
        """
        full_config = get_config(config_path)

        # This is the harvester specific part in the config
        self.config = full_config.get(self.__class__.__name__, {})
        #print(self.config)
        self.stack_config = self.config.get('stack', [])

    def to_string(self):
        """
        Display the stack
        """
        return str(self.stack)

    def add_to_stack(self, item):
        """
        Add a task to the stack
        """
        self.stack += item

    def apply_to(self, data_object: LinkedDataObject):
        """
        Apply the given stack to the given data_object in line

        The changes are applied to the derived data and then the patch_stack is updated.

        """
        patch_stack = data_object.patch_stack
        derived = data_object.derived  # an Union(dict, list
        if isinstance(derived, dict):
            context = derived.get('@context', {})  # we assume here that the context does not change
        else:
            for entry in derived:
                context = entry.get('@context', None)
                if context:  # fornow just use the first one found...
                    break
        # an feature which changes prefixes needs to change also this.
        for i, item in enumerate(self.stack):
            # store prov on this small level or higher level, i.e on patch versus many
            patch = None
            if item['type'] == 'python':
                method_name = item['method'].split('.')[-1]
                module_path = item['method'].rstrip(f'.{method_name}')
                module = importlib.import_module(module_path)
                method = getattr(module, method_name)
                # TODO make this more robust, i.e the methods needs to have a patch decorator...
                # but for functions taking the dict, there is no graph input
                # TODO how to do patches for these?
                # be careful derived can now be a graph
                derived = method(data=derived, **item['kwargs'])
            elif item['type'] == 'sparql':
                basepath = Path(__file__).parent / 'data_enrichment'  #TODO get from config if set
                filepath = Path(basepath) / item['file']
                update = get_update_from_file(filepath)
                #print(update)
                #sparql functions always need a graph
                if not isinstance(derived, Graph):
                    derived = Graph().parse(data=json.dumps(derived), format='json-ld')
                patch, derived = apply_update(graph=derived, sparql_update=update)
                patch.metadata['sprarql_update_path'] = item['file']
                #patch.metadata['sparql_update'] = update
            else:
                raise ValueError(f'Aggregator command in stack not understood, unknown type in: {item}.')
            if patch is not None:  # TODO only add patch if the patch is not empty...
                if patch.add_triples or patch.delete_triples:
                    patch_stack.append(patch)

        data_object.patch_stack = patch_stack
        '''
        for pat in patch_stack:
            print('add:')
            pprint(from_rdfgraph(pat.add_triples))
            print('delete:')
            pprint(from_rdfgraph(pat.delete_triples))
            print('intersection:')
            pprint((pat.add_triples & pat.delete_triples))
        '''
        #data_object.set_derived(derived)
        if isinstance(derived, Graph):
            derived = json.loads(
                derived.serialize(format='json-ld', encoding='utf-8', context=context, sort_keys=False)
            )
            # this serialzation can differ each time...
            # the returned is in the form of the json-ld graph notation, which nice, but not so human readable
            #derived = jsonld.compact(derived)
        data_object.derived = derived
        metadata = data_object.metadata
        metadata.update({'last_modified_at': datetime.now().isoformat()})
        data_object.metadata = metadata
        #data_object.set_metadata(metadata)
        #print(data_object)
        #print(data_object.model_dump_json())
        return data_object

    def apply_to_database(self, database_endpoint: str):
        """
        Apply the given stack of sparql updates to a given database endpoint
        """
        raise NotImplementedError
