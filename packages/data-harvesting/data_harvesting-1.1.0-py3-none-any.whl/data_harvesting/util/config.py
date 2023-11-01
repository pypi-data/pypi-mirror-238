# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
Contains methods around the configuration file for the harvester pipelines
"""
from pathlib import Path

import yaml

TOP_DIR = Path(__file__).parent.parent.resolve()


def get_config_path():
    """
    return the path to the default config file in the repository
    """

    config_path = TOP_DIR / 'configs' / 'config.yaml'

    return config_path


def get_config(config_path=None):
    """Load a given config and return it"""

    if config_path is None:
        config_path = get_config_path()

    config = None
    with open(config_path, 'r', encoding='utf-8') as fileo:
        config = yaml.load(fileo, Loader=yaml.FullLoader)
    return config
