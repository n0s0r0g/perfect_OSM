from handlers.simplehandler import SimpleHandler

_NODE_BUILDING = {
    'title': 'Здание указано точкой',
    'help_text': """
""",
}

_NO_ADDR = {
    'title': 'Здание без адреса',
    'help_text':"""Для здания не указан адрес.""",
}

_ADDR_BUILDING_TYPES = {'apartments', 'residential',}


class BuildingChecker(SimpleHandler):
    def __init__(self):
        self._building_on_node = []
        self._no_addr = []

    def process(self, obj):
        if 'building' in obj:
            if obj['@type'] == 'node':
                self._building_on_node.append(obj['@id'])
            if obj['building'] in _ADDR_BUILDING_TYPES and ('addr:street' not in obj or 'addr:housenumber' not in obj):
                self._no_addr.append((obj['@type'], obj['@id']))

    def finish(self, issues):
        issues.add_issue_type('todo/building/is_node', _NODE_BUILDING)
        for node_id in self._building_on_node:
            issues.add_issue_obj('todo/building/is_node', 'node', node_id)

        issues.add_issue_type('todo/building/no_addr', _NO_ADDR)
        for obj_type, obj_id in self._no_addr:
            issues.add_issue_obj('todo/building/no_addr', obj_type, obj_id)
