# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
'''
Mapping which maps to map openaire datasource sets to a dict compliant with the hmc repository schema

A fast way for jq command testing is https://jqplay.org/
A lot of examples can be found here: https://github.com/stedolan/jq/wiki/Cookbook#filter-objects-based-on-the-contents-of-a-key
'''
from typing import Dict
from typing import List


# HOW to track metadata not used...?
def check_unmapped_keys(mapping: Dict[str, str], full_keys: List[str]) -> List[str]:
    """Small helper function to check if a key is within a mapping string

    :param mapping: The jq mapping as a dict, where each value is a jq mapping string
    :type mapping: Dict[str, str]
    :param full_keys: Keys which may be present
    :type full_keys: List[str]
    :return: A list of unused keys
    :rtype: List[str]
    """
    unused_keys = []
    for key in full_keys:
        found = False
        for val in mapping.values():
            if key in val:
                found = True
                continue
        if not found:
            unused_keys.append(key)
    return unused_keys


MAP_OPENAIRE_SOURCE_HMC_REPO: Dict[str, str] = {
    'resourceName':
    r'[{"name": .officialname, "nameType": "name", "nameLanguage": null}, {"name": .englishname, "nameType": "translated name", "nameLanguage": "en"}]',
    'resourceDescription': r'.description',
    'repositoryType': r'[]',
    'repositoryLanguage': r'.languages',
    'identifier': r'[{"id": .originalId[], "identifierType": null}, {"id": .id, "identifierType": null}]',
    'databaseAccess': r'.accessrights',
    'documentationUri': r'.websiteurl',
    'helmholtzResearchField': r'[]',
    'keyword': r'.subjects',
    'providerType': r'[]',
    'resourceStatus': r'"valid"',
    'dataUploadType': r'[.uploadrights]',
    'offersEnhancedPublication': r'["unknown"]',
    'date': r'[]',
    'contentType': r'[]',
    'contact': r'[]'
}

# two letter ISO language codes mocked up by slicing the string to first 2 characters for now
# API requests currently provide schema 2.2 responses. This mapping therefore maps re3data v2.2
# additional identifiers and e.g. contentType key are part of re3data schema v3.1
# resourceStatus "active" is set as a default value for now
# will not validate without contactName in contact
# some optional keys from CCT1 schema might still be missing like api
# issue with too many quotes around string values not solved yet
#[{"name": .re3data.repository.repositoryName.content, "nameType": "name", "nameLanguage": .re3data.repository.repositoryName.language[0:2]}] + [.re3data.repository.additionalName[] | {"name": .content, "nameType": "alternative name", "nameLanguage": .language[0:2]}]
MAP_RE3DATA_HMC_REPO: Dict[str, str] = {
    'resourceName': # The same language problem here
    r'[{"name": .re3data.repository.repositoryName.content, "nameType": "name", "nameLanguage": .re3data.repository.repositoryName.language[0:2]}] + [.re3data.repository.additionalName as $a | if ($a | type) == "array" then ($a[]) elif $a == null then empty else ($a) end | {"name": .content , "nameLanguage": .language[0:2] , "nameType": "name"}]',
    'resourceDescription':
    r'.re3data.repository.description.content',
    'repositoryType':
    r'[.re3data.repository.type as $a | if $a == null then ("other") elif ($a | type) == "array" then ($a[]) else ($a) end | .]',
    'repositoryLanguage':
    r'[.re3data.repository.repositoryLanguage as $a | if ($a | type) == "array" then ($a[][0:2]) else ($a[0:2]) end] | ["sp","in","jp","ma","po"] as $a | del(.[] | select(. == $a[]))',
    # for now remove the false lang 2 onces, todo figure out right replacement ['sp' -> 'es'] maybe with "sub" like [.[] | ["sp","in","jp","ma","po"] as $a | sub($a; "es")]
    'identifier':
    r'[{"id": .re3data.repository."re3data.orgIdentifier", "identifierType": "re3data ID"}]',
    'databaseAccess':
    r'[.re3data.repository.databaseAccess.databaseAccessType]',
    'documentationUri':
    r'[.re3data.repository.missionStatementURL]',
    # 'helmholtzResearchField':
    # r'[]',
    'keyword':
    r'[.re3data.repository.keyword as $a | if ($a | type) == "array" then ($a[]) else ($a) end] + [.re3data.repository.subject as $b | if ($b | type) == "array" then ($b[]) else ($b) end | .content as $c | if $c == null then empty else ($c) end]',
    'providerType':
    r'[.re3data.repository.providerType as $b | if ($b | type) == "array" then ($b[]) else ($b) end | sub( "P"; " p")]',
    'resourceStatus':
    r'"valid"',
    'dataUploadType':
    r'[.re3data.repository.dataUpload as $b | if ($b | type) == "array" then ($b[]) else ($b) end | .dataUploadType as $c | if $c == null then empty else $c end]',
    'offersEnhancedPublication':
    r'[.re3data.repository.enhancedPublication]',
    'date':
    r'[{"resourceDate": .re3data.repository.entryDate, "dateType": "other"}] + [{"resourceDate": .re3data.repository.lastUpdate, "dateType": "modified"}]',
    # 'contentType':
    # r'[]',
    'contact':
    r'[.re3data.repository.repositoryContact as $b | if ($b | type) == "array" then ($b[]) else ($b) end | . as $d | if $d == null then empty else {"contactUri": .} end] + [.re3data.repository.institution as $a | if ($a | type)=="array" then ($a[]) else ($a) end | .institutionContact as $c | if ($c | type)=="array" then ($c[]) else ($c) end | . as $d | if $d == null then empty else {"contactUri": .} end] | unique'
}

MAP_OPENAIRE_DATASET_HMC_DATASET: Dict[str, str] = {
    'resourceName':
    r'.data.title as $a | [{"name": .maintitle, "nameType": "name", "nameLanguage": "en"}] | if $a == null then . else (. + [{"name": $a, "nameType": "name", "nameLanguage": "en"}]) end',
    'resourceDescription': r'[.description[]] | join(", ")',
    'identifier':  #[$b | {"id": $b.value, "identifierType": $b.scheme}])) else (. + [{"id": $b.value, "identifierType": $b.scheme}]) end
    r'.originalID as $a | .url as $c | .pid as $b | [($b[] | {"id": .value, "identifierType": (.scheme | if . == "doi" then "DOI" else . end)})] + [{"id": .id, "identifierType": "other"}] | if $a == null then . else (. + [{"id": $a, "identifierType": "other"}]) end | if $c == null then . else (. + [{"id": $c, "identifierType": "handle"}]) end',  #There are still some issues, for example .originalID can be a list also ...
    'documentationUri':
    r'.data.locations as $a | if $a == null then empty else [$a[].url] end + .data.uri as $b | if $b == null then empty else [$b] end',
    #"helmholtzResearchField": r'[]',
    'keyword': r'[.subjects[] | .subject.value]',
    'resourceStatus': r'"valid"',
    'date': r'[{"resourceDate": .publicationdate, "dateType": "start date"}]',
    'author':
    r'[.author[] | ({"fullname": .fullname} + if (.name == null or .name =="") then empty else {"name":.name} end + if (.surname == null or .surname =="") then empty else {"surname": .surname} end)]',  #.name as $a if $a == null then empty else ("name": .name)  end) |
    'dataType': r'.type',
    'contributor': r'.contributor',
    'publisher': r'.publisher',
    #'fairScore': r'',
    'country': r'.country[] | {"code": .code, "label": .label}',
    'accessRight': r'.bestaccessright',
    'size': r'.size',
    'tool': r'.tool',
    'source': r'.source',
    'geolocation': r'.geolocation',
    'dataFormat': r'.format',
    'relatedPublication': r'.relatedPublication'
}

MAP_OPENAIRE_ORG_HMC_ORG: Dict[str, str] = {}

# MSC URI mapping preliminary
# overall nameType values need to be adjusted to v1.0 enum values
# overall resourceStatus values need to be adjusted to v1.0 enum values
# overall check for missing keys (a couple are still missing here)
# pull helmholtzResearchField from KIT version of MSC? IDs do not match >100
# MSC bath catalog provides organizations, related entities, crosswalks as well
# pattern for MSCID: ^msc:(m|g|t|c|e|datatype|location|type|id_scheme)\d+$
# some metadata standard entities do contain keys others dont: like versions

# common properties CCT1 v1.0 (name & description are mandatory):
# resourceName (name, nameType, nameLanguage), repeatable, mandatory
# identifier (id, identifierType)
# resourceDescription, exactly 1, mandatory
# resourceURI
# documentationURI
# contact (contactName, contactidentifier, contactIdentifierSystem, contactURI, contactRole)
# keyword
# date (resourceDate, dateType)
# resourceStatus
# (relatedHelmholtzCentre) enum
# scientificDiscipline
# helmholtzResearchField

MAP_RDA_BATH_METADATASTANDARD_HMC_METADATASTANDARD: Dict[str, str] = {
    'resourceName':
    r'[{"name": .data.title, "nameType": "name", "nameLanguage": "en"}]',  # language is here hardcoded.... because this information is required but not there.
    'resourceDescription': r'.data.description as $a | if $a == null then ("Metadata standard") else $a end',
    'identifier': r'[{"id": .data.mscid, "identifierType": "MSC ID (Bath version)"}]',
    'documentationUri': r'[.data.locations as $a | if $a == null then empty else $a[].url end] + [.data.uri]',
    #"helmholtzResearchField": r'[]',
    #"keyword": r'[]',
    'resourceStatus': r'"valid"',
    # Input JSON contains multiple versions with dates issued. Mapping most recent to CCT1 schema.
    'date':
    r'.data.versions[-1].issued as $a | if $a == null then empty else ([{"resourceDate": $a, "dateType": "modified"}]) end',
    #"contact": r'[]',
    # most recent version number in versions array
    'metadataStandardVersion': r'.data.versions[-1].number as $a | if $a == null then empty else $a | tostring end'
    #"metadataStandardScope": r'[]'
}

# per hand https://opendatacommons.org/licenses/
# see https://opensource.org/licenses
## see also https://spdx.org/licenses/
# https://reuse.software/spec/
MAP_OPENSOURCE_LICENSE_HMC_LICENSE: Dict[str, str] = {
    'resourceName':
    r'[{"name": .name, "nameType": "name", "nameLanguage": "en"}, {"name": .id, "nameType": "abbreviation", "nameLanguage": "en"}]',
    'resourceDescription': r'.name',  # there is not a real description provided, could be parsed from te html urls?
    'identifier': r'[.identifiers[] | {"id": .identifier, "identifierType": .scheme}]',
    'documentationUri': r'[.links[] | .url]',
    'keyword': r'[.keywords[]]',
    'resourceStatus': r'"valid"',
    #'date': r'',
    #"contact": r'[]',
    'LicenseScope':
    r'["code"]',  # All are code but some are also for others things... Do not know how to get this from a set
    #"licenseJurisdiction": r'[]',
    'isMachineReadable':
    r'[.identifiers[] | .scheme ] | map( . == "DEP5") | any'  #not sure, there is a link to it, so yes. i do not know if a machine can do something with this, or only onces with DEP5 identifier?
    #"licenseVersion": r'[]' # could be parsed from the same of some.
}

# https://api.creativecommons.org/docs/readme_dev.html
MAP_CC_LICENSE_HMC_LICENSE: Dict[str, str] = {
    'resourceName':
    r'[.RDF.License.title[]  | select(.lang == "en" or .lang == "de") | {"name": .content, "nameType": "name", "nameLanguage": .lang}]',  # Often also links
    'resourceDescription':
    r'["A creative commons license, which description is found here: ", .RDF.License.about, .RDF.Description as $a | if ($a | type) == "array" then ($a[] | if .language == "en" then .about else empty end) elif $a == null then empty else ($a | if .language == "en" then .about else empty end) end] | join(" ")',
    # there is not a real description provided, could be parsed from te html urls?
    'identifier': r'[{"id": .RDF.License.identifier , "identifierType": "other"}]',
    'documentationUri':
    r'[.RDF.Description as $a | if ($a | type) == "array" then ($a[] | if .language == "en" then .about else empty end) elif $a == null then empty else ($a | if .language == "en" then .about else empty end) end]',
    #"keyword": r'[.keywords[]]',
    'resourceStatus': r'"valid"',
    'date': r'.RDF.license.hasVersion',
    #"contact": r'[]',
    'LicenseScope':
    r'["data", "text", "other"]',  # All are code but some are also for others things... Do not know how to get this from a set
    'licenseJurisdiction':
    r'.RDF.License.jurisdiction as $a | if ($a | type) == "array" then $a[] else ([$a]) end | map(.resource) | join(" ")',
    'isMachineReadable': r'true',
    'licenseVersion': r'.RDF.License.hasVersion'
}

MAP_ROR_HMC_ORGANIZATION: Dict[str, str] = {
    'resourceName':
    r'[{"name": .name, "nameType": "name", "nameLanguage": "en"}] + [.acronyms[] | {"name": ., "nameType": "abbreviation", "nameLanguage": "en"}]',
    'resourceDescription':
    r'([.wikipedia_url] + [.links as $a | if ($a | type) == "array" then $a[] else [$a] end]) | join(" ") | ltrimstr(" ")',
    'identifier':
    r'[{"id": .id , "identifierType": "ROR"}, {"id": .external_ids.GRID.preferred , "identifierType": "GRID"}]',  # There are many other identifiers to be parsed
    'documentationUri': r'[.wikipedia_url]',
    'keyword': r'.types',
    'resourceStatus': r'.status as $a | if $a =="active" then "valid" else "uncertain" end',
    'date':
    r'.established | tostring | . as $a | if $a == null then empty else [{"resourceDate": ., "dateType": "start date"}] end',
    'organizationType':
    r'["other"]',  #.types[] as $a | if $a == "Education" then "research institute" else $a end', # TODO need so solution for relace each matching string entry with somethin else from a list
    'geographicAreaServed': r'.country.country_code'
    #"contact": r'[]',
}
