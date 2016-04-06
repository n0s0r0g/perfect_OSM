from handlers.handler import Handler
from routines.output import save_nodes

_HIGHWAY_ROAD_TAGS = {'road', 'track', 'service', 'unclassified', 'residential', 'tertiary', 'tertiary_link',
                      'secondary', 'secondary_link', 'primary', 'primary_link', 'trunk', 'trunk_link',
                      'motorway', 'motorway_link'}

_CROSSING_NOT_ON_HIGHWAY = """highway=crossing - пешеходный переход через автомобильную дорогу.

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

    def process_iteration(self, obj, iteration):
        if iteration == 0:
            if obj['@type'] == 'node' and obj.get('highway') == 'crossing':
                self._not_on_road.add(obj['@id'])
        elif iteration == 1:
            if self._not_on_road:
                if obj['@type'] == 'way' and obj.get('highway') in _HIGHWAY_ROAD_TAGS:
                    tmp = list(self._not_on_road)
                    highway_nodes = set(obj['@nodes'])
                    for node_id in tmp:
                        if node_id in highway_nodes:
                            self._not_on_road.remove(node_id)

    def is_iteration_required(self, iteration):
        return iteration < 2

    def finish(self, output_dir):
        save_nodes(output_dir + 'errors/highway/crossing/not_on_highway/', self._not_on_road, _CROSSING_NOT_ON_HIGHWAY)
