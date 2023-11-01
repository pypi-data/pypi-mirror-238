# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Command line group for the harvesters"""
from pathlib import Path
from typing import Dict
from typing import List
from typing import Type

import typer
from rich.console import Console
from rich.table import Table

from data_harvesting import get_config_path
from data_harvesting.base_harvester import Harvester
from data_harvesting.datacite import DataciteHarvester
from data_harvesting.gitlab import GitHarvester
from data_harvesting.oaipmh import OAIHarvester
from data_harvesting.sitemap import SitemapHarvester

console = Console()
app = typer.Typer(add_completion=True)

# fixme: get from some pipeline registry file somewhere instead?
pipelines: List[Dict[str, str]] = [
    {
        'name': 'git',
        'description': 'Pipeline to harvest metadata from gitlab projects.'
    },
    {
        'name': 'sitemap',
        'description': 'Pipeline to harvest metadata from a given sitemap.'
    },
    {
        'name': 'datacite',
        'description': 'Pipeline to harvest metadata from a given datacite.'
    },
    {
        'name': 'oai',
        'description': 'Pipeline to harvest metadata from a given OAI-PMH API.'
    },
]

harvester_classmap: Dict[str, Type[Harvester]] = {
    'git': GitHarvester,
    'sitemap': SitemapHarvester,
    'datacite': DataciteHarvester,
    'oai': OAIHarvester
}


# maybe split the different harvesters in several commands
@app.command()
def run(
    name: str = typer.Option('all', help='The harvester to execute.'),
    out: Path = typer.Option(Path('.').resolve(), help='The folder path where to save stuff'),
    config: Path = typer.Option(get_config_path())
) -> None:
    # kwargs: Optional[str] = typer.Option(None, help='Additional parameters to parse to the harvesters')) -> None:
    """Run a certain data harvesting pipeline, default is 'all'"""
    print(f"Starting pipeline '{name}' saving to '{out}'")

    # if out is None:
    #    out = Path('.').resolve()

    if name == 'all':
        # fixme: run this in parallel?
        for pipeline in pipelines:
            hname = pipeline['name']
            harvester = harvester_classmap[hname](outpath=out, config_path=config)
            harvester.run()  # **kwargs)
    else:
        harvester = harvester_classmap[name](outpath=out, config_path=config)
        harvester.run()  # **kwargs)


@app.command('list')  # We do not want to overwrite builtin
def list_harvesters() -> None:
    """List all available harvesters"""

    table = Table('Name', 'Description')
    for pipe in pipelines:
        table.add_row(pipe['name'], pipe['description'])
    console.print(table)
