import os

from handlers.handler import Handler

_HIGHWAY_ROAD_TAGS = {'road', 'track', 'living_street', 'service', 'unclassified', 'residential', 'tertiary', 'tertiary_link',
                      'secondary', 'secondary_link', 'primary', 'primary_link', 'trunk', 'trunk_link',
                      'motorway', 'motorway_link'}

_TRAFFIC_CALMING_NOT_ON_ROAD = """highway=traffic_calming - препятствие на дороге, заставляющее снижать скорость.

Препятствие обозначено точкой с тегом highway=traffic_calming.
Точка должна быть включена в автомобильную дорогу.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:traffic_calming
"""


class HighwayTrafficCalmingChecker(Handler):
    def __init__(self):
        self._not_on_road = set()

    def process_iteration(self, item, iteration):
        if iteration == 0:
            if item['tag'] == 'node' and 'traffic_calming' in item:
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
            fn = output_dir + 'errors/traffic_calming/not_on_road/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_TRAFFIC_CALMING_NOT_ON_ROAD)

            fn = output_dir + 'errors/traffic_calming/not_on_road/nodes.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for node_id in self._not_on_road:
                    f.write('https://www.openstreetmap.org/node/%d\n' % (node_id,))
