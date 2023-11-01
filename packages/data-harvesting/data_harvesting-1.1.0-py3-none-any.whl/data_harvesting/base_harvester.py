# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Module containing the Base Harvester class"""
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

from data_harvesting import get_config
from data_harvesting import get_config_path


class Harvester(ABC):
    """Basic harvester class template to be implemented for a given pipeline

    Required in a method called run.
    This class may be extended in the future with maybe functions to parse
    and process data
    """
    outpath: Path
    config: dict
    sources: dict
    last_run: datetime

    def __init__(self, outpath=Path('.'), config_path=get_config_path()):
        """Initialize the Harvester

        Outpath: where data will be stored
        config_path: Path to the config files to read sources
        """
        self.outpath = outpath
        self.set_config(config_path=config_path)

    def set_config(self, config_path=get_config_path()):
        """Set sources and harvester specific config from a given config"""
        full_config = get_config(config_path)

        # This is the harvester specific part in the config
        self.config = full_config.get(self.__class__.__name__, {})
        self.sources = self.config.get('sources', {})
        last_run = self.get_last_run()

        self.last_run = last_run

    def get_sources(self) -> dict:
        """Return sources"""
        return self.sources

    def get_config(self) -> dict:
        """Return harvester specific config"""
        return self.config

    @abstractmethod
    def run(self, **kwargs) -> None:
        """Run the harvester

        This method is required to be implemented for every harvester
        """
        raise NotImplementedError

    def set_last_run(self, time: datetime = datetime.now()) -> None:
        """
        Saves the last run time of the harvester to a file.
        May be overwritten by each harvester.
        """
        harvester = self.__class__.__name__
        with open(f'{harvester}.last_run', 'w', encoding='utf-8') as file:
            file.write(time.strftime('%Y-%m-%d %H:%M:%S'))

    def get_last_run(self) -> Optional[datetime]:
        """
        Get the last run time of the harvester as datetime.
        May be overwritten by each harvester.
        """
        harvester = self.__class__.__name__

        try:
            with open(f'{harvester}.last_run', 'r', encoding='utf-8') as file:
                return datetime.strptime(file.read(), '%Y-%m-%d %H:%M:%S')
        except (FileNotFoundError, ValueError):
            return None


class Harvesters(str, Enum):
    """Enum containing all supported harvesters"""
    GIT = 'GitHarvester'
    SITEMAP = 'SitemapHarvester'
    DATACITE = 'DataciteHarvester'
    OAI = 'OAIHarvester'
