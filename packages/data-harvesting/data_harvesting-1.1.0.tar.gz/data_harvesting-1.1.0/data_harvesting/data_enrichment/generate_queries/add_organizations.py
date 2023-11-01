# -*- coding: utf-8 -*-
"""This module contains code to generate sparql update queries from given lists"""
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import List

import requests

DIR_PATH: Path = Path(__file__).resolve().parent
OUTPUT_FILEPATH = DIR_PATH / 'add_organizations.rd'


@dataclass
class ResearchInstitute:
    ror_id: str
    official_name: str


organization_names = [
    'fzj',
    'geomar',
    'desy',
    'hzg',
    'Alfred Wegener Institute',
    'Max Delbrück Center',
    'hzi',
    'Helmholtz-Zentrum Berlin',
    'gfz',
    'German Aerospace Center',
    'hzdr',
    'ufz',
    'dzne',
    'cispa',
    'Helmholtz Centre for Heavy Ion Research',
    'dkfz',
    'Karlsruhe Institute of Technology',
    'hmgu',
]
organizations: List[ResearchInstitute] = []

for org_name in organization_names:
    ror_api_url = f'https://api.ror.org/organizations?query={org_name}'
    org_data: dict = requests.get(ror_api_url, timeout=60).json()

    # If the org cannot be found in the ROR database, ignore it and continue with the
    # next one.
    if org_data['number_of_results'] == 0:
        print(f'WARNING: no information could be found about {org_name} using the ROR API')
        continue

    ror_id = org_data['items'][0]['id']
    offial_name = org_data['items'][0]['name']

    print(f'{org_name}:\nOffial name: {offial_name} ROR ID: {ror_id}\n')

    organizations.append(ResearchInstitute(ror_id, offial_name))

queries = []
for institute in organizations:
    query = f"""
    PREFIX schema: <http://schema.org/>
    INSERT {{
      <{institute.ror_id}> a schema:Organization ;
         schema:name "{institute.official_name}".
    }}
    """
    query = dedent(query)
    queries.append(query)

OUTPUT_FILEPATH.write_text('# This queries were generated automatically.\n' + ''.join(queries))
