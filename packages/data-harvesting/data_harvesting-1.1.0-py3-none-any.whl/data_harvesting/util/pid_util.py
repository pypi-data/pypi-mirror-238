# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
'''
Module containing function to generate uuid, pids and and to help dealing with these.

maybe consider using https://github.com/skorokithakis/shortuuid instead, also
'''
import uuid


def generate_uuid():
    """Function to generate and return a universal random uuid for our purposes

    We want to have a universal unique id which is save,
    i.e does not contain any personal information in its generation

    Convert a UUID to a string of hex digits in standard form:
    str(uuid.uuid4())
    # Convert a UUID to a 32-character hexadecimal string
    uuid.uuid4().hex

    :return: A uuid from pythons uuid module
    :rtype: uuid.UUID
    """
    return uuid.uuid4()


def generate_uuid5(namespace, name: str):
    """Function to generate and return a universal uuid for our purposes
    from a specified namespace like DNS, URL, OID, X500

    We want to have a universal unique id which is save,
    i.e does not contain any personal information in its generation

    example: uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')


    Convert a UUID to a string of hex digits in standard form:
    str(uuid.uuid5())
    # Convert a UUID to a 32-character hexadecimal string
    uuid.uuid5().hex

    :return: A uuid from pythons uuid module
    :rtype: uuid.UUID
    """
    return uuid.uuid5(namespace, name)
