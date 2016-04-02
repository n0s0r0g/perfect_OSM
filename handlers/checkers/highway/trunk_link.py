import os

from handlers.simplehandler import SimpleHandler

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
        if self._no_oneway:
            fn = output_dir + 'warnings/highway/trunk_link/no_oneway/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_TRUNK_LINK_NO_ONEWAY)

            fn = output_dir + 'warnings/highway/trunk_link/no_oneway/ways.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for way_id in self._no_oneway:
                    f.write('https://www.openstreetmap.org/way/%d\n' % (way_id,))
