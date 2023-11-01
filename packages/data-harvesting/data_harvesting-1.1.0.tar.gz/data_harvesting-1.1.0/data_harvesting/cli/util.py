# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Command line group for exposed utility"""
import json
from pathlib import Path
from typing import List
from typing import Optional

import typer
from jsondiff import diff
from rich.console import Console

from data_harvesting.datacite.datacite_harvester import correct_keywords as correct_keyw
from data_harvesting.util.data_model_util import upload_data_filepath

console = Console()
app = typer.Typer(add_completion=True)


@app.command('correct-keywords')
def correct_keywords(
    filenames: List[Path],
    overwrite: bool = typer.Option(
        True, '--overwrite', help='Overwrite the files inplace or save them with _corrected.'
    ),
    dry_run: bool = typer.Option(False, '--dry-run', help='Do not change any file, print the difference to console.'),
) -> None:
    """Apply keyword format correction to keyword lists in the given files

    format has to be something that json can read
    full example usage
    ```
    hmc_unhide util correct-keywords --overwrite True ./*.json
    ```
    """
    folders = []

    for filename in filenames:
        if filename.is_dir():
            folders.append(filename)
            continue
        print(f'Correcting {filename}')
        with open(filename, 'r', encoding='utf-8') as fileo:
            data = json.load(fileo)
        if isinstance(data, list):
            continue  # for now
        data_new = correct_keyw(data)  # inline change

        if dry_run:
            print(diff(data, data_new, syntax='explicit'))
        else:
            if overwrite:
                filename_new = str(filename)
            else:
                splits = str(filename).split('.')
                filename_new = '.'.join(splits[:-1]) + '_corrected.' + splits[-1]

            with open(filename_new, 'w', encoding='utf-8') as fileo:
                json.dump(data_new, fileo)

    for folder in folders:
        for filename in folder.glob('**/*.jsonld'):
            print(f'Correcting {filename}')
            with open(filename, 'r', encoding='utf-8') as fileo:
                data = json.load(fileo)

            if isinstance(data, list):
                continue  # for now
            data_new = correct_keyw(data)  # inline change

            if dry_run:
                print(diff(data, data_new, syntax='explicit'))
            else:
                if overwrite:
                    filename_new = str(filename)
                else:
                    splits = str(filename).split('.')
                    filename_new = '.'.join(splits[:-1]) + '_corrected.' + splits[-1]

                with open(filename_new, 'w', encoding='utf-8') as fileo:
                    json.dump(data_new, fileo)


@app.command('upload')
def upload(
    filepath: List[Path],
    graph_name: Optional[str] = typer.Option(
        'http://www.purl.com/test/my_graph', '--graph', help='The graph to upload data to.'
    ),
    endpoint_url: Optional[str] = typer.Option(
        'http://localhost:8890/sparql-auth', '--ep', help='The sparql endpoint to interact with.'
    ),
    username: Optional[str] = typer.Option('dba', '--user', help='The user for interaction with the endpoint.'),
    passwd: Optional[str] = typer.Option('dba', '--pw', help='The password for the provided user.')
):
    """Upload LinkedData to a triple store

    :param filepath: A list of paths to files, or a folders with files.
    :type filepath: List[Path]
    :param graph_name: The graph to upload data to. defaults to 'http://www.purl.com/test/my_graph'
    :type graph_name: Optional[str], optional
    :param endpoint_url: The sparql endpoint to interact with. defaults to 'http://localhost:8890/sparql-auth'
    :type endpoint_url: Optional[str], optional
    :param username: The user for interaction with the endpoint., defaults to 'dba'
    :type username: Optional[str], optional
    :param passwd: The password for the provided user., defaults to 'dba'
    :type passwd: Optional[str], optional
    """

    folders = []

    for filename in filepath:
        if filename.is_dir():
            folders.append(filename)
            continue
        print(f'Uploading {filename}')
        upload_data_filepath(
            filepath=filename, graph_name=graph_name, endpoint_url=endpoint_url, username=username, passwd=passwd
        )
    for folder in folders:
        for filename in folder.glob('**/*.json'):
            print(f'Uploading {filename}')
            try:
                upload_data_filepath(
                    filepath=filename,
                    graph_name=graph_name,
                    endpoint_url=endpoint_url,
                    username=username,
                    passwd=passwd
                )
            except Exception as msg:  # pylint: disable=broad-exception-caught
                print(f'Exception on upload, {msg}')
