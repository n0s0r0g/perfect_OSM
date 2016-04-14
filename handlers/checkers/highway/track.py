from handlers.simplehandler import SimpleHandler

_NO_SURFACE = {
    'title': 'Не указано покрытие дороги',
    'help_text': """Для highway=track не задано покрытие (surface).

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
""",
}


class HighwayTrackChecker(SimpleHandler):
    def __init__(self):
        self._no_surface = set()

    def process(self, obj):
        if obj.get('highway') == 'track' and obj['@type'] == 'way':
            if not 'surface' in obj:
                self._no_surface.add(obj['@id'])

    def finish(self, issues):
        issues.add_issue_type('todo/highway/track/no_surface', _NO_SURFACE)
        for way_id in self._no_surface:
            issues.add_issue_obj('todo/highway/track/no_surface', 'way', way_id)
