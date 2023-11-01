# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""

Comment: we assume openaire has a good uniqueness check. We however need to identify which metadata entries are also available in the Center collections and if there are entries in the centers collection which are not in the openaire set.

Also validation is slow, from a partly check all datasets seem to comply with the openaire scheme.
Since the full dataset is a dump from a graph, maybe we should import that graph into a database instead and query the data there, instead of looping over it in python.
maybe we can even ask openaire for a 'datapipeline' to us, with everything connected to the HGF!
"""
import json
from typing import List
from typing import Optional

from jsonschema import validate
from jsonschema.exceptions import ValidationError


def keep_dataset(dataset: dict, identifiers: dict) -> bool:
    """
    Keep the given dataset?

    function which checks if a certain identifier is present
    in the given metadata, if yes, it returns True
    """
    match = False
    for key, identifier, in identifiers.items():
        entry = dataset.get(key, [])
        if isinstance(entry, list):
            for ent in entry:
                if any(hit in ent for hit in identifier):
                    match = True
                    return match
        elif isinstance(entry, str):
            if any(hit in entry for hit in identifier):
                match = True
                return match

    return match


def filter_json_data(
    identifiers: dict,
    filepaths: List[str],
    do_validation: bool = False,
    schemafilepath: Optional[str] = None,
    save_file_path: Optional[str] = None,
    verbose: bool = True
) -> Optional[List[dict]]:
    """
    Function to loop through json data, specially the openaire data set and filter out certain data sets based on given identifiers.

    Since the openaire graph data is quite large (150 GB, with 200 Mio nodes), we do not load it into a DB and query it directly.

    :param identifiers: dictionary of identifiers with values to filter for
    :param filepaths: list of paths to the files with the data, the files are expected to have one json object per line
    :param do_validation: validate each dataset found with the json schema given under schemafilepath
    :param schemafilepath: path to the json schema file
    :param schemafilepath: path to the json schema file
    :param verbose: print additional information (Default True)
    :returns filtered_data: Only if not saved to a file, if saved to a file, None is returned
    """
    if verbose:
        print(f'identifiers: {identifiers}')

    if schemafilepath is None:
        do_validation = False
    else:
        with open(schemafilepath, 'r', encoding='utf-8') as fileo:
            schema = json.load(fileo)
        # print(list(schema['properties'].keys()), len(list(schema['properties'].keys())))

    mined_data = []
    keylength = []

    for filename in filepaths:
        if verbose:
            print(f'reading {filename}')
        count = 0
        with open(filename, 'r', encoding='utf-8') as fileo:
            lines = fileo.readlines()
            for line in lines:
                datat = json.loads(line)
                if do_validation:
                    try:
                        validate(instance=datat, schema=schema)
                    except ValidationError as error:
                        print(error)
                keys = list(datat.keys())
                if keep_dataset(datat, identifiers=identifiers):
                    mined_data.append(datat)
                    count = count + 1
                keylength.append(len(keys))
            #print(statistics.mean(keylength), statistics.median(keylength))
        if verbose:
            print(max(keylength), min(keylength), count)
    if verbose:
        print('data mined: ' + str(len(mined_data)))

    if save_file_path is not None:
        with open(save_file_path, 'w', encoding='utf-8') as fileo:
            json.dump(mined_data, fileo, ensure_ascii=False)
    else:
        return mined_data

    return None
