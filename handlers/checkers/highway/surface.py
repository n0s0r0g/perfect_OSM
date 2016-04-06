from handlers.simplehandler import SimpleHandler
from routines.output import save_ways

_COMPLEX_SURFACE = """Тег surface=* состоит из нескольких документированных покрытий.
Например: "asphalt;ground".

Желательно разбить дорогу на участки с однозначным типом покрытия.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:surface
"""

_UNDOC_SURFACE = """Значение тега surface=* не задокументированно в wiki.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:surface
"""

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
        self._complex_surface = list()

    def process(self, obj):
        if obj['@type'] == 'way' and 'highway' in obj and 'surface' in obj:
            surface = obj['surface']
            if surface not in _DOCUMENTED_VALUES:
                if ';' in surface:
                    documented = True
                    for surface_part in surface.split(';'):
                        surface_part = surface_part.strip('\n\r\t ')
                        if surface_part not in _DOCUMENTED_VALUES:
                            documented = False
                            break
                    if documented:
                        self._complex_surface.append(obj['@id'])
                    else:
                        self._undoc_surface.append(obj['@id'])
                else:
                    self._undoc_surface.append(obj['@id'])

    def finish(self, output_dir):
        save_ways(output_dir + 'warnings/highway/undocumented_surface/', self._undoc_surface, _COMPLEX_SURFACE)
        save_ways(output_dir + 'todo/highway/complex_surface/', self._complex_surface, _COMPLEX_SURFACE)
