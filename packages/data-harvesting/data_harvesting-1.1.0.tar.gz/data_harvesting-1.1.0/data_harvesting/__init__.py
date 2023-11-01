# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
'''
Data Harvesting
'''
#import importlib_metadata
#from typing_extensions import Final

__version__: str = 'v1.1.0'
#Final[str] = "v1.1.0" #importlib_metadata.version(__package__ or __name__)

from .util.config import get_config_path
from .util.config import get_config
