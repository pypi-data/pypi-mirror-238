# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Utility CLI for the unHide data_harvesting."""
import typer

from cron import setup as cron
from data_harvesting.cli import aggregator
from data_harvesting.cli import converter
from data_harvesting.cli import harvesters
from data_harvesting.cli import indexer
from data_harvesting.cli import util
from data_harvesting.oaipmh import convert_harvest

cli = typer.Typer(add_completion=True)
cli.add_typer(cron.app, name='cron')
cli.add_typer(harvesters.app, name='harvester')
cli.add_typer(converter.app, name='rdf')
cli.add_typer(convert_harvest.app, name='dcxml')
cli.add_typer(util.app, name='util')
cli.add_typer(indexer.app, name='indexer')
cli.add_typer(aggregator.app, name='aggregator')

if __name__ == '__main__':  # pragma: no cover
    cli()
