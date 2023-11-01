# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""
This module contains util and a class to harvest metadata from data cite with respect to organizations

given a ROAR identifier a query is posted to the graphql API of datacite to receive all
connected PIDS. Then over an API request the full datacite metadata is extracted for each of these PIDS
This metadata is then converted to a desired format.
"""
import binascii
import json
import time
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

import progressbar
import requests

from data_harvesting.base_harvester import Harvester
from data_harvesting.data_model import derive_metadata
from data_harvesting.data_model import LinkedDataObject
# from lxml import etree


def convert_datacite(metadata: dict, dataformat: str = 'schema.org jsonld'):
    """
    Convert a given datecite metadata entry to some other format default schema.org json-ld

    :param metadata: [description]
    :type metadata: [type]
    :param dataformat: [description], defaults to schema.org jsonld
    :type dataformat: str, optional
    """
    pass
    # under the xml key is the whole metadata in Base64


def correct_keywords(mdata: dict) -> dict:
    """Data cite provides all keywords in a single string, also it adds topic to keywords

    The frontend expects here a list.
    # TODO maybe add something to deal with the field syntax > >.
    # TODO: maybe also make this a set of keywords to avoid duplicates
    # TODO: enrich keywords via AI extractions from title and abstract texts and also how these
    # correspond to a certain field.
    # TODO: generalize, if a list of dicts is given, or keywords are nested further down
    """
    keywords = mdata.get('keywords', None)
    new_data = mdata.copy()  # do not do inline changes
    if (keywords is not None) and isinstance(keywords, str):
        keywords = keywords.split(',')
        keywords = [keyword.strip() for keyword in keywords]

        new_data['keywords'] = keywords
    return new_data


def extract_metadata_restapi(pid: str) -> Optional[dict]:  #etree
    """
    Request the datacite metadata for a given pid over the rest API
    """
    # parse doi to right format 10.5438/0012
    doi = pid.lstrip('https://doi.org/')
    base_url = 'https://api.datacite.org/dois/'
    record_url = base_url + doi
    # application/ld+json text/turtle
    headers = {'Accept': 'application/ld+json'}
    req = requests.get(record_url, headers=headers, timeout=(10, 60))
    datacite_json: Optional[dict] = req.json()
    if req.status_code != 200:
        datacite_json = None
    return datacite_json


def query_graphql_api(roar: str,
                      max_count: int = 2000,
                      get_all: bool = True,
                      since: Optional[str] = None) -> Tuple[List[str], List[List[dict]]]:
    """
    Query the Graphql graph of Datacite over the API

    We do this instead of a query to the normal API, because the graph contains more aggregated links
    to works. Through the PIDS of works in the Graph do not have to correspond to the PIDS of the same
    work in the usual Datacite API.


    example:
    curl 'https://api.datacite.org/graphql' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json'
    -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://api.datacite.org' --data-binary '{"query":"{organization(id: \"https://ror.org/02nv7yv05\") {\nid name\n    works (first:3){nodes {id}}}}"}' --compressed

    # The api is a bit unstable, or restricted, this is why serialize the data
    #todo implement since, i.e the 'updated' key
    """
    url = 'https://api.datacite.org/graphql'
    query = """query {organization(id: "https://ror.org/02nv7yv05") {
id name alternateName wikipediaUrl citationCount viewCount
    downloadCount
    works (first:3){totalCount
      published {
        title count}
      resourceTypes {
        title count}
      nodes {id}}}}"""
    #query = '{organization(id: \"https://ror.org/02nv7yv05\") {id name works (first:'+ str(max_count) + '){totalCount nodes {id}}}}'
    query = '{organization(id: ' + f'\"{roar}\"' + ') {id name works (first:' + str(
        max_count
    ) + '){totalCount pageInfo {endCursor hasNextPage} nodes {id doi publisher relatedIdentifiers{relatedIdentifier relationType}}}}}'
    #print(query)
    query_f = query  #.format(roar, max_count)#=roar, max_count=max_count)
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://api.datacite.org'
    }
    req = requests.post(url, json={'query': query_f}, headers=headers, timeout=(10, 600))
    json_data = json.loads(req.text)
    if req.status_code != 200:
        print(f'Failed to query datacite graphql API for {roar}')
        return [], []

    #print(json_data)
    json_data_all = json_data
    total_count = json_data['data']['organization']['works']['totalCount']
    print(f'Found {total_count} records for {roar}')
    pid_list = [val['id'] for val in json_data['data']['organization']['works']['nodes']]
    if (total_count >= max_count) and get_all:
        # we missed some records, query again to get all
        further_queries = total_count // max_count
        for i in range(further_queries):
            last_id = json_data['data']['organization']['works']['pageInfo']['endCursor']
            # offset is not supported by datacite graphql api, but after is
            query_f = '{organization(id: ' + f'\"{roar}\"' + ') {id name works (first:' + str(
                max_count
            ) + ' after: \"' + last_id + '\"){totalCount pageInfo {endCursor hasNextPage} nodes {id doi publisher relatedIdentifiers{relatedIdentifier relationType}}}}}'
            print(query_f)
            req = requests.post(
                url, json={'query': query_f}, headers=headers, timeout=(10, 600)
            )  #query.format(roar=roar, max_count=max_count)})
            json_data = json.loads(req.text)
            pid_list.extend([val['id'] for val in json_data['data']['organization']['works']['nodes']])
            nodes_all = json_data_all['data']['organization']['works']['nodes']
            nodes_all.extend(json_data['data']['organization']['works']['nodes'])
            json_data_all['data']['organization']['works']['nodes'] = nodes_all

    return pid_list, json_data_all


def harvest_roar(
    roar: str,
    since: Optional[str] = None,
    base_savepath: Optional[Path] = None,
    skip_existing: Optional[bool] = True,
    use_cached_ql: Optional[bool] = True,
    unhidedata: bool = True
):  #pylint: disable=too-many-statements
    """
    For each pid related to the roar identifier, down load all metadata records

    updated since then.
    """
    failed_records = []
    successful_records = []

    if base_savepath is None:
        base_savepath = Path('.')
    base_savepath.mkdir(parents=True, exist_ok=True)

    filename = 'graph_ql_res.json'  #binascii.hexlify(roar.encode('utf-8')).decode() + ".json"
    graph_query: Path = base_savepath / filename
    filename2 = 'pid_list.txt'  #binascii.hexlify(roar.encode('utf-8')).decode() + ".json"
    pid_list_path: Path = base_savepath / filename2
    store = True
    if pid_list_path.exists() and graph_query.exists() and use_cached_ql:
        store = False
        with open(graph_query, 'r', encoding='utf-8') as fileo:
            json_data = json.load(fileo)
        with open(pid_list_path, 'r', encoding='utf-8') as fileo:
            record_pids = fileo.readlines()
    else:
        record_pids, json_data = query_graphql_api(roar, since=since)

    if len(record_pids) == 0:
        return [], []

    if store:
        with open(graph_query, 'w', encoding='utf-8') as fileo:
            json.dump(json_data, fileo, indent=4, separators=(', ', ': '), sort_keys=True)
        with open(pid_list_path, 'w', encoding='utf-8') as fileo:
            for item in record_pids:
                fileo.write(f'{item}\n')

    npids = len(record_pids)
    print(f'Harvesting {npids} record pids from Datacite {roar}')
    with progressbar.ProgressBar(max_value=npids) as pbar:
        for i, record in enumerate(record_pids):
            pbar.update(i)
            if unhidedata:
                filename = binascii.hexlify(record.encode('utf-8')).decode() + '.json'
            else:
                filename = binascii.hexlify(record.encode('utf-8')).decode() + '.jsonld'
            jsonld_filepath: Path = base_savepath / filename
            if jsonld_filepath.exists() and skip_existing:
                successful_records.append(record)
                continue
            mdata = extract_metadata_restapi(record)
            time.sleep(0.01)

            if mdata is None:
                # look into related identifiers sameAs is in Datacite IsVariantFormOF
                related_identifier = json_data['data']['organization']['works']['nodes'][i]['relatedIdentifiers']
                for identifier in related_identifier:
                    if identifier['relationType'] == 'IsVariantFormOf':
                        identifier_totry = identifier['relatedIdentifier']
                        mdata = extract_metadata_restapi(identifier_totry)
                if mdata is None:
                    print(f'Failed, to retrieve jsonld {record}')
                    failed_records.append(record)
                    continue
            mdata = correct_keywords(mdata)  # TODO: since we change the original data here: we might
            # want to move this into some uplifting tasks (also if for other sources) and track the
            # provenance for it.
            if unhidedata:  # store as linked data.
                metadata = derive_metadata()
                metadata['harvester_class'] = 'DataciteHarvester'
                metadata['source_pid'] = record
                metadata['provider'] = 'Datacite'
                metadata['preprocess'] = 'prov:corrected_keywords'
                ldo = LinkedDataObject(original=mdata, derived=mdata, patch_stack=[], metadata=metadata)
                ldo.serialize(destination=jsonld_filepath)
            else:  #just dump what was found
                with open(jsonld_filepath, 'w', encoding='utf-8') as fileo:
                    json.dump(mdata, fileo, indent=4, separators=(', ', ': '), sort_keys=True)
            successful_records.append(record)

    return successful_records, failed_records


class DataciteHarvester(Harvester):
    """This is the Harvester to crawl sitemap.xmls and extract metadata from resulting urls.

    the Urls can selected according to a given pattern.
    the main target metadata is json-LD which is schema.org conform
    """

    # for know we just allow these, others could be possible
    # i.e get all child and parent organizations also
    def __init__(self, outpath=Path('.'), **kwargs):
        if isinstance(outpath, str):
            outpath = Path(outpath)
        super().__init__(outpath=outpath, **kwargs)

    def get_roars(self):
        # sources is set on init from a provided or default config file
        return self.sources

    def run(self, centers: str = 'all', since=None, base_savepath: Optional[Path] = None, **kwargs):
        """Execute the harvester for a given center or all """
        fail = []
        if base_savepath is None:
            base_savepath = self.outpath
        if since is None:
            since = self.last_run

        roars = self.get_roars()
        if centers == 'all':
            for key, val in roars.items():
                print(f'Harvesting Center {key}')
                roar = val['roar']
                base_savepath1 = base_savepath / key
                suc, fai = harvest_roar(roar, base_savepath=base_savepath1, since=since)
                fail.extend(fai)
        else:
            roar = roars['center']['roar']
            base_savepath = base_savepath / roars['center']
            suc, fail = harvest_roar(roar, base_savepath=base_savepath, since=since)

        print(fail)

        self.set_last_run()
