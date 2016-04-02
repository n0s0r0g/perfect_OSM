import os

from handlers.simplehandler import SimpleHandler

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


class HighwayTrunkChecker(SimpleHandler):
    def __init__(self):
        self._no_maxspeed = set()
        self._no_lit = set()

    def process(self, item):
        if item['tag'] == 'way' and 'highway' in item and item['highway'] == 'trunk':
            if 'maxspeed' not in item:
                self._no_maxspeed.add(item['id'])
            if 'lit' not in item:
                self._no_lit.add(item['id'])

    def finish(self, output_dir):
        if self._no_maxspeed:
            fn = output_dir + 'todo/highway/trunk/no_maxspeed/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_TRUNK_NO_MAXSPEED)

            fn = output_dir + 'todo/highway/trunk/no_maxspeed/ways.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for way_id in self._no_maxspeed:
                    f.write('https://www.openstreetmap.org/way/%d\n' % (way_id,))

        if self._no_lit:
            fn = output_dir + 'todo/highway/trunk/no_lit/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_TRUNK_NO_LIT)

            fn = output_dir + 'todo/highway/trunk/no_lit/ways.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for way_id in self._no_lit:
                    f.write('https://www.openstreetmap.org/way/%d\n' % (way_id,))
