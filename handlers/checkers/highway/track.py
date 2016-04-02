import os

from handlers.simplehandler import SimpleHandler

_NO_SURFACE = """Для highway=track не задано покрытие (surface).

Объективные параметры:
- surface - тип покрытия

Субьективные параметры:
- surface:grade - оценка качества относительно типа покрытия (0..3)
- smoothness - абсолютное качество покрытия
- maxspeed:practical - скорость легкового автомобиля, с которой комфортно ехать
- tracktype

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dtrack
- http://wiki.openstreetmap.org/wiki/RU:Key:surface
- http://wiki.openstreetmap.org/wiki/RU:Proposed_features/Surface_Quality
- http://wiki.openstreetmap.org/wiki/User:Danidin9/Variants_of_smooth_surfaces

Список найденных дорог (highway=track): ways.txt
"""


class HighwayTrackChecker(SimpleHandler):
    def __init__(self):
        self._no_surface = set()

    def process(self, item):
        if item['tag'] == 'way' and 'highway' in item and item['highway'] == 'track':
            if not 'surface' in item:
                self._no_surface.add(item['id'])

    def finish(self, output_dir):
        if self._no_surface:
            fn = output_dir + 'todo/highway/track/no_surface/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_NO_SURFACE)
            fn = output_dir + 'todo/highway/track/no_surface/ways.txt'
            with open(fn, 'wt') as f:
                for way_id in self._no_surface:
                    f.write('https://www.openstreetmap.org/way/%d\n' % (way_id,))