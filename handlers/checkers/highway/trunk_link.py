from handlers.simplehandler import SimpleHandler
from routines.output import save_ways

_TRUNK_LINK_NO_ONEWAY = """Для вьезда/сьезда с трассы (highway=trunk_link) не задан тег oneway.
Для избежания неоднозначности, рекомендуется всегда добавлять тег oneway=*.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:highway

Список найденных вьездов/сьездов (highway=trunk_link): ways.txt
"""


class HighwayTrunkLinkChecker(SimpleHandler):
    def __init__(self):
        self._no_oneway = set()

    def process(self, item):
        if item['tag'] == 'way' and 'highway' in item and item['highway'] == 'trunk_link':
            if 'oneway' not in item:
                self._no_oneway.add(item['id'])

    def finish(self, output_dir):
        save_ways(output_dir + 'warnings/highway/trunk_link/no_oneway/', self._no_oneway, _TRUNK_LINK_NO_ONEWAY)
