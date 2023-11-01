# -*- coding: utf-8 -*-
"""
A dict containing identifier namespaces.
description_url: Should contain a link where the identifier namespace is described, e.g https://registry.identifiers.org/registry/doi
resolving_url: The base_link where the identifier need to be appended for being resolved properly e.g. https://doi.org/
"""

IDENTIFIER_NAMESPACE = {
    'ark': {
        'description_url': 'https://registry.identifiers.org/registry/ark',
        'resolving_url': 'https://n2t.net/ark:',
    },
    'arxiv': {
        'description_url': 'https://registry.identifiers.org/registry/arxiv',
        'resolving_url': 'https://arxiv.org/abs/',
    },
    'doi': {
        'description_url': 'https://registry.identifiers.org/registry/doi',
        'resolving_url': 'https://doi.org/',
    },
    'hdl': {
        'description_url': 'https://www.handle.net/index.html',
        'resolving_url': 'https://hdl.handle.net/',
    },
    'isbn': {
        'description_url': 'https://registry.identifiers.org/registry/isbn',
        'resolving_url': 'https://www.worldcat.org/isbn/',
    },
    'issn': {
        'description_url': 'https://registry.identifiers.org/registry/issn',
        'resolving_url': 'https://portal.issn.org/resource/ISSN/',
    },
    'nbn': {
        'description_url': 'https://registry.identifiers.org/registry/nbn',
        'resolving_url': 'https://nbn-resolving.org/resolver?verb=redirect&identifier=',
    },
    'pmid': {
        'description_url': 'https://registry.identifiers.org/registry/pubmed',
        'resolving_url': 'https://www.ncbi.nlm.nih.gov/pubmed/',
    },
    'purl': {
        'description_url': 'https://purl.archive.org/',
        'resolving_url': 'https://purl.archive.org/',
    },
    'urn': {
        'description_url': 'https://de.wikipedia.org/wiki/Uniform_Resource_Name',
        'resolving_url': '',
    },
    'wos': {
        'description_url': 'https://registry.identifiers.org/registry/wos',
        'resolving_url': 'https://www.webofscience.com/wos/woscc/full-record/',
    },
}

# Following https://wiki.surfnet.nl/display/standards/info-eu-repo/#infoeurepo-Publicationtypes we need to
# add http://purl.org/ as a prefix to the authoritative term if it's a string starting with info:eu-repo
# but purl.org is hosted now by internet archive… should we change to https://purl.archive.org/ instead?
PURL_PREFIX = 'http://purl.org/'
