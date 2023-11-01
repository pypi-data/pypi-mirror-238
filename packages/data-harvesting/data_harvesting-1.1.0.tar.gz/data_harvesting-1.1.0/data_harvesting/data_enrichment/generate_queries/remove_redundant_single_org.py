# -*- coding: utf-8 -*-
"""This file contains a script to generate sparql updates for organizations,

this still needs to be generalized and integrated into the data-harvesting code base """
import json
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import List

import requests

DIR_PATH: Path = Path(__file__).resolve().parent
OUTPUT_FILEPATH = DIR_PATH / 'remove_redundant_single_org.rd'
INPUT_FILEPATH = DIR_PATH / 'single_org_names.json'


@dataclass
class ResearchOrganizationWithNames:
    ror_id: str
    official_name: str
    alternative_names: List[str]


raw_data: dict = json.loads(INPUT_FILEPATH.read_text())
print(raw_data.keys())

organizations = []
for org_name, alternative_names in raw_data.items():
    ror_api_url = f'https://api.ror.org/organizations?query={org_name}'
    org_data: dict = requests.get(ror_api_url, timeout=(10, 100)).json()

    # If the org cannot be found in the ROR database, ignore it and continue with the
    # next one.
    if org_data['number_of_results'] == 0:
        print(f'WARNING: no information could be found about {org_name} using the ROR API')
        continue

    ror_id = org_data['items'][0]['id']
    official_name = org_data['items'][0]['name']

    print(f'{org_name}:\nofficial name: {official_name} ROR ID: {ror_id}\n')

    organizations.append(ResearchOrganizationWithNames(ror_id, official_name, alternative_names))

queries = []
for institute in organizations:
    alternative_name_str: str = '\n    '.join([f'"{name}"' for name in institute.alternative_names])
    query = f"""
    INSERT {{ ?res schema:affiliation ?org}}
    WHERE {{
    ?res schema:affiliation ?affname.  . FILTER (STR(?affname) IN ({alternative_name_str}))
    ?org a schema:Organization. FILTER (ISIRI(?org)).
    ?org schema:name ?orgname . FILTER (STR(?orgname) =STR(?affname))
    }}
    """
    query = dedent(query)
    queries.append(query)

# file_contents = ""
# for query_string in queries:
#     file_contents += query_string

OUTPUT_FILEPATH.write_text(f"# This queries were generated automatically.\n{''.join(queries)}")
