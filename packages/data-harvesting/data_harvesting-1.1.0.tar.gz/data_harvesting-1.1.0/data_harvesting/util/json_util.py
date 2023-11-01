# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Module containing utility functions around json objects"""
import ast
import csv
import json
import os
from typing import List
from typing import Optional
from typing import Set
from typing import Union


# write several json records into one file
def merge_json_records(records_list: Union[List[str], List[dict]], file_dest: str) -> None:
    """Merge several json records together into one file

    Args:
        records_list (List): List of file paths as string, or list of dicts (json data)
        file_dest (str): file path to write to
    """
    data = []
    for record in records_list:
        if isinstance(record, str):
            with open(record, 'r', encoding='utf-8') as fileo:
                datat = json.load(fileo)
                data.append(datat)
        else:
            data.append(record)

    with open(file_dest, 'w', encoding='utf-8') as fileo:
        for datat in data:
            datad = json.dumps(datat, ensure_ascii=False, sort_keys=True)
            fileo.write(datad)
            fileo.write('\n')


# write several json records from one file into many files.
def split_json_records(filepath: str, file_dest_paths: Optional[List[str]] = None):
    """Split json file with a json record on each line into several files with one record each

    Args:
        filepath (str): path to the input json file
        file_dest_paths (List[str]), optional): List of file names to write to has to be as long as number of records in given json file. Defaults to None.
        Then the name is id_.json under the same path as the given filepath
    """

    with open(filepath, 'r', encoding='utf-8') as fileo:
        data = json.load(fileo)

    for i, datat in enumerate(data):
        if file_dest_paths is not None:
            file_dest = file_dest_paths[i]
        else:
            id_ = datat.get('_id', '')
            id_ = id_.replace('/', '.')
            file_dest = os.path.join(os.path.dirname(filepath), str(id_) + '.json')
        with open(file_dest, 'w', encoding='utf-8') as fileo:
            json.dump(datat, fileo, ensure_ascii=False, sort_keys=True)


def write_all_data_to_csv(data: List[dict], tablefilename: str, overwrite=False):
    """Write given data (list of dicts) to a single csv file

    :param data: Data to be written to the csv file in the form of a list of dicts.
                 Further nesting will result in strings written to the csv file
    :type data: List[dict]
    :param tablefilename: Path to the file name to write to
    :type tablefilename: str
    """
    if len(data) == 0:
        print('Empty list provided as data!')
        return None

    if not overwrite:
        if os.path.exists(tablefilename):
            return None

    keys: Set[str] = set()
    for datat in data:
        keyst = set(list(datat.keys()))
        keys = keyst.union(keys)

    header = list(keys)
    header.sort()
    with open(tablefilename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        for datat in data:
            list_t = []
            for key in header:
                list_t.append(datat.get(key, None))
            csv_writer.writerow(list_t)
    return True


def write_all_jsons_to_csv(
    tablefilename: str,
    filelist: Optional[List[str]] = None,
    filefolder: Optional[str] = None,
    overwrite: bool = False,
    filter_for: Optional[str] = None
):
    """Write all given json file paths to a table, or all json files in a given filefolder

    :param filelist: [description]
    :type filelist: List[str]
    :param tablefilename: [description]
    :type tablefilename: str
    :param filefolder: [description], defaults to None
    :type filefolder: str, optional
    :param overwrite: [description], defaults to False
    :type overwrite: bool, optional
    :param filter_for: use only file names which contain this string, defaults to None
    :type filter_for: str, optional
    """
    if filelist is None:
        filelist = []
    data = []
    if filefolder is not None:
        all_files = os.listdir(filefolder)
        for file_j in all_files:
            if file_j.endswith('.json'):
                if filter_for is None:
                    filelist.append(os.path.join(filefolder, file_j))
                else:
                    if filter_for in file_j:
                        filelist.append(os.path.join(filefolder, file_j))

    for file_j in filelist:
        with open(file_j, 'r', encoding='utf-8') as fileo:
            datat = json.load(fileo)
            data.append(datat)

    write_all_data_to_csv(data=data, tablefilename=tablefilename, overwrite=overwrite)


def write_csv_to_jsonfiles(
    tablefilename: str,
    id_key: str = 'id',
    dest_folder: Optional[str] = None,
    dest_filenames: Optional[List[str]] = None,
    overwrite=False
):
    """AI is creating summary for write_csv_to_jsonfiles

    :param tablefilename: Path to the csv file to read
    :type tablefilename: str
    :param id_key: key in the table under which to find an id, which is used for automatic naming '<id>.json' of files.
    :type id_key: str
    :param dest_folder: Path to the folder to same the json files to, defaults to None, in which case the same folder is used as where tablefilename is
    :type dest_folder: str, optional
    :param dest_filenames: List of filenames for each file, has to be the right length, defaults to None, in which case the filenames will be '<id>.json', where the id collum in the table is expected
    :type dest_filenames: List[str], optional
    """
    # TODO consider to implement merge
    data = []
    header: list = []
    with open(tablefilename, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader):
            data_dict = {}
            if i == 0:
                header = row
                continue
            for i, key in enumerate(header):
                # all cells are read and converted to strings, therefore we need to do manuall conversions
                val = row[i]
                if any(
                    val.startswith(mark) for mark in ['[', '{', '"[', '"{']
                ):  # we do not assume that a name will start with [, or {
                    val = ast.literal_eval(row[i])
                # We might still have to do something about numbers
                if not val == '':
                    #val = None
                    #else:
                    data_dict[key] = val
            data.append(data_dict)

    if dest_folder is None:
        dest_folder = os.path.dirname(tablefilename)

    # write to json
    for i, datat in enumerate(data):
        if dest_filenames is None:
            id_d = datat.get(id_key, str(i))
            id_d = id_d.replace('/', '.')
            filename = f'{id_d}.json'
        else:
            filename = dest_filenames[i]
        dest = os.path.join(dest_folder, filename)
        if not overwrite:
            if os.path.exists(dest):
                print(f'File: {dest} exists, I do not overwrite it.')
                continue
        # We sort the keys for better diffs, otherwise each time all files will differ.
        with open(dest, 'w', encoding='utf-8') as fileo:
            json.dump(datat, fileo, ensure_ascii=False, sort_keys=True)
