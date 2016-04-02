import os

from handlers.handler import Handler

USELESS_NODE = """Если точка (node):
- не имеет тегов
- не входит в линию (way)
- не входит в отношение (relation)

то такая точка не содержит полезной информации.

Что нужно сделать:

1. Разобраться, почему такая точка появилась.
2. Постараться заполнить точку полезной информацией.
3. Если точка была добавлена по ошибке - удалить её.

Список найденных точек: nodes.txt

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/Untagged_unconnected_node
"""


class NodeChecker(Handler):
    def __init__(self):
        self._nodes = set()

    def process_iteration(self, item, iteration):
        if iteration == 0:
            self.first_iteration(item)
        elif iteration == 1:
            self.second_iteration(item)

    def first_iteration(self, item):
        if item['tag'] == 'node':
            # add node without user-specified tags
            if set(item.keys()) == {'id', 'tag', 'lon', 'lat', 'user', 'timestamp', 'version', 'changeset'}:
                self._nodes.add(item['id'])

    def second_iteration(self, item):
        nodes = self._nodes
        # remove nodes used in ways or relations
        if item['tag'] == 'way':
            for node in item['nodes']:
                if node in nodes:
                    nodes.remove(node)
        elif item['tag'] == 'relation':
            for d in item['members']:
                if d['type'] == 'node':
                    node = d['ref']
                    if node in nodes:
                        nodes.remove(node)

    def get_iterations_required(self):
        return 2

    def finish(self, output_dir):
        if self._nodes:
            fn = output_dir + 'errors/useless_node/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(USELESS_NODE)

            fn = output_dir + 'errors/useless_node/nodes.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for node_id in self._nodes:
                    f.write('https://www.openstreetmap.org/node/%d\n' % (node_id,))
