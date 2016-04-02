import os

from handlers.handler import Handler

_USELESS_WAY = """Если линия (way):
- не имеет тегов
- не входит в отношение (relation)

то такая линия не содержит полезной информации.

Что нужно сделать:

1. Разобраться, почему такая линия появилась.
2. Постараться заполнить линию полезной информацией.
3. Если линия была добавлена по ошибке - удалить её.

Список найденных линий: ways.txt
"""


class WayChecker(Handler):
    def __init__(self):
        self._ways = set()

    def process_iteration(self, item, iteration):
        if iteration == 0:
            self.first_iteration(item)
        elif iteration == 1:
            self.second_iteration(item)

    def first_iteration(self, item):
        if item['tag'] == 'way':
            # add way without user-specified tags
            if set(item.keys()) == {'id', 'tag', 'user', 'timestamp', 'version', 'changeset', 'nodes'}:
                self._ways.add(item['id'])

    def second_iteration(self, item):
        # remove ways used in relations
        if item['tag'] == 'relation':
            ways = self._ways
            for d in item['members']:
                if d['type'] == 'way':
                    way_id = d['ref']
                    if way_id in ways:
                        ways.remove(way_id)

    def get_iterations_required(self):
        return 2

    def finish(self, output_dir):
        if self._ways:
            fn = output_dir + 'errors/useless_ways/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_USELESS_WAY)

            fn = output_dir + 'errors/useless_ways/ways.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                for way_id in self._ways:
                    f.write('https://www.openstreetmap.org/way/%d\n' % (way_id,))
