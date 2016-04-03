from handlers.handler import Handler
from routines.output import save_nodes

_HIGHWAY_ROAD_TAGS = {'road', 'track', 'living_street', 'service', 'unclassified', 'residential', 'tertiary',
                      'tertiary_link',
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
        save_nodes(output_dir + 'errors/traffic_calming/not_on_road/', self._not_on_road, _TRAFFIC_CALMING_NOT_ON_ROAD)
