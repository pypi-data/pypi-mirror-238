# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""Module containing the OAI-PMH Harvester class"""
import logging
import os
import subprocess
import time

from data_harvesting.base_harvester import Harvester
from data_harvesting.data_model import derive_metadata
from data_harvesting.oaipmh.convert_harvest import dc_xml_to_schema_org_jsonld
from data_harvesting.util.data_model_util import convert_json_unhide

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class OAIHarvester(Harvester):
    """
    Harvester to collect dublin core xml data from OAI-PMH APIs
    Implements run() function from BaseClass but nothing else for now
    """
    def run(self, **kwargs) -> None:
        t = time.localtime()
        start_time = time.strftime('%H:%M:%S', t)
        log_file = f'oai_harvest_{start_time}.log'
        logging.info('OAI Harvester starts. Check %s for details…', log_file)

        for center_name, center_data in self.sources.items():
            output_dir = os.path.join(self.outpath, center_name)
            logging.info('Start OAI harvesting from %s to %s', center_name, output_dir)

            cmd = f"oai-harvest --dir {output_dir} --no-delete --metadataPrefix oai_dc {center_data['oai_endpoint']}"
            cmd += f' --from {self.last_run.strftime("%Y-%m-%d")}' if self.last_run is not None else ''
            cmd += f' >> {log_file} 2>&1'

            with subprocess.Popen(cmd, shell=True) as process:
                process.wait()

            dc_xml_to_schema_org_jsonld(output_dir, output_dir)

            # convert to unhide data
            metadata = derive_metadata()
            metadata['harvester_class'] = 'OAIHarvester'
            metadata['provider'] = center_name
            metadata['endpoint'] = center_data['oai_endpoint']
            metadata['preprocess'] = 'prov:dc_xml_to_schema_org'
            convert_json_unhide(output_dir, metadata=metadata, overwrite=True)

        self.set_last_run()
