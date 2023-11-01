# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""This module contains the pipeline to harvest jsonld data over sitemaps of websites,
similar to what the gleaner software does in the OIH project
"""
import binascii
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional

import advertools as adv
import extruct
import pandas as pd
import progressbar
import requests
from w3lib.html import get_base_url

from data_harvesting.base_harvester import Harvester
from data_harvesting.data_model import derive_metadata
from data_harvesting.data_model import LinkedDataObject
#import base64


def get_all_sitemaps(url: str) -> pd.DataFrame:
    """From the top sitemap url get all sub urls and parse"""
    sitemap_df = adv.sitemap_to_df(url)
    return sitemap_df


def filter_urls(
    sitemap_df: pd.DataFrame,
    since: Optional[datetime] = None,
    match_pattern: Optional[str] = None,
    antimatch_pattern: Optional[str] = None
) -> pd.DataFrame:
    """Return a list of urls from a given sitemap tree which have been updated since and which optional match a certain pattern

    :param since: str Date
    :param match_pattern: str, regular expression
    """
    sub_df = sitemap_df
    #print(sub_df['loc'][:10])
    if match_pattern is not None:
        #mask = sub_df['loc'].str.contains(match_pattern, case=False, na=False, regex=False)
        mask = [bool(re.match(match_pattern, url)) for url in sub_df['loc']]
        sub_df = sub_df[mask]

    if antimatch_pattern is not None:
        # this does not work yet...
        #sub_df = sub_df[~sub_df['loc'].str.contains(antimatch_pattern, case=False, na=False, regex=False)]
        mask = [not bool(re.match(antimatch_pattern, url)) for url in sub_df['loc']]
        sub_df = sub_df[mask]

    if since is not None:
        #now = date.today()  #now()
        #sub_df = sub_df.between_time(since, now) # this takes only time

        # the dt.date is needed otherwise the timestamp comparison does not work
        sub_df['lastmod_date'] = pd.to_datetime(sub_df['lastmod']).dt.date
        sub_df = sub_df[sub_df['lastmod_date'] > pd.Timestamp(since)]

        # if this is turns out to slow, set date the index and do
        # df.loc[start_date:end_date] instead
    return sub_df


def extract_metadata_url(
    url: str, syntaxes: Optional[List[str]] = None
) -> dict:  #, 'microdata', 'opengraph', 'rdfa']):
    """
    # TODO add other format which extruct does not manage
    """
    data: dict = {}
    if syntaxes is None:
        syntaxes = ['dublincore', 'json-ld']

    try:
        req = requests.get(url, timeout=(10, 100))
    except requests.exceptions.ChunkedEncodingError as ex:
        print(f'Invalid chunk encoding {str(ex)}')
        return {syn: [] for syn in syntaxes}
    base_url = get_base_url(req.text, req.url)
    try:
        data = extruct.extract(req.text, syntaxes=syntaxes, base_url=base_url)  #base_rul=base_url,
    except json.JSONDecodeError as err:
        print(f'Could not extract metadata from {url}. {str(err)}')
        return {}

    if len(data.get('json-ld', [])) == 0:
        try:
            req_json = req.json()
        except json.JSONDecodeError as err:  # requests.exceptions.JSONDecodeError as err:
            return data
        if '@context' in req_json.keys():
            #we assume it is json-ld
            data['json-ld'] = [req_json]

    return data


def transform_url(urls: List[str], url_transforms: Optional[List] = None) -> List[str]:
    """
    Apply given transformation to a url

    currently mainly 'str replace'
    maybe there are better packages to do such things also more general

    for example
    urls_should = ['https://data.fz-juelich.de/api/datasets/export?exporter=schema.org&persistentId=doi:10.26165/JUELICH-DATA/VGEHRD']

    urls = ['https://data.fz-juelich.de/dataset.xhtml?persistentId=doi:10.26165/JUELICH-DATA/VGEHRD']
    transforms = [{'replace' : ('dataset.xhtml?', 'api/datasets/export?exporter=schema.org&')]

    """
    if url_transforms is None:
        url_transforms = []

    new_urls = []
    for url in urls:
        new_url = url
        for transform in url_transforms:
            for key, val in transform.items():
                if key == 'replace':
                    new_url = new_url.replace(val[0], val[1])
        new_urls.append(new_url)

    return new_urls


def harvest_sitemap(
    sitemap: str,
    since: Optional[datetime] = None,
    match_pattern: Optional[str] = r'*/record/\d',  # r ?
    base_savepath: Optional[Path] = None,
    url_transforms: Optional[List[dict]] = None,
    antimatch_pattern: Optional[str] = None,
    skip_existing: Optional[bool] = False,
    unhidedata: bool = False
):  #, formats=['jsonld']):
    """
    For each url in a sitemap try to extract some metadata of a specified format through different means

    updated since then.
    """
    failed_records = []
    successful_records = []
    sitemap_df = get_all_sitemaps(sitemap)
    record_urls_df = filter_urls(sitemap_df, since=since, match_pattern=match_pattern)
    #print(record_urls_df.keys())
    record_urls = transform_url(record_urls_df['loc'], url_transforms=url_transforms)
    if base_savepath is None:
        base_savepath = Path('.')

    nurls = len(record_urls)
    print(f'Harvesting {nurls} record urls')
    with progressbar.ProgressBar(max_value=nurls) as pbar:
        for i, record in enumerate(record_urls):
            pbar.update(i)
            # we want to zuse the url as filename, but the / make problems. : also
            # the best solution so far it to encode the url using base64,
            # it can be decoded back with base64.b64decode(filename)
            # binasci.unhexify(filename) (without.json)
            # or https://stackoverflow.com/questions/27253530/save-url-as-a-file-name-in-python
            #filename = f"{record.replace('/', ':')}.json"
            #filename = str(base64.b64encode(record.encode('utf-8')).decode() + ".json")
            filename = binascii.hexlify(record.encode('utf-8')).decode() + '.json'
            #print(filename)
            jsonld_filepath: Path = base_savepath / filename
            if jsonld_filepath.exists() and skip_existing:
                successful_records.append(record)
                continue
            mdata = extract_metadata_url(record)
            time.sleep(0.1)
            jsonld_md = mdata.get('json-ld', [])
            # if this failed, try to download, json directly
            if len(jsonld_md) == 0:
                print(f'Failed, to retrive jsonld {record}')
                failed_records.append(record)
                continue

            # Do some basic checks on json-lD

            # store file
            # add some metadata to file
            #jsonld_filepath.write_text(json.dumps(jsonld_md, indent=4))
            #print(jsonld_md)
            if unhidedata:
                metadata = derive_metadata()
                metadata['harvester_class'] = 'SitemapHarvester'
                metadata['source_pid'] = record
                metadata['sitemap'] = sitemap
                ldo = LinkedDataObject(original=jsonld_md[0], derived=jsonld_md[0], patch_stack=[], metadata=metadata)
                ldo.serialize(destination=jsonld_filepath)
            else:
                with open(jsonld_filepath, 'w', encoding='utf-8') as fileo:
                    json.dump(jsonld_md[0], fileo, indent=4, separators=(', ', ': '), sort_keys=True)
            successful_records.append(record)

    return successful_records, failed_records


# Todo Lock the URL harvested into a file


class SitemapHarvester(Harvester):
    """This is the Harvester to crawl sitemap.xmls and extract metadata from resulting urls.

    the Urls can selected according to a given pattern.
    the main target metadata is json-LD which is schema.org conform
    """
    # read in sitempas which are included in the Knowledgegraph
    kg_sitemaps: List['str'] = []

    def __init__(self, outpath=Path('.'), **kwargs):
        """Initialize a Harvester instance"""
        if isinstance(outpath, str):
            outpath = Path(outpath)

        super().__init__(outpath=outpath, **kwargs)

    def get_sitemaps(self):
        """Return the sitemap list, which are the sources in this case"""
        return self.sources

    def run(
        self,
        sitemap='all',
        since=None,
        base_savepath=None,
        match_pattern=None,
        antimatch_pattern=None,
        url_transforms=None,
        **kwargs
    ):
        """Execute the harvester for a given sitemap or all """

        if base_savepath is None:
            base_savepath = self.outpath

        if since is None:
            since = self.last_run

        sitemaps_r = self.get_sitemaps()
        failed_records = []

        if sitemap == 'all':
            for sitem in sitemaps_r:
                # since the patters and transforms possible differ for each sitemap, we get them from a
                # predefinded table/json (in the future should be in sources.csv table)
                successful_records, failed_records = harvest_sitemap(
                    sitem,
                    since=since,
                    base_savepath=base_savepath,
                    match_pattern=match_pattern,
                    antimatch_pattern=antimatch_pattern,
                    url_transforms=url_transforms,
                    unhidedata=True
                )
        else:
            successful_records, failed_records = harvest_sitemap(
                sitemap,
                since=since,
                base_savepath=base_savepath,
                match_pattern=match_pattern,
                antimatch_pattern=antimatch_pattern,
                url_transforms=url_transforms,
                skip_existing=True,
                unhidedata=True
            )
        # todo log these:
        print(failed_records)

        self.set_last_run()


#url = 'https://juser.fz-juelich.de/sitemap-index.xml'

#sitemap = get_all_sitemaps(url)
#records = filter_urls(sitemap, match_pattern="*/record/\d")

#print(sitemap)

# sh = SitemapHarvester()
# sh.run(sitemap=url)
