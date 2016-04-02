import os

from handlers.handler import Handler

_HIGHWAY_ROAD_TAGS = {'road', 'track', 'service', 'unclassified', 'residential', 'tertiary', 'tertiary_link',
                      'secondary', 'secondary_link', 'primary', 'primary_link', 'trunk', 'trunk_link',
                      'motorway', 'motorway_link'}

_CROSSING_NOT_ON_ROAD = """highway=crossing - пешеходный переход через автомобильную дорогу.

Важно:
Если на автомобильной дороге (highway=*) есть пешеходный переход, то он должен быть
обозначен точкой с тегом highway=crossing и эта точка должна быть включена в дорогу.

Другие случаи:
Для обозначения пересечения с железнодорожными путями существует тег railway=crossing.
Для highway=footway используется тег footway=crossing.
Пересечения с дворовым проездом (highway=service + living_street=yes) не обозначаются как highway=crossing.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dcrossing
- http://wiki.openstreetmap.org/wiki/RU:Key:crossing
- http://wiki.openstreetmap.org/wiki/RU:Tag:railway%3Dcrossing
"""


class HighwayCrossingChecker(Handler):
    def __init__(self):
        self._not_on_road = set()

    def process_iteration(self, item, iteration):
        if iteration == 0:
            if item['tag'] == 'node' and item.get('highway') == 'crossing':
                self._not_on_road.add(item['id'])
        elif iteration == 1:
            if self._not_on_road:
                if item['tag'] == 'way' and item.get('highway') in _HIGHWAY_ROAD_TAGS:
                    tmp = list(self._not_on_road)
                    highway_nodes = set(item['nodes'])
                    for node_id in tmp:
                        if node_id in highway_nodes:
                            self._not_on_road.remove(node_id)

    def get_iterations_required(self):
        return 2

    def finish(self, output_dir):
        if self._not_on_road:
            fn = output_dir + 'errors/highway/crossing/not_on_road/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_CROSSING_NOT_ON_ROAD)

            fn = output_dir + 'errors/highway/crossing/not_on_road/nodes.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for node_id in self._not_on_road:
                    f.write('https://www.openstreetmap.org/node/%d\n' % (node_id,))
