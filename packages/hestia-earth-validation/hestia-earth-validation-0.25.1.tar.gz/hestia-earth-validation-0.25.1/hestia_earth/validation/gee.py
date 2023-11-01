import os
from functools import reduce
from hestia_earth.utils.tools import current_time_ms
from hestia_earth.schema import NodeType

from .log import logger

ENABLED = os.getenv('VALIDATE_SPATIAL', 'true') == 'true'
ENABLE_TYPES = [NodeType.SITE.value, NodeType.ORGANISATION.value]
MAX_AREA_SIZE = int(os.getenv('MAX_AREA_SIZE', '5000'))

_caching = {}
_RASTERS = [
    {
        'name': 'siteType',
        'collection': 'MODIS/006/MCD12Q1',
        'band_name': 'LC_Prop2',
        'year': '2019'
    }
]
_VECTORS = [
    {
        'name': f"region-{level}",
        'collection': f"users/hestiaplatform/gadm36_{level}",
        'fields': f"GID_{level}"
    } for level in range(0, 6)
]


def _caching_key(func_name: str, args: dict):
    return '-'.join([func_name, str(args)])


def _run_with_cache(func_name: str, args: dict, func):
    global _caching
    key = _caching_key(func_name, args)
    _caching[key] = _caching.get(key, func())
    return _caching[key]


def _node_key(node: dict): return '/'.join([node.get('type', node.get('@type')), node.get('id', node.get('@id'))])


def _cache_nodes(nodes: list):
    from hestia_earth.models.cache_sites import ParamType, _run_values

    now = current_time_ms()

    cached_nodes = _run_values([
        (n, 0) for n in nodes  # expecting tuple with area_size
    ], ParamType.COORDINATES, _RASTERS, _VECTORS)
    nodes_mapping = reduce(lambda prev, curr: prev | {_node_key(curr): curr}, cached_nodes, {})

    logger.info('Done caching in %sms', current_time_ms() - now)

    return [nodes_mapping.get(_node_key(n), n) for n in nodes]


def init_gee_by_nodes(nodes: list):
    # need to validate for non-aggregated Site or Oganisation with coordinates
    enabled_nodes = [
        n for n in nodes if all([
            n.get('@type', n.get('type')) in ENABLE_TYPES,
            not n.get('aggregated', False),
            'latitude' in n and 'longitude' in n
        ])
    ]
    should_init = len(enabled_nodes) > 0
    if should_init and ENABLED:
        try:
            from hestia_earth.earth_engine import init_gee
        except ImportError:
            logger.error("Run `pip install hestia_earth.earth_engine` to use geospatial validation")
        init_gee()
        return _cache_nodes(enabled_nodes)
    return nodes


def is_enabled():
    if ENABLED:
        try:
            from hestia_earth.earth_engine.version import VERSION
            logger.debug("Using earth_engine version %s", VERSION)
            return True
        except ImportError:
            logger.error("Run `pip install hestia_earth.earth_engine` to use geospatial validation")

    return False


def id_to_level(id: str): return id.count('.')


def get_cached_data(site: dict, key: str, year: int = None):
    from hestia_earth.models.geospatialDatabase.utils import _cached_value
    value = _cached_value(site, key)
    return value.get(str(year)) if year else value


def get_region_id(node: dict):
    level = id_to_level(node.get('region', node.get('country')).get('@id'))
    id = get_cached_data(node, f"region-{level}")
    return None if id is None else f"GADM-{id}"


def get_region_distance(gid: str, latitude: float, longitude: float):
    global _caching
    try:
        from hestia_earth.earth_engine.gadm import get_distance_to_coordinates
        return _run_with_cache('get_region_distance',
                               {'gid': gid, 'latitude': latitude, 'longitude': longitude},
                               round(get_distance_to_coordinates(gid, latitude=latitude, longitude=longitude) / 1000))
    except Exception:
        return None
