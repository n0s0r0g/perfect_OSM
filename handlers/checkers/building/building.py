from handlers.simplehandler import SimpleHandler

_NODE_BUILDING = {
    'title': 'Здание указано точкой',
    'help_text': """
""",
}


class BuildingChecker(SimpleHandler):
    def __init__(self):
        self._building_on_node = []

    def process(self, obj):
        if 'building' in obj and obj['@type'] == 'node':
            self._building_on_node.append(obj['@id'])

    def finish(self, issues):
        issues.add_issue_type('todo/building/is_node', _NODE_BUILDING)
        for node_id in self._building_on_node:
            issues.add_issue_obj('todo/building/is_node', 'node', node_id)
