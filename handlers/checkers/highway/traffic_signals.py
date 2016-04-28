from handlers.handler import Handler

_HIGHWAY_ROAD_TAGS = {'road', 'track', 'living_street', 'service', 'unclassified', 'residential', 'tertiary',
                      'tertiary_link', 'secondary', 'secondary_link', 'primary', 'primary_link', 'trunk', 'trunk_link',
                      'motorway', 'motorway_link'}

_TRAFFIC_SIGNALS_NOT_ON_ROAD = {
    'title': 'Светофор не на дороге',
    'help_text': """Светофор расположен не на дороге.""",
}


class HighwayTrafficSignalsChecker(Handler):
    def __init__(self):
        self._not_on_road = set()

    def process_iteration(self, obj, iteration):
        if iteration == 0:
            if obj.get('highway') == 'traffic_signals' and obj['@type'] == 'node':
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

    def finish(self, issues):
        issues.add_issue_type('errors/traffic_signals/not_on_highway', _TRAFFIC_SIGNALS_NOT_ON_ROAD)
        for node_id in self._not_on_road:
            issues.add_issue_obj('errors/traffic_signals/not_on_highway', 'node', node_id)
