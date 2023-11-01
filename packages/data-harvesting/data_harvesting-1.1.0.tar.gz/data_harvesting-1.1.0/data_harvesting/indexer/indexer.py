# -*- coding: utf-8 -*-
"""
This model contains the indexer

The purpose of the indexer is to transform the contents of a given jsonld file
into a predefined indexed version, which the schema of SOLR can use.
Also the indexer has utility to communicate with SOLR. For more details read the README.md

"""
import hashlib
import itertools
import json
import logging
import os
import shutil
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import progressbar
import requests

import data_harvesting.indexer.conversions
from data_harvesting.data_model import LinkedDataObject
from data_harvesting.indexer.common import flatten
from data_harvesting.indexer.conversions import UnhandledDispatchException
from data_harvesting.indexer.models import Att
from data_harvesting.indexer.test_utils import test_generation

#from pathos.multiprocessing import ProcessingPool as Pool  # because this uses different serializers beyond pickle
#from multiprocessing import Pool
#from multiprocessing import Value


class Indexer(object):
    """
    This is the Indexer

    It converts given jsonld documents, or unHIDE specific json documents, to index version of it,
    which can then be used by Apache SOLR. For more information read the README and docs.

    Example of what it does:

    The json-ld document:
    {
      "@context": {
        "@vocab": "https://schema.org/"
      },
      "@type": "ResearchProject",
      "@id": "https://edmerp.seadatanet.org/report/7985",
      "name": "The impact of Coccolithophorid blooms off western Ireland",
      "identifier": "7985",
      "alternateName": "N/A",
      "url": "https://edmerp.seadatanet.org/report/7985",
      "sameAs": "http://www.nuigalway.ie/microbiology/dr__john_w__patching.html",
      "description": "High concentrations or blooms of the coccolithophorid Emiliania huxleyi can significantly affect a region by acting as a source of organic sulfur (i.e. dimethyl sulfide) to the atmosphere and calcium carbonate to the sediments, and by altering the optical properties of the surface layer. Documenting the occurrence of blooms in time and space is therefore essential in characterizing the biogeochemical environment of a region. Furthermore, their distribution pattern can be employed to define the environmental conditions favorable for their occurrence. E. huxleyi blooms can be distinguished from most other conditions in visible satellite imagery by their milkly white to turquoise appearance. This project funded under the Environmental Change Institute aims to examine of these blooms off the west coast of Ireland.",
      "areaServed": "West Coordinate: -12 East Coordinate: -9 North Coordinate: 56 South Coordinate: 51",
      "parentOrganization": {
        "@type": "Organization",
        "url": "https://edmo.seadatanet.org/report/774"
      },
      "memberOf": [
        {
          "@type": "ProgramMembership",
          "programName": "European Directory of Marine Environmental Research Projects (EDMERP)"
        },
        {
          "@type": "Organization",
          "url": "https://edmo.seadatanet.org/report/774"
        }
      ]
    }


    Would index to this:

    {
      "id": "https://edmerp.seadatanet.org/report/7985",
      "type": "ResearchProject",
      "name": "The impact of Coccolithophorid blooms off western Ireland",
      "txt_identifier": [
        "7985"
      ],
      "txt_alternateName": [
        "N/A"
      ],
      "txt_url": [
        "https://edmerp.seadatanet.org/report/7985"
      ],
      "txt_sameAs": [
        "http://www.nuigalway.ie/microbiology/dr__john_w__patching.html"
      ],
      "description": "High concentrations or blooms of the coccolithophorid Emiliania huxleyi can significantly affect a region by acting as a source of organic sulfur (i.e. dimethyl sulfide) to the atmosphere and calcium carbonate to the sediments, and by altering the optical properties of the surface layer. Documenting the occurrence of blooms in time and space is therefore essential in characterizing the biogeochemical environment of a region. Furthermore, their distribution pattern can be employed to define the environmental conditions favorable for their occurrence. E. huxleyi blooms can be distinguished from most other conditions in visible satellite imagery by their milkly white to turquoise appearance. This project funded under the Environmental Change Institute aims to examine of these blooms off the west coast of Ireland.",
      "txt_areaServed": [
        "West Coordinate: -12 East Coordinate: -9 North Coordinate: 56 South Coordinate: 51"
      ],
      "txt_parentOrganization": [
        "https://edmo.seadatanet.org/report/774"
      ],
      "txt_memberOf": [
        "European Directory of Marine Environmental Research Projects (EDMERP)",
        "https://edmo.seadatanet.org/report/774"
      ],
      "keys": [
        "id",
        "type",
        "name",
        "txt_identifier",
        "txt_alternateName",
        "txt_url",
        "txt_sameAs",
        "description",
        "txt_areaServed",
        "txt_parentOrganization",
        "txt_memberOf"
      ],
      "json_source": "{\"@context\": {\"@vocab\": \"https://schema.org/\"}, \"@type\": \"ResearchProject\", \"@id\": \"https://edmerp.seadatanet.org/report/7985\", \"name\": \"The impact of Coccolithophorid blooms off western Ireland\", \"identifier\": \"7985\", \"alternateName\": \"N/A\", \"url\": \"https://edmerp.seadatanet.org/report/7985\", \"sameAs\": \"http://www.nuigalway.ie/microbiology/dr__john_w__patching.html\", \"description\": \"High concentrations or blooms of the coccolithophorid Emiliania huxleyi can significantly affect a region by acting as a source of organic sulfur (i.e. dimethyl sulfide) to the atmosphere and calcium carbonate to the sediments, and by altering the optical properties of the surface layer. Documenting the occurrence of blooms in time and space is therefore essential in characterizing the biogeochemical environment of a region. Furthermore, their distribution pattern can be employed to define the environmental conditions favorable for their occurrence. E. huxleyi blooms can be distinguished from most other conditions in visible satellite imagery by their milkly white to turquoise appearance. This project funded under the Environmental Change Institute aims to examine of these blooms off the west coast of Ireland.\", \"areaServed\": \"West Coordinate: -12 East Coordinate: -9 North Coordinate: 56 South Coordinate: 51\", \"parentOrganization\": {\"@type\": \"Organization\", \"url\": \"https://edmo.seadatanet.org/report/774\"}, \"memberOf\": [{\"@type\": \"ProgramMembership\", \"programName\": \"European Directory of Marine Environmental Research Projects (EDMERP)\"}, {\"@type\": \"Organization\", \"url\": \"https://edmo.seadatanet.org/report/774\"}]}",
      "index_id": "8c9e2611-7976-4267-bad4-1308714aec6e",
      "_version_": "1726272489341845504",
      "indexed_ts": "2022-03-03T10:02:16.204Z"
    }
    """

    version = '0.2.0'
    _config: dict
    conf_path: Optional[Path]

    def __init__(self, conf: Optional[Union[dict, Path]] = None, loglevel=logging.INFO):
        """
        Init the indexer with a given configuration as a default the indexer will look for
        an indexer.conf file
        """
        self.set_config(conf)
        self._session = requests.Session()
        self.last_indexed_data: list = []

        today = datetime.today().strftime('%Y-%m-%d')
        log_dir = self.config.get('LOG_DIR', '.')
        if not log_dir.exists():
            log_dir.mkdir(parents=True)

        logfile = log_dir / f'indexer_{today}.log'
        logging.basicConfig(
            filename=logfile,
            level=loglevel,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S'
        )
        logging.debug('Indexer Started')
        logging.debug('Running indexer version : %s', self.version)
        logging.debug('Using config file: %s', self.conf_path)
        logging.debug('Config dump:')
        logging.debug(self.config)

    @property
    def config(self) -> dict:
        """The configuration of the indexer, where to store or send the indexed files to.

        A simple dict containing:

        """
        return self._config

    def set_config(self, conf: Optional[Union[dict, Path]] = None):
        """Set config from dict, or Path or default indexer.conf file"""

        conf_path = None

        if conf is None:
            default_conf: Path = Path('.').resolve() / 'indexer.conf'
            if default_conf.is_file():
                conf = default_conf
                logging.debug('Using default indexer.conf file.')

        if isinstance(conf, Path):
            conf_path = conf

        self.conf_path = conf_path

        conf = conf or {}
        base_solr_url = os.environ.get('SOLR_URL', None)
        if base_solr_url is None:
            solr_url = None
            delete_url = None
            query_url = None
        else:
            solr_url = base_solr_url + '/update/json/docs'
            delete_url = base_solr_url + '/update'
            query_url = base_solr_url + '/select'

        data_dir_env = os.environ.get('DATA_DIR')
        if data_dir_env is None:
            data_dir = Path('.').resolve()  # / 'summoned'
        else:
            data_dir = Path(data_dir_env)
        base_dir = Path(data_dir)
        log_dir = base_dir / 'logs'
        except_dir = base_dir / 'exceptions'
        solr_params = {'commit': 'true'}

        base_config: dict = {
            'solr_url':
            solr_url,
            'delete_url':
            delete_url,
            'query_url':
            query_url,
            'DATA_DIR':
            data_dir,
            'BASE_DIR':
            base_dir,
            'EXCEPT_DIR':
            except_dir,
            'LOG_DIR':
            log_dir,
            'nthreads':
            8,
            'solr_params':
            solr_params,
            'ignore_keys': [],
            'entity_list': [
                'Person', 'Organization', 'Dataset', 'CreativeWork', 'SoftwareSourceCode', 'SoftwareApplication',
                'Book', 'Thesis', 'Article', 'DigitalDocument', 'ScholarlyArticle', 'Report', 'Course',
                'ResearchProject', 'DataCatalog'
            ]
        }

        if isinstance(conf, dict):
            base_config.update(conf)
        elif isinstance(conf, Path):
            with open(conf, 'r', encoding='utf-8') as fileo:
                conf_con = json.load(fileo)
                base_config.update(conf_con)
        else:
            raise ValueError('Config has to be either provided as a dict, or Path.')

        self._config = base_config

    def info(self):
        """Print some information about the indexer
        """
        print(f'Running indexer version : {self.version}')
        print(f'Using config file: {self.conf_path}')
        print('Config dump:')
        print(self.config)
        logging.info('Running indexer version : %s', self.version)
        logging.info('Using config file: %s', self.conf_path)
        logging.info('Config dump:')
        logging.info(self.config)

    def index_file(self, path: Union[Path, str], fl_reindex: bool = False, fail: bool = False, unhidedata=True):
        """Index a single file
        """
        base_dir = self.config['BASE_DIR']
        if isinstance(path, str):
            filename: str = path.strip()
            src = Path(base_dir) / path
        else:
            src = base_dir / path

        logging.info('Indexing file %s', src)
        # TODO this will be at some point replaced by reading from a ModelData class
        # also the read in should be with validation.

        if not src.is_file():
            msg = f'Source file path provided for indexing, does not exists or is not a file: {src}'
            if fail:
                raise ValueError(msg)
            logging.error(msg)
        # assume unhide data:
        uplifted = None
        if unhidedata:
            ldo = LinkedDataObject.from_filename(src)
            uplifted = ldo.derived
            orig = ldo.original
        # if it fails, load from json
        else:
            with open(src, 'rb') as fileo:
                try:
                    orig = json.load(fileo)
                except UnicodeDecodeError:
                    fileo.seek(0)
                    file_bytes = fileo.read()
                    try:
                        file_string = file_bytes.decode('latin1')
                        orig = json.loads(file_string)
                    except json.JSONDecodeError as msg:
                        logging.error(f'Issue decoding {filename}, continuing')
                        exp_path = self.config['EXCEPT_DIR'] / filename.split('/')[-1]
                        shutil.copy(src, exp_path)
                        return

        self.index_data(orig, fl_reindex=fl_reindex, fail=fail, uplifted=uplifted)

    def index_data(self, orig, fl_reindex: bool = False, fail: bool = False, uplifted=None):
        """
        Create an index, for a given piece of data and upload it to solr
        """
        ignore_keys = self.config.get('ignore_keys', [])
        entity_list = self.config.get('entity_list', None)
        res = extract_entity_dicts(orig, entity_list=entity_list, ignore_keys=ignore_keys)

        nent = len(res)
        logging.info(f'Found {nent} entities for indexing.')
        logging.debug(f'Identified the following entities for indexing: {res}')

        indexes = []
        for i, entry in enumerate(res):
            entry_index = generate_index_dict(entry, uplifted=uplifted)
            if entry_index is not None:
                indexes.append(entry_index)
            logging.debug(f'Index generated {i+1}/{nent}: {entry_index}')
            _id = entry.get('@id', entry.get('url', ''))
            #old, but now indexed several times:
            # #self.upsert(_id, entry_index, fl_reindex)

        # Is there a way to upload these in bulk to solr?
        for index_ in indexes:
            self.upload_data(index_, orig=orig)
            # check if already present in solr
            # if present strategy
            # upload to solr if not present
        self.last_indexed_data = indexes

    def solr_request_get(self, solr_url: Optional[str] = None, solr_parameters: Optional[dict] = None) -> dict:
        """
        Make a get request to solr, i.e all communication should go through this. i.e queries

        All error catching should happen here.
        """
        solr_params: dict = {
            'facet.limit': 1000,
            'q': '*:*',
            'facet.field': [
                'id',
            ],
            'sort': 'score desc, indexed_ts desc',
            'facet.mincount': '2',
            'rows': 0,
            'facet': 'true',
        }

        resp: dict = {}
        if solr_parameters is None:
            solr_parameters = solr_params

        solr_url = solr_url or self.config['query_url']
        logging.debug(f'Query Solr with: {solr_url}, {solr_parameters}.')
        resp = self._session.get(solr_url, params=solr_parameters).json()

        return resp

    def solr_request_post(
        self,
        data: dict,
        orig: Optional[dict] = None,
        solr_url: Optional[str] = None,
        solr_parameters: Optional[dict] = None
    ):
        """
        Make a post request to solr, i.e all upload communication should go through this.
        All the error catching happens here.

        data, dict: The payload
        orig, dict: The original larger data part, needed for meaningful stacktraces
        solr_url, str: The url the post requests goes to
        solr_parameters, dict: Parameters for the post request

        """
        solr_params = self.config['solr_params']
        if solr_parameters is None:
            solr_parameters = solr_params
        solr_url = solr_url or self.config['solr_url']
        logging.debug(f'Uploading to index: {data}.')
        solr_post = self._session.post(solr_url, params=solr_parameters, json=data)
        try:
            solr_post.raise_for_status()
            logging.info(f"Added resource {data['id']}: {data['type']} to index.")
        except requests.exceptions.HTTPError:
            trb = traceback.format_exc()
            logging.info(f"Failed to added resource {data['id']}: {data['type']} to index.")
            self.dump_exception(orig, solr_post.text, trb=trb)

    def solr_request_delete(self, idn: str):
        """
        Make a post delete request to solr, i.e all delete communication should go through this.
        All the error catching happens here.

        data, dict: The payload
        orig, dict: The original larger data part, needed for meaningful stacktraces
        solr_url, str: The url the post requests goes to
        solr_parameters, dict: Parameters for the post request

        """
        solr_params: dict = {'commit': 'true'}
        solr_url = self.config['delete_url']
        payload = {'delete': {'query': f'id:"{idn}"'}}
        logging.info(f'Delete resource {idn}: from index.')

        self._session.post(solr_url, params=solr_params, json=payload)

    def upload_data(self, data: dict, orig: Optional[dict] = None, overwrite=True):
        """Uploads a single data entry to solr,
        by first deleting if it exists already, i.e overwriting it.

        :param data: [description]
        :type data: [type]
        """
        if self.config['delete_url'] is None:
            return

        idn = data.get('id', None)
        idn = idn or data.get('@id', None)

        if idn is None:
            return

        # first check if the resource exists if yes get it.
        # depending on the strategy delete the old one, and replace with new.
        # or merge them together through a graph operation. (nested dict merge)

        # for now always replace with new data
        if overwrite:
            self.solr_request_delete(idn=data['id'])
            exists = False
        else:
            exists = False
            # exists = self.solr_request_existence(idn=data['id']) # TODO implement

        if not exists:
            solr_params = self.config['solr_params']
            self.solr_request_post(data=data, orig=orig, solr_url=self.config['solr_url'], solr_parameters=solr_params)
        #else:
        #    # get data in database, merge or only replace if new dict is larger.
        #    query_url = self.config['query_url']
        #    resp = self.solr_request_get(solr_url=query_url, solr_parameters=solr_params)
        #    data =

    def dump_exception(self, elt, err=None, trb=None):
        """Dump an exception and log the file"""
        trb = trb or ''
        logging.info('Dumping Exception.')
        try:
            if isinstance(elt, str):
                src = elt
            else:
                src = json.dumps(elt)
            filehash = hashlib.md5(src.encode('utf-8')).hexdigest()[:10]
        except TypeError as msg:  # There might be other exceptions here...
            logging.error(f'Exception dumping exception: {msg}')

        base_path = self.config['EXCEPT_DIR']

        if not base_path.exists():
            base_path.mkdir(parents=True)
        with open(base_path / (f'{filehash}.json'), 'w', encoding='utf-8') as fileo:
            fileo.write(src)
        if err:
            with open(base_path / (f'{filehash}.err.txt'), 'w', encoding='utf-8') as fileo:
                fileo.write(trb)
                fileo.write(err)

    def reindex_query(self, frq, chunk: int = 100, fail=False):
        """Reindex all results from a certain query

        :param frq: [description]
        :type frq: [type]
        :param chunk: [description], defaults to 100
        :type chunk: int, optional
        """
        start = 0
        count = -1
        solr_params = {
            'q': '*:*',
            'fl': 'id,json_source',
            'sort': 'id asc',  # this can't be the indexed timestamp
            'rows': chunk,
            'fq': frq,
        }
        query_url = self.config['query_url']
        while start == 0 or start < count:
            solr_params['start'] = start
            logging.info(f'indexing from {start} of {count}')
            resp = self.solr_request_get(solr_url=query_url, solr_parameters=solr_params)

            start += chunk
            if count == -1:
                count = resp['response']['numFound']

            for orig in resp['response']['docs']:
                orig_source = json.loads(orig['json_source'])
                self.index_data(orig_source)

    def reindex(self, url, fail=False):
        """Reindex a certain url

        :param url: [description]
        :type url: [type]
        """
        solr_params = {
            'q': '*:*',
            'fl': 'id,json_source',
            'start': '0',
            'sort': 'indexed_ts desc',
            'fq': [f'+id:"{url}"'],
            'rows': '1',
        }
        resp = self.solr_request_get(solr_url=self.config['query_url'], solr_parameters=solr_params)
        orig = resp['response']['docs'][0]

        orig_source = json.loads(orig['json_source'])
        self.index_data(orig_source)

    def fetch_dups(self):
        """
        Fetch the facet counts from solr
        """
        solr_params = {
            'facet.limit': 1000,
            'q': '*:*',
            'facet.field': [
                'id',
            ],
            'sort': 'score desc, indexed_ts desc',
            'facet.mincount': '2',
            'rows': 0,
            'facet': 'true',
        }
        resp = self.solr_request_get(solr_url=self.config['query_url'], solr_parameters=solr_params)

        return resp['facet_counts']['facet_fields']['id'][::2]

    def remove_dups(self):
        """Reindex the facet stats"""
        for url in self.fetch_dups():
            self.reindex(url)


# Helper functions


def index_dir(
    src_dir: Path,
    indexer: Indexer = Indexer(),
    ending: str = 'json',
    fl_reindex: bool = False,
    threads: Optional[int] = None,
    fail: bool = False,
    pbar: bool = True,
    unhidedata: bool = True
):
    """
    Index all files found in a certain directory and its sub directories.
    """
    config = indexer.config
    threads = threads or config.get('threads', 8)
    files = list(src_dir.glob(f'**/*.{ending}'))  # for millions of files, it would be nice to keep generator
    nfiles = len(files)
    print(nfiles)
    if pbar:
        prbar = progressbar.ProgressBar(
            max_value=nfiles, redirect_stdout=True
        )  #progressbar.UnknownLength, redirect_stdout=True)
    else:
        prbar = None
    if not src_dir.is_dir():
        msg = f'Source directory provided for indexing, does not exists or is not a directory: {src_dir}'
        if fail:
            raise ValueError(msg)
        logging.error(msg)
    '''
    #count = Value('i', 0)

    def calculate(func, args):
        return func(*args)

    def calculatestar(args):
        return caluclate(*args)


    def process_multi(arg, i, indexer, pbar, bar, fl_reindex, fail):
        """Helper function"""
        filep = arg#[1]
        #i = arg[0]
        if pbar:
            prbar.update(i)
        #   #logging.info(f'Indexing file {i}/{nf}: {filep}')
        indexer.index_file(filep, fl_reindex=fl_reindex, fail=fail)
    '''
    # parallel index creation
    # if can be very large: TODO: make this a generataor instead somehow
    #TASKS = [(process_multi, [filename, i, indexer, pbar, bar,  fl_reindex, fail]) for i, filename in enumerate(src_dir.glob(f'**/*.{ending}'))]

    #with Pool(threads) as poolt:
    #    imap_it = poolt.map(calculatestar, TASKS)

    # serial version
    for i, filep in enumerate(src_dir.glob(f'**/*.{ending}')):
        if pbar:
            prbar.update(i)
        indexer.index_file(filep, fl_reindex=fl_reindex, fail=fail, unhidedata=unhidedata)
    '''
    # Playround with other possibilities
    with Pool(threads) as poolt:
        poolt.map_async(process_multi, args)#src_dir.glob(f'**/*.{ending}'))
    poolt = Pool(threads)
    with Pool(threads) as poolt:
        result = poolt.map_async(process_multi, files)#src_dir.glob(f'**/*.{ending}'))
        while not result.ready():
            nready = nfiles - result._number_left
            if pbar:
                prbar.update(nready)
            else:
                print(nready)
    '''


def calculate(func, args):
    return func(*args)


# for parallel version of indexing
def calculatestar(args):
    # first argument has to be the callable functions
    return calculate(*args)


def process_multi(filep, i, indexer, pbar, prbar, fl_reindex, fail):
    """Helper function"""
    if pbar:
        prbar.update(i)
    indexer.index_file(filep, fl_reindex=fl_reindex, fail=fail)


@test_generation
def dispatch(_type, dic):
    """Generate index for special types"""
    try:
        return getattr(data_harvesting.indexer.conversions, _type.replace(':', '__'))(dic)
    except (KeyError, AttributeError) as exc:
        raise UnhandledDispatchException(f'On {_type}, {dic}') from exc


# new ones:


def extract_entity_dicts(
    data: Union[dict, List[dict]],
    entity_list: Optional[List] = None,
    ignore_keys: Optional[List] = None
) -> List[dict]:
    """
    From a given json ld dict (which can also be a list of dicts) extract all entities and their data relevant for indexing.

    this is currently bound to json-LD, could be generalized

    This is a recursive function!

    # TODO maybe make a return category sorted, or a dict of lists...
    # or a dict with identifiers and results
    # or use rdflib to do this instead?
    # This as to work maybe with an unhide data model
    # one would also need to do this for the uplifted data.
    """
    results: list = []
    if ignore_keys is None:
        ignore_keys = []

    if not data:  #empty
        return results

    # default entity list:
    if entity_list is None:
        entity_list = [
            'Person', 'Organization', 'Dataset', 'CreativeWork', 'SoftwareSourceCode', 'SoftwareApplication', 'Book',
            'Thesis', 'Article', 'DigitalDocument', 'ScholarlyArticle', 'Report', 'Course', 'ResearchProject',
            'DataCatalog'
        ]
        #['Person', 'Organization', 'Dataset', 'CreativeWork', 'SoftwareSourceCode', 'SoftwareApplication']

    def _single_dict(_data: dict):
        if _data.get('@type', None) in entity_list:
            results.append(_data)

        # Look for further entities in all subtypes.
        for key, val in _data.items():
            if key in ignore_keys:
                continue
            if isinstance(val, dict):
                _single_dict(val)  # !recursion
            elif isinstance(val, list):
                for entry in val:
                    if isinstance(entry, dict):
                        _single_dict(entry)  # !recursion
                continue

    # This part is since we allow for lists of dicts as inputs
    if isinstance(data, dict):
        _single_dict(data)
    else:  #List
        for data_e in data:
            if not data_e:
                continue
            if isinstance(data_e, dict):
                _single_dict(data_e)

    return results


def select_identifier(data: Union[Dict[str, Any], List[Any], str]) -> Optional[str]:
    """Rekursively choose an identifier from the given input.
    If a list is given or found in the process always the first element is taken
    """
    data2 = None
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        data1 = data.get('@id', data.get('identifier', data.get('sameAs', data.get('url', None))))
        if data1 is not None:
            data2 = select_identifier(data1)  # rekursion!
        else:  # This was needed for mypy to be happy
            data2 = data1
    elif isinstance(data, list):
        if len(data) > 0:
            data2 = select_identifier(data[0])  # rekursion!
    # This includes None
    return data2


def extract_dict(dic: dict, entity_list: Optional[List] = None):
    """Extract a the to index part, i.e. test fields from a given dictionary"""
    _type = dic.get('@type', None)
    _id = select_identifier(dic)  # there can be list of nested dicts and everything

    # default entity list:
    if entity_list is None:
        entity_list = [
            'Person', 'Organization', 'Dataset', 'CreativeWork', 'SoftwareSourceCode', 'SoftwareApplication', 'Book',
            'Thesis', 'Article', 'DigitalDocument', 'ScholarlyArticle', 'Report', 'Course', 'ResearchProject',
            'DataCatalog'
        ]

    if isinstance(_type, list):
        # If this should be valid schema, we will have to figure out how to deal with it, i.e which type take.
        # or all?
        logging.error(f'A list of types was found for {_id}: {_type}. This entry will be ignored')
        return {}

    if _type and len(dic.keys()) == 1:
        return {}  # rather None?
    try:
        if _type and not _type in entity_list:
            return dispatch(_type, dic)
    except (UnhandledDispatchException) as msg:
        logging.warning(f'UnhandledDispatchException: {msg}')

    if _id and _type not in {'PropertyValue'}:
        return [Att('id', _id), Att('txt', str(dic.get('name', dic.get('description', ''))))]
    member = dic.get('member', None)
    if member:
        return extract_dict(member)

    # Erroring if description is a number
    return Att('txt', str(dic.get('name', dic.get('description', ''))))


@test_generation(post=lambda x: x)
def generic_test(_type: Optional[str], orig: dict, e_id: Optional[str] = None):
    return generic_type_toatts(orig, e_id)


def generic_type_toatts(orig: dict, e_id: Optional[str] = None, entity_list: Optional[List] = None) -> dict:  #pylint: disable=too-many-statements
    #pylint: disable=too-many-branches
    """
     This is a generic entity -> solr atts table for json-ld structures.
    dictionary => dictionary

    * For items that are common, (name, type, description) we add them
      to the corresponding field.

    * For items with specific types (entities), we dispatch to type (entity) specific
      parsers, which return an Att or list of Atts

    * For text items, we add them directly, as txt_[field] = value

    * For dictionaries, we call out to extract the data from the
      dictionary. This may be single valued, or it may be multivalued,
      including creating and referencing other graph nodes.

    * For lists, we add all of the individual items, either extracted
      from dictionaries or a list of string.
    """
    # first we sort out data we do not want to index:

    if '@type' in orig.keys() and len(orig.keys()) == 1:
        return {}

    # default entity list:
    if entity_list is None:
        entity_list = [
            'Person', 'Organization', 'Dataset', 'CreativeWork', 'SoftwareSourceCode', 'SoftwareApplication', 'Book',
            'Thesis', 'Article', 'DigitalDocument', 'ScholarlyArticle', 'Report', 'Course', 'ResearchProject',
            'DataCatalog'
        ]

    # generate index_dict
    #_id = e_id or orig.get('@id', orig.get('identifier', orig.get('sameAs', orig.get('url', ''))))
    _id = e_id or select_identifier(orig)  # there can be list of nested dicts and everything
    try:
        #print('to_att')
        #print(_id)
        if not _id:
            name = orig.get('name', None)
            if name:
                _id = hashlib.md5(name.encode('utf-8')).hexdigest()
            else:
                _id = str(uuid.uuid4())
        d_type = orig.get('@type', None)
        #print(orig)
        data = [
            Att(None, _id, 'id'),
            Att(None, orig['@type'], 'type'),
        ]
    except KeyError as msg:
        logging.warning(f"Warning -- didn't get id or url and type in {orig}. Raising KeyError")
        #return
        #print(traceback.format_exc())
        raise msg
        #return

    for key, val in orig.items():
        if not val:
            continue
        if key in {'@id', '@type', '@context'}:
            continue
        if key in {'name', 'description'}:
            data.append(Att(None, val, key))
            continue
        if key not in entity_list:  # dispatch only for special keys
            try:
                # check by name
                att = dispatch(key, val)
                if isinstance(att, Att):
                    att.name = att.name or key
                    data.append(att)
                else:
                    data.extend(att)
                continue
            except UnhandledDispatchException:
                pass

        if isinstance(val, str):
            data.append(Att('txt', [val], key))
            continue
        if isinstance(val, list):
            if isinstance(val[0], str):
                data.append(Att('txt', val, key))
                continue
            if isinstance(val[0], dict):
                vals = []
                for elt in val:
                    res = extract_dict(elt)
                    if res:
                        vals.append(res)
                try:
                    vals = sorted(flatten(vals))  #extract_dict(elt) for elt in val))
                except TypeError as msg:
                    trb = traceback.format_exc()
                    #    dump_exception(orig, str(msg), trb=trb)
                    logging.error(str(msg))
                    continue
                # this should be sorted (prefix1, val), (prefix1, val2), (prefix2, val2)
                for prefix, val in itertools.groupby(vals, lambda x: x.prefix):
                    _val = [elt.value for elt in val if elt.value]
                    names = [elt.name for elt in val if elt.name]
                    if names:
                        name = name.pop()
                    else:
                        name = key
                    if _val:
                        data.append(Att(prefix, _val, name))

        if isinstance(val, dict):
            atts = extract_dict(val)
            if not atts:
                continue
            if not isinstance(atts, list):
                atts = [atts]
            for att in atts:
                if not att.value:
                    continue
                if not att.name:
                    att.name = key
            data.extend(atts)

    #old singlevalued version.
    # return {d.key:d.value for d in data if d.value}

    # Note that some things like provider can come from either provider or prov:wasAttributedTo,
    # so we can get lists of these things from multiple keys that need to be merged.
    ret = {}
    for dic in data:
        ### Complicated. Want either single string valued, or list of
        ### items, but some single string items can't be sent as a
        ### list. So we can't use a default dict, we have to iterate.
        if not dic.value:
            continue
        if dic.key not in ret:
            ret[dic.key] = dic.value
            continue
        ret[dic.key] = list(flatten([ret[dic.key], dic.value]))
    return ret


def generate_index_dict(
    orig: dict,
    uplifted: Optional[dict] = None,
    e_id: Optional[str] = None,
    entity: Optional[list] = None,
    recipe: Optional[dict] = None,
    fail: bool = False
) -> Optional[dict]:
    """For a given data dict, create an indexed version for solr. Since the index is different for certain entities.
    the recipe tells the functions what should go into the index.


    This is a generic entity -> solr atts table for json-ld structures.
    dictionary => dictionary

    * For items that are common, (name, type, description) we add them
      to the corresponding field.

    * For items with specific types (entities), we dispatch to type (entity) specific
      parsers, which return an Att or list of Atts

    * For text items, we add them directly, as txt_[field] = value

    * For dictionaries, we call out to extract the data from the
      dictionary. This may be single valued, or it may be multivalued,
      including creating and referencing other graph nodes.

    * For lists, we add all of the individual items, either extracted
      from dictionaries or a list of string.
    """
    data: Optional[dict] = None
    data = generic_test('generic', orig, e_id)
    #    data = generic_type_toatts(orig, e_id)
    if data is None:
        logging.debug('No index generated, returning')
        return None
    logging.debug(f'Index_one: Index generated: {data}')
    data['keys'] = list(data.keys())
    #    print (json.dumps(data, indent=2))
    data['json_source'] = json.dumps(orig)
    if uplifted is None:
        uplifted = orig  # FIXME for now
    data['json_uplifted'] = json.dumps(uplifted)

    return data
