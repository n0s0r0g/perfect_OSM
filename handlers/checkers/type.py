from handlers.simplehandler import SimpleHandler

POINT = 'p'
LINE = 'l'
AREA = 'a'
RELATION = 'r'

_BAD_TYPE = {
    'title': 'Некорректный тип элемента',
    'help_text': 'Для данного тега, либо пары тег=значение в Wiki указаны другие типы данных (точка, линия, '
                 'полигон/мультиполигон/отношение).',
}

_TAGS = {
    'building': {POINT, AREA}, # TODO: wiki doesn't allow POINT on building=*; tracked in todo/building/is_node
    'landuse': {POINT, AREA}, # TODO: wiki doesn't allow POINT on industrial=*
    'entrance': {POINT},
    'amenity': {POINT, LINE, AREA, RELATION}, # TODO: wiki doesn't allow LINE on amenity=*
}

_TAG_VALUES = {
    'highway': {
        'motorway': {LINE},
        'trunk': {LINE},
        'primary': {LINE},
        'secondary': {LINE},
        'tertiary': {LINE},
        'unclassified': {LINE},
        'residential': {LINE},
        'service': {LINE, AREA},
        'motorway_link': {LINE},
        'trunk_link': {LINE},
        'primary_link': {LINE},
        'secondary_link': {LINE},
        'tertiary_link': {LINE},
        'living_street': {LINE},
        'pedestrian': {LINE, AREA},
        'track': {LINE},
        'bus_guideway': {LINE},
        'raceway': {LINE},
        'road': {LINE},
        'footway': {LINE},
        'bridleway': {LINE},
        'steps': {LINE},
        'path': {LINE},
        'cycleway': {LINE},
        'proposed': {LINE},
        'construction': {LINE},
        'bus_stop': {POINT},
        'crossing': {POINT},
        'elevator': {POINT},
        'emergency_access_point': {POINT},
        'escape': {POINT},
        'give_way': {POINT},
        'mini_roundabout': {POINT},
        'motorway_junction': {POINT},
        'passing_place': {POINT},
        'rest_area': {POINT, AREA},
        'speed_camera': {POINT},
        'street_lamp': {POINT},
        'services': {POINT, AREA},
        'stop': {POINT},
        'traffic_signals': {POINT},
        'turning_circle': {POINT},
    },
    'natural': {
        'wood': {POINT, AREA},
        'tree_row': {LINE},
        'tree': {POINT},
        'scrub': {POINT, AREA},
        'heath': {POINT, AREA},
        'moor': {POINT, AREA},
        'grassland': {AREA},
        'fell': {POINT, AREA},
        'bare_rock': {AREA},
        'scree': {POINT, AREA},
        'shingle': {POINT, AREA},
        'sand': {POINT, AREA},
        'mud': {POINT, AREA},
        'water': {POINT, AREA},
        'wetland': {POINT, AREA},
        'glacier': {POINT, AREA},
        'bay': {POINT, AREA},
        'beach': {POINT, AREA},
        'coastline': {LINE},
        'spring': {POINT},
        'hot_spring': {POINT},
        'geyser': {POINT},
        'peak': {POINT},
        'volcano': {POINT},
        'valley': {POINT, LINE},
        'river_terrace': {POINT, LINE},
        'ridge': {LINE},
        'arete': {LINE},
        'cliff': {POINT, LINE, AREA},
        'saddle': {POINT},
        'rock': {POINT, AREA},
        'stone': {POINT},
        'sinkhole': {POINT, AREA},
        'cave_entrance': {POINT},
    },
    'waterway': {
        'river': {LINE, RELATION}, # TODO: relation: type=waterway - document in Wiki
        'riverbank': {AREA},
        'stream': {LINE, RELATION}, # TODO: relation: type=waterway - document in Wiki
        'canal': {LINE, RELATION},  # TODO: relation: type=waterway - document in Wiki
        'drain': {LINE, RELATION},  # TODO: relation: type=waterway - document in Wiki
        'ditch': {LINE, RELATION},  # TODO: relation: type=waterway - document in Wiki
        'dock': {POINT, AREA},
        'boatyard': {POINT, AREA},
        'dam': {LINE, AREA},
        'weir': {POINT, LINE},
        'waterfall': {POINT},
        'lock_gate': {POINT},
        'turning_point': {POINT},
        'water_point': {POINT},
    }
}


def _is_point(obj):
    return obj['@type'] == 'node'


def _is_line(obj):
    if obj['@type'] == 'way':
        return True
    return False


def _is_area(obj):
    if obj['@type'] == 'way':
        return obj['@nodes'][0] == obj['@nodes'][-1]
    elif obj['@type'] == 'relation':
        if obj.get('type') == 'multipolygon':
            return True
    return False


def _is_relation(obj):
    if obj['@type'] == 'relation':
        return True
    return False


class TypeChecker(SimpleHandler):
    def __init__(self):
        self._bad_type = []

    def process(self, obj):
        allowed_type = {POINT, LINE, AREA, RELATION}
        for k, v in obj.items():
            if k.startswith('@'):
                continue
            if k in _TAGS:
                allowed_type = allowed_type.intersection(_TAGS[k])
            if k in _TAG_VALUES and v in _TAG_VALUES[k]:
                allowed_type = allowed_type.intersection(_TAG_VALUES[k][v])

        valid = False
        if POINT in allowed_type and _is_point(obj):
            valid = True
        if not valid and LINE in allowed_type and _is_line(obj):
            valid = True
        if not valid and AREA in allowed_type and _is_area(obj):
            valid = True
        if not valid and RELATION in allowed_type and _is_relation(obj):
            valid = True

        if not valid:
            self._bad_type.append((obj['@type'], obj['@id']))

    def finish(self, issues):
        issues.add_issue_type('warnings/bad_type', _BAD_TYPE)
        for obj_type, obj_id in self._bad_type:
            issues.add_issue_obj('warnings/bad_type', obj_type, obj_id)
