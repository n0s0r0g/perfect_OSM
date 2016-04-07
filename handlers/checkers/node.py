from handlers.handler import Handler

_USELESS_NODE = {
    'title': 'Бесполезная точка',
    'help_text': """Если точка (node):
- не имеет тегов
- не входит в линию (way)
- не входит в отношение (relation)

то такая точка не содержит полезной информации.

Что нужно сделать:

1. Разобраться, почему такая точка появилась.
2. Постараться заполнить точку полезной информацией.
3. Если точка была добавлена по ошибке - удалить её.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/Untagged_unconnected_node
""",
}


class NodeChecker(Handler):
    def __init__(self):
        self._nodes = set()

    def process_iteration(self, item, iteration):
        if iteration == 0:
            self.first_iteration(item)
        elif iteration == 1:
            self.second_iteration(item)

    def first_iteration(self, obj):
        if obj['@type'] == 'node':
            # add node without user-specified tags
            if set(obj.keys()) == {'@id', '@type', '@lon', '@lat', '@user', '@timestamp', '@version', '@changeset'}:
                self._nodes.add(obj['@id'])

    def second_iteration(self, obj):
        nodes = self._nodes
        # remove nodes used in ways or relations
        if obj['@type'] == 'way':
            for node in obj['@nodes']:
                if node in nodes:
                    nodes.remove(node)
        elif obj['@type'] == 'relation':
            for d in obj['@members']:
                if d['type'] == 'node':
                    node = d['ref']
                    if node in nodes:
                        nodes.remove(node)

    def is_iteration_required(self, iteration):
        return iteration < 2

    def finish(self, issues):
        issues.add_issue_type('errors/node/useless', _USELESS_NODE)
        for node_id in self._nodes:
            issues.add_issue_obj('errors/node/useless', 'node', node_id)
