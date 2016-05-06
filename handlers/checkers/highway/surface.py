from common.routines import composite_value
from handlers.simplehandler import SimpleHandler

_COMPOSITE_SURFACE = {
    'title': 'Составное значение покрытия дороги',
    'help_text': """Тег surface=* состоит из нескольких документированных покрытий.
Например: "asphalt;ground".

Желательно разбить дорогу на участки с однозначным типом покрытия.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:surface
""",
}

_UNDOC_SURFACE = {
    'title': 'Недокументированное значение покрытия дороги',
    'help_text': """Значение тега surface=* не задокументированно в wiki.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:surface
""",
}

_DOCUMENTED_VALUES = {
    # paved
    'paved', 'asphalt', 'cobblestone', 'cobblestone:flattened', 'sett', 'concrete', 'concrete:lanes',
    'concrete:plates', 'paving_stones', 'metal', 'wood',
    # unpaved
    'unpaved', 'compacted', 'dirt', 'earth', 'grass', 'grass_paver', 'gravel_turf', 'fine_gravel',
    'gravel', 'ground', 'ice', 'mud', 'pebblestone', 'salt', 'sand', 'snow', 'woodchips',
    # special
    'tartan', 'artificial_turf', 'decoturf', 'clay', 'metal_grid',
}


class HighwaySurfaceChecker(SimpleHandler):
    def __init__(self):
        self._undoc_surface = list()
        self._composite_surface = list()

    def process(self, obj):
        if obj['@type'] == 'way' and 'highway' in obj and 'surface' in obj:
            surface = obj['surface']
            if surface not in _DOCUMENTED_VALUES:
                if ';' in surface:
                    documented = True
                    items = composite_value(surface)
                    for item in items:
                        if item not in _DOCUMENTED_VALUES:
                            documented = False
                            break
                    if documented:
                        self._composite_surface.append(obj['@id'])
                    else:
                        self._undoc_surface.append(obj['@id'])
                else:
                    self._undoc_surface.append(obj['@id'])

    def finish(self, issues):
        issues.add_issue_type('warnings/highway/surface/undocumented_value', _UNDOC_SURFACE)
        for way_id in self._undoc_surface:
            issues.add_issue_obj('warnings/highway/surface/undocumented_value', 'way', way_id)
        issues.add_issue_type('todo/highway/surface/composite_value', _COMPOSITE_SURFACE)
        for way_id in self._composite_surface:
            issues.add_issue_obj('todo/highway/surface/composite_value', 'way', way_id)
