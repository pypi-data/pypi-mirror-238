# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
'''
Module, which contains function to perform mappings
'''
import json
import os
from json.decoder import JSONDecodeError

import jq


def apply_jq_mapping(data: dict, mapping: dict, silent: bool = True, verbose: bool = True) -> dict:
    """Apply some given jq mapping to some data

    :param data: data to be mapped, i.e. converted.
    :type data: dict
    :param mapping: the mapping, i.e. the conversion/cross walk to be applied.
        Applied key wise, i.e. it has to be in the form {'key1': jq_string, 'key2': jq_string2, ...}
    :type mapping: dict
    :param silent: if true no errors will be raised, defaults to True
    :type silent: bool, optional
    :param verbose: if true additional information will be printed, defaults to True
    :type verbose: bool, optional
    :raises ValueError: errors thrown by jq.compile, will be surpressed if silent==True
    :return: the resulting data from the applied mapping
    :rtype: dict
    """

    results = {}
    for key, val in mapping.items():
        raw_str = None
        try:
            raw_str = jq.compile(val).input(data).text()  # pylint: disable=c-extension-no-member
        except ValueError as error:
            if verbose:
                print(f'Failed Mapping of {key} failed for {val}')
                print(error)
            if not silent:
                raise error

        # i.e. if the parsing of the key fails we it will not exist, but we will continue.
        criterion = [raw_str == crit for crit in ['null']]
        if raw_str is None:  # has to be separate
            pass
        elif not any([not raw_str, raw_str is None, len(raw_str) == 0, any(criterion)]):
            try:
                results[key] = json.loads(raw_str)
            except JSONDecodeError as error:
                # parse as string
                #if not '{' in raw_str:
                #    results[key] = json.loads(r"{}".format(raw_str))
                #else:
                print(raw_str)
                raise error
    return results


def apply_jq(data: dict, mapping: str, silent: bool = True, verbose: bool = True) -> dict:
    """
    Apply a single jq mapping
    """
    results: dict = {}
    try:
        raw_str = jq.compile(mapping).input(data).text()  # pylint: disable=c-extension-no-member
    except ValueError as error:
        if verbose:
            print(f'Failed Mapping of {mapping} failed for {data}')
            print(error)
        if not silent:
            raise error
    # i.e. if the parsing of the key fails we it will not exist, but we will continue.
    criterion = [raw_str == crit for crit in ['null']]
    if raw_str is None:  # has to be separate
        pass
    elif not any([not raw_str, raw_str is None, len(raw_str) == 0, any(criterion)]):
        try:
            results = json.loads(raw_str)
        except JSONDecodeError as error:
            # parse as string
            print(raw_str)
            raise error
    # do this rekursive
    #if remove_null:
    #    for key, val in results.items():
    #        if val=='null':
    #            results[key].pop
    return results


def apply_jq_mapping_file(inputfile: str, outputfile: str, mapping: dict, **kwargs):
    """Apply a given jq mapping dict to a file and write output to an output file

    any kwargs will be parsed to apply_jq_mapping
    like [silent: bool, verbose: bool]

    :param inputfile: path to input file
    :type inputfile: str
    :param outputfile: path to output file
    :param mapping: the mapping, i.e. the conversion/cross walk to be applied.
        Applied key wise, i.e. it has to be in the form {'key1': jq_string, 'key2': jq_string2, ...}
    :type mapping: dict
    """

    if 'data' in kwargs:
        print('data given in kwargs, will be ignored')
        kwargs.pop('data')

    with open(inputfile, 'r', encoding='utf-8') as file_o:
        dataraw = json.load(file_o)

    results = apply_jq_mapping(data=dataraw, mapping=mapping, **kwargs)

    with open(outputfile, 'w', encoding='utf-8') as file_o:
        json.dump(results, file_o, indent=4, separators=(', ', ': '), sort_keys=True)


def apply_jq_mapping_folder(folder_source: str, folder_dest: str, mapping: dict, **kwargs):
    """Apply a jq mapping dict to all files within a given folder and write results to another folder

    any kwargs will be parsed to apply_jq_mapping
    like [silent: bool, verbose: bool]

    :param folder_source: path to the folder which contains files to convert
    :type folder_source: str
    :param folder_dest: path to folder to store the results.
    :type folder_dest: str
    :param mapping: the mapping, i.e. the conversion/cross walk to be applied.
        Applied key wise, i.e. it has to be in the form {'key1': jq_string, 'key2': jq_string2, ...}
    :type mapping: dict
    """
    output_filepaths = []
    files = os.listdir(folder_source)

    for filepath in files:
        source = os.path.join(folder_source, filepath)
        dest_file = os.path.join(folder_dest, 'map_' + filepath)
        output_filepaths.append(dest_file)
        apply_jq_mapping_file(inputfile=source, outputfile=dest_file, mapping=mapping, **kwargs)

    return output_filepaths
