# -*- coding: utf-8 -*-
"""
Field and Type conversions.

The intention here is that we can dispatch on either type or the
fieldname to be able to convert the given jsonld source data into a
set of attributes that will be indexed in solr.  There are several use
cases:

* extract a field from a typed dictionary: e.g. DataDownload, we want
to return the contentUrl field.
* Conditionally extract the data from a potentially complicated type:
e.g. Place. We're preferentially parsing geo, [lat/lon], and address
fields, and returning a rich set of data from the place.
* Returning a specific type for a field, and potentially parsing: e.g
startDate/endDate
* Renaming a field: e.g. rdf:name -> name

Dispatch conventions:

* Function names should match the graph field name or type value.
* Colons (:) in the name are replaced by double underscore (__)

Any method beginning with _ is internal.
"""
#pylint: disable=invalid-name
# the camel case names are needed, because they are directly connected to schema types
#pylint: disable=missing-function-docstring
import json
import math

import shapely.geometry
import shapely.wkt
from dateutil.parser import isoparse

from data_harvesting.indexer import regions
from data_harvesting.indexer.common import flatten
from data_harvesting.indexer.models import Att
from data_harvesting.indexer.test_utils import test_generation


class UnhandledFormatException(Exception):
    pass


class UnhandledDispatchException(Exception):
    pass


class IDCollisionError(Exception):
    pass


@test_generation
def _dispatch(_type, dic):
    try:
        mod = __import__('data_harvesting.indexer.conversions')
        return getattr(mod, _type.replace(':', '__'))(dic)
    except (KeyError, AttributeError) as exc:
        raise UnhandledDispatchException() from exc


###
#  Types
#
#  These types will be inlined as attributes on the enclosing
#  object. They are not saved as separate items in the index.
###


def _extractField(fieldName):
    def _extractor(dic):
        return Att('txt', dic[fieldName])

    return _extractor


ProgramMembership = _extractField('programName')
#Organization = _extract('url')
PropertyValue = _extractField('value')
DataDownload = _extractField('contentUrl')


def Place(dic):
    _formats = {'polygon': 'POLYGON ((%s))', 'point': 'POINT (%s)'}

    geo = dic.get('geo', None)
    if geo and geo.get('@type', None):
        return _dispatch(geo['@type'], geo)

    lat = dic.get('latitude', None)
    lon = dic.get('longitude', None)
    if lat is not None and lon is not None:
        return _geo('point', _formats['point'] % (f'{lon} {lat}'))

    address = dic.get('address', None)
    if address:
        return [Att('txt', address), Att('txt', regions.regionForAddress(address), 'region')]

    return None


def GeoShape(geo):
    _formats = {'polygon': 'POLYGON ((%s))', 'point': 'POINT (%s)'}

    for field, fmt in _formats.items():
        val = geo.get(field, None)
        if val:
            return _geo(field, fmt % val)
    raise UnhandledFormatException(f"Didn't handle {json.dumps(geo)} in GeoShape")


def CourseInstance(data):
    atts = [_dispatch(field, data.get(field, None)) for field in ('startDate', 'endDate')]
    if 'location' in data:
        loc = data['location']
        if loc.get('@type', None):
            try:
                atts.append(_dispatch(loc['@type'], loc))
            except UnhandledDispatchException:
                pass
    atts.append(Att('txt', data.get('name', data.get('description', ''))))
    return list(flatten(atts))


## Geometry processing
def _to_geojson(geo):
    return json.dumps(shapely.geometry.mapping(geo))


def _geo_polygon(feature):
    the_geom = shapely.wkt.loads(feature)
    (minx, miny, maxx, maxy) = the_geom.bounds
    if minx == -180 and maxx == 180:
        # solr can't handle this, returns org.locationtech.spatial4j.exception.InvalidShapeException: Invalid polygon, all points are coplanar
        the_geom = shapely.ops.clip_by_rect(the_geom, -179.99, -89.99, 180.0, 89.99)
        print('Detected invalid geometry -- +- 180 bounds. Reducing slightly')

    # the_geom.length is the perimeter, I want a characteristic length
    length = math.sqrt((maxx - minx)**2 + (maxy - miny)**2)
    if len(feature) > 200:
        print(f'Complicated feature: {the_geom.area}, {length}, {feature}')

    return [
        Att('geojson', _to_geojson(the_geom.representative_point()), 'point'),
        Att('geojson', _to_geojson(the_geom.simplify(0.1)), 'simple'),
        Att('geojson', _to_geojson(the_geom), 'geom'),
        Att('geom', the_geom.area, 'area'),
        Att('geom', length, 'length'),
        Att('the', the_geom.wkt, 'geom'),
    ]


def _geo_default(feature):
    the_geom = shapely.wkt.loads(feature)
    return [
        Att('the', feature, 'geom'),
        Att('geojson', _to_geojson(the_geom.representative_point()), 'point'),
        Att('geojson', _to_geojson(the_geom), 'geom'),
    ]


def _geo(featuretype, feature):
    """ Create the attributes for the geometric feature
    feature: wkt representation of the feature
    returns: list of attributes
    """

    _dispatch = {'polygon': _geo_polygon}

    atts = [
        Att('txt', regions.regionsForFeature(feature), 'region'),
        Att('geom', featuretype, 'type'),
        Att('has', True, 'geom')
    ]

    atts.extend(_dispatch.get(featuretype, _geo_default)(feature))

    return atts


###
#   Individual Fields
###


def _parseDate(field, dic):
    try:
        dtc = isoparse(dic)
        return [
            Att('dt', dic.isoformat(), field),
            Att('n', dic.year, field.replace('Date', 'Year')),
        ]
    except ValueError:
        return Att('txt', dic, field)


def _extractDate(field):
    def _extractor(dic):
        if isinstance(dic, str):
            return _parseDate(field, dic)
        dct = dic.get('date', None)
        if dct:
            return _parseDate(field, dct)
        return None

    return _extractor


endDate = _extractDate('endDate')
startDate = _extractDate('startDate')


def temporalCoverage(field):
    if field == 'null/null' or not '/' in field:
        return Att('txt', field, 'temporalCoverage')
    try:
        (start, end) = field.split('/')
        return list(
            flatten([_parseDate('startDate', start),
                     _parseDate('endDate', end),
                     Att('txt', field, 'temporalCoverage')])
        )

    except ValueError as exc:
        raise UnhandledFormatException(f"Didn't handle {field} in temporalCoverage") from exc


## Prov Fields
def prov__wasAttributedTo(data):
    if isinstance(data, str):
        return Att('id', data, 'provider')

    _id = data.get('@id', None)
    if not _id:
        return UnhandledFormatException(f"Didn't find @id in prov:wasAttributedto {data}")

    return [
        Att('id', _id, 'provider'),
        Att('txt', data.get('rdf:name', None), 'provider'),
    ]


def rdf__name(data):
    return Att(None, data, 'name')


def rdfs__seeAlso(data):
    return Att('txt', data, 'sameAs')
