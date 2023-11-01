# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Small command line interface to run the indexer"""
import logging
from pathlib import Path
from typing import List
from typing import Optional

import progressbar
import typer
from pathos.multiprocessing import ProcessingPool as Pool

from data_harvesting.indexer.indexer import index_dir
from data_harvesting.indexer.indexer import Indexer

app = typer.Typer(add_completion=False)


@app.command('index')
def index(
    filenames: Optional[List[Path]] = typer.Argument(None, help='The file or file names to be indexed'),
    folder: Optional[Path] = typer.Option(None, '--folder', '-d', help='The folder path to be indexed.'),
    reindex_all: bool = typer.Option(
        False, '--reindex-all', '-ria', help='Re-index all entries, i.e overwrite if existing.'
    ),
    reindex_query: str = typer.Option(
        None, '--reindex-query', '-fq', help='fq (filter query) expression to reindex from items already in the index'
    ),
    config: Optional[Path] = typer.Option(None, help='The path with the indexer config.'),
    fail_errors: bool = typer.Option(
        False, '--fail', '-e', help='Make the indexer fail on error. I.e exceptions are raised'
    ),
    info: bool = typer.Option(True, '--info', help='Print information about the indexer.'),
    progress: bool = typer.Option(False, '--progress', help='Display a progress bar.')
):
    """
    Run the indexer to index a certain data, given a datafile, list of files, or all files in a directory
    """
    indexer = Indexer(config)

    if info:
        indexer.info()
    filenames = filenames or []
    prbar = None
    #if len(filenames) >1:
    nfls = len(filenames)

    if progress:
        with progressbar.ProgressBar(max_value=nfls) as prbar:  #, redirect_stdout=True)

            def process_multi_f(arg):
                """Helper function"""
                i = arg[0]
                filep = arg[1]
                prbar.update(i)
                logging.info(f'Indexing file {i}/{nfls}: {filep}')
                indexer.index_file(filep, fl_reindex=reindex_all, fail=fail_errors)

            args = [enumerate(filenames)]
            with Pool(6) as poolt:
                poolt.map(process_multi_f, args)
        #for i, filep in enumerate(filenames):
        #    prbar.update(i)
        #    logging.info(f'Indexing file {i}/{nfls}: {filep}')
        #    indexer.index_file(filep, fl_reindex=reindex_all, fail=fail_errors)
    else:
        for i, filep in enumerate(filenames):
            logging.info(f'Indexing file {i}/{nfls}: {filep}')
            indexer.index_file(filep, fl_reindex=reindex_all, fail=fail_errors)

    if folder is not None:
        logging.info(f'Indexing dir: {folder}')
        index_dir(folder, indexer, fl_reindex=reindex_all, fail=fail_errors, pbar=True)
    if reindex_query is not None:
        indexer.reindex_query(reindex_query, fail=fail_errors)
    logging.info('Indexer finished')
