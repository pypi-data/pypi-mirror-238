# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
'''
Module which contains helper functions to deal with xml data, or convert xml to json
'''
from typing import List
from typing import Optional
from xml.etree.ElementTree import fromstring

from xmljson import yahoo as yh


def convert_xml_to_json(xml_data: str, to_replace: Optional[List[tuple]] = None):
    """AI is creating summary for convert_xml_to_json

    :param xml_data: xml data as string
    :type xml_data: str
    """
    if to_replace is None:
        to_replace = [('r3d:', ''), (r' content="', r' content_save="')]
    #data_new = xml_data.replace('r3d:', '') # otherwise the replacement of this will prefix every key
    #data_new = xml_data.replace(r' content="', r' content_save="') # replace content attribute to something more save
    data_new = xml_data
    for val, rep in to_replace:
        data_new = data_new.replace(val, rep)

    etree = fromstring(data_new)
    data_dict = yh.data(etree)
    #pprint(data_dict)

    return data_dict
