# -*- coding: utf-8 -*-
""" Provides the method dc_xml_to_schema_org_jsonld for converting a dublin core xml to a schema.org jsonld file. """
import logging
import os

import typer
from lxml import etree

from data_harvesting.oaipmh.jsonldoutput import JsonldOutput

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
app = typer.Typer(add_completion=True)


@app.command('convert')
def dc_xml_to_schema_org_jsonld(
    input_dir: str = typer.Option(default='.', help='Path to the folder that include dc xml files'),
    output_dir: str = typer.Option(default='.', help='The output folder to put the converted files in'),
):
    """
    Converts all xml files in an input_dir to a jsonld file.
    All xml tags with a dublin core namespace will be mapped to a suitable schema.org property
    and added to the jsonld file.
    """
    try:
        list_dir = os.listdir(input_dir)
    except FileNotFoundError:
        list_dir = []

    file_count = str(len(list_dir))
    logging.info('%s files found in input directory %s.', file_count, input_dir)

    for file in list_dir:
        if not file.endswith('.xml'):
            continue

        filepath = os.path.join(input_dir, file)
        with open(filepath, 'rb') as f:
            content = f.read()

        try:
            xml = etree.fromstring(content)
        except etree.XMLSyntaxError as error:
            logging.error('Error: %s for file %s', str(error), filepath)
            continue

        json_ld = JsonldOutput(xml)
        json_ld.save(os.path.join(output_dir, os.path.basename(filepath)) + '.jsonld')

    logging.info('Script execution done')
