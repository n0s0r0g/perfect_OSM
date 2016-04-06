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

    def process_iteration(self, obj, iteration):
        if iteration == 0:
            if obj['@type'] == 'node' and 'traffic_calming' in obj:
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
        save_nodes(output_dir + 'errors/traffic_calming/not_on_highway/', self._not_on_road, _TRAFFIC_CALMING_NOT_ON_ROAD)
