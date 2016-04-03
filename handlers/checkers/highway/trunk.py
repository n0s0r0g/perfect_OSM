from handlers.simplehandler import SimpleHandler
from routines.output import save_ways

_TRUNK_NO_MAXSPEED = """На трассе (highway=trunk) не указан maxspeed.

Что нужно сделать:
1. Выяснить, какое ограничение скорости на данном участке трассы (явное - знак ограничения скорости, либо неявное)
2. Добавить тег maxspeed с ограничением

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dtrunk
- http://wiki.openstreetmap.org/wiki/RU:Key:maxspeed

Список найденных трасс (highway=trunk): ways.txt
"""

_TRUNK_NO_LIT = """На трассе (highway=trunk) не указано наличие освещения (lit=*).

Что нужно сделать:
1. Выяснить, освещается ли данный участок трассы.
2. Добавить тег lit

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dtrunk
- http://wiki.openstreetmap.org/wiki/Key:lit

Список найденных трасс (highway=trunk): ways.txt
"""

_TRUNK_NO_LANES = """На трассе (highway=trunk) не указано количество полос (lanes=*).

Что нужно сделать:
1. Выяснить, сколько полос на данном участке трассы.
2. Добавить тег lanes

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:lanes
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dtrunk

Список найденных участков трасс (highway=trunk): ways.txt
"""


class HighwayTrunkChecker(SimpleHandler):
    def __init__(self):
        self._no_maxspeed = set()
        self._no_lit = set()
        self._no_lanes = set()

    def process(self, item):
        if item['tag'] == 'way' and 'highway' in item and item['highway'] == 'trunk':
            if 'maxspeed' not in item:
                self._no_maxspeed.add(item['id'])
            if 'lit' not in item:
                self._no_lit.add(item['id'])
            if 'lanes' not in item:
                self._no_lanes.add(item['id'])

    def finish(self, output_dir):
        save_ways(output_dir + 'todo/highway/trunk/no_maxspeed/', self._no_maxspeed, _TRUNK_NO_MAXSPEED)
        save_ways(output_dir + 'todo/highway/trunk/no_lanes/', self._no_lanes, _TRUNK_NO_LANES)
        save_ways(output_dir + 'todo/highway/trunk/no_lit/', self._no_lit, _TRUNK_NO_LIT)
