# -*- coding: utf-8 -*-
"""
Class that takes a lxml.etree object on init and maps each found dublin core tag to a suitable schema.org property.
Everything is stored in a python dict following json_ld style and exported to a jsonld file by the save() method.
"""
import json
import logging
import os
from typing import Optional
from typing import Tuple
from typing import Union

from lxml import etree

from data_harvesting.oaipmh.constants import IDENTIFIER_NAMESPACE
from data_harvesting.oaipmh.constants import PURL_PREFIX


class JsonldOutput:
    """
    Class that takes a lxml.etree object on init and maps each found dublin core tag to a suitable schema.org property.
    Everything is stored in a python dict following json_ld style and exported to a jsonld file by the save() method.
    """
    _json_ld: dict
    _xml: etree

    def __init__(self, xml: etree):
        """ Initializes the json ld dict and start the processing of converting the dublin core tags """
        self._xml = xml
        self._json_ld = {
            '@context': {
                '@vocab': 'https://schema.org/'
            },
            '@type': 'DigitalDocument',
        }

        namespace = {'dc': xml.nsmap.get('dc', 'http://purl.org/dc/elements/1.1/')}

        for elem in xml.iterfind('*', namespaces=namespace):
            self._process_tag(elem)

    def save(self, file_path: str):
        """
        Save the json_ld object to the file given on file_path.
        All folders on the path will be created.
        """
        try:
            os.makedirs(os.path.dirname(file_path))
        except FileExistsError:
            pass

        with open(file_path, 'w', encoding='utf-8') as file_o:
            json.dump(self._json_ld, file_o, indent=4, separators=(', ', ': '), ensure_ascii=False)

    def _process_tag(self, elem: etree) -> None:
        """
        Takes a dc xml tag and maps it to the correct mapping function _map_tagName
        If no function for the tag exists an error is added to the error list (see self.get_errors())
        """
        tag_name = etree.QName(elem).localname

        try:
            func = getattr(self, f'_map_{tag_name}')
            func(elem)
        except AttributeError:
            logging.warning('No handle function found for tag %s. Skipping.', tag_name)

    def _map_identifier(self, elem: etree) -> None:
        """
        Maps dc:identifier to schema.org identifier tag.
        Sets the found identifier as @id for json ld if it's a URL
        or parses it if it's an info uri or urn
        """
        ident: str = elem.text

        if ident is not None:
            property_data = {
                '@type': 'PropertyValue',
                'value': ident,
            }

            if ident.startswith('http'):
                property_data.update({'@id': ident, 'url': ident})

            if ident.startswith('info:') or ident.startswith('urn:'):
                data = ident.split(':')
                identifier_type = data[1]
                identifier = data[2]
                property_data.update(self.__alt_identifier_to_property_data(identifier, identifier_type))

            self._json_ld['identifier'] = self._json_ld.get('identifier', []) + [property_data]

    def _map_creator(self, elem: etree) -> None:
        self._json_ld['creator'] = self._json_ld.get('creator', []) + [{'name': elem.text}]

    def _map_contributor(self, elem: etree) -> None:
        self._json_ld['contributor'] = self._json_ld.get('contributor', []) + [{'name': elem.text}]

    def _map_title(self, elem: etree) -> None:
        self._json_ld['name'] = elem.text

    def _map_description(self, elem: etree) -> None:
        self._json_ld['abstract'] = elem.text

    def _map_language(self, elem: etree) -> None:
        self._json_ld['inLanguage'] = elem.text

    def _map_publisher(self, elem: etree) -> None:
        self._json_ld['publisher'] = {'@type': 'Organization', 'name': elem.text}

    def _map_rights(self, elem: etree) -> None:
        self._json_ld['license'] = elem.text

    def _map_format(self, elem: etree) -> None:
        self._json_ld['encodingFormat'] = self._json_ld.get('encodingFormat', [elem.text]) + []

    def _map_subject(self, elem: etree) -> None:
        self._json_ld['keywords'] = self._json_ld.get('keywords', []) + [{'name': elem.text}]

    def _map_type(self, elem: etree) -> None:
        """
        Maps dc:type tag to schema.org genre property
        """
        content = elem.text
        schema_tag = 'genre'

        if content and content.startswith('info:eu-repo'):
            set_schema_tag, content = self._parse_eu_repo(elem.text)
            schema_tag = schema_tag if set_schema_tag is None else set_schema_tag

        self._json_ld[schema_tag] = self._json_ld.get(schema_tag, [content]) + []

    def _map_date(self, elem: etree) -> None:
        self._json_ld['datePublished'] = elem.text

    def _map_doi(self, elem: etree) -> None:
        """Maps dc:doi tag either to the @id attribute if not set yet or to schema.org sameAs property"""
        doi = elem.text
        property_id, base_url = self._get_property_data_for_identifier_type('doi')
        url = base_url + doi
        identifier = {'@id': url, '@type': 'PropertyValue', 'propertyID': property_id, 'value': doi, 'url': url}

        self._json_ld['identifier'] = self._json_ld.get('identifier', []) + [identifier]

    def _map_source(self, elem: etree) -> None:
        self._json_ld['provider'] = elem.text

    def _map_audience(self, elem: etree) -> None:
        # TODO: Check if Range is correct
        self._json_ld['audience'] = {'@type': 'Audience', 'audienceType': elem.text}

    def _map_coverage(self, elem: etree) -> None:
        self._json_ld['spatial'] = {'@type': 'Place', 'keywords': [elem.text]}

    def _parse_eu_repo(self, repo_string: str) -> Tuple[Optional[str], Optional[Union[dict, str]]]:
        """Parse an info:eu-repo url (c.f. https://wiki.surfnet.nl/display/standards/info-eu-repo) if necessary"""

        data = repo_string.split('/')

        property_obj = {
            '@type': 'PropertyValue',
            'value': data,
        }

        if len(data) <= 2:
            # In this case we actually have an empty entry but
            url = PURL_PREFIX + repo_string
            property_obj['url'] = url

            return None, property_obj

        try:
            if data[2] == 'altIdentifier':
                identifier_type = data[3]
                identifier = '/'.join(data[4:])

                if not identifier:
                    raise IndexError

                property_obj.update(self.__alt_identifier_to_property_data(identifier, identifier_type))

                return 'sameAs', property_obj

            if data[1] == 'semantics':
                identifier = '/'.join(data[2:])
                return 'genre', identifier

            if data[1] == 'grantAgreement':
                identifier = '/'.join(data[2:])
                return 'citation', identifier

        except IndexError:
            # In that case our entry is actually empty
            return None, ''

        url = PURL_PREFIX + repo_string
        property_obj['url'] = url

        return None, repo_string

    def __alt_identifier_to_property_data(self, identifier: str, identifier_type: str) -> dict:
        """
        Gets data  for an identifier namespace from constant.py.
        If no data is found a warning is thrown.
        """

        # HMGU and GFZ use invalid identifiers pissn and eissn for issn…
        if identifier_type in ['pissn', 'eissn']:
            identifier_type = 'issn'

        property_id, base_url = self._get_property_data_for_identifier_type(identifier_type)

        if base_url is not None:
            url = base_url + identifier
            return {'@id': url, 'propertyID': property_id, 'url': url}

        logging.warning('No identifier data for identifier_type %s and identifier %s', identifier_type, identifier)
        return {}

    def _map_relation(self, elem: etree) -> None:
        """
        Maps dc:relation tag to schema.org sameAs
        if not set otherwise by info:eu-repo information
        """
        content = elem.text
        schema_tag = 'sameAs'

        if content and content.startswith('info:eu-repo'):
            set_schema_tag, content = self._parse_eu_repo(elem.text)
            schema_tag = schema_tag if set_schema_tag is None else set_schema_tag

        self._json_ld[schema_tag] = self._json_ld.get(schema_tag, [content]) + []

    @staticmethod
    def _get_url_from_doi(doi: str) -> str:
        return 'https://doi.org/' + doi

    @staticmethod
    def _get_property_data_for_identifier_type(identifier_type: str) -> Tuple[Optional[str], Optional[str]]:
        """If data for an identifier namespace exists in config IDENTIFIER_NAMESPACE we return it"""
        if identifier_type in IDENTIFIER_NAMESPACE:
            namespace = IDENTIFIER_NAMESPACE[identifier_type]
            return namespace['description_url'], namespace['resolving_url']

        return None, None
