from handlers.handler import Handler
from routines.output import save_nodes

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
        save_nodes(output_dir + 'errors/highway/crossing/not_on_road/', self._not_on_road, _CROSSING_NOT_ON_ROAD)
