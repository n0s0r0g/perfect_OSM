from routines.output import save_ways
from handlers.handler import Handler

_EMPTY_WAY = """Пустая линия (way).

Список найденных линий: ways.txt
"""

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
        self._useless_ways = set()
        self._empty_ways = set()

    def process_iteration(self, item, iteration):
        if iteration == 0:
            self.first_iteration(item)
        elif iteration == 1:
            self.second_iteration(item)

    def first_iteration(self, item):
        if item['tag'] == 'way':
            # add way without user-specified tags
            if set(item.keys()) == {'id', 'tag', 'user', 'timestamp', 'version', 'changeset', 'nodes'}:
                self._useless_ways.add(item['id'])
            if not item.get('nodes'):
                self._empty_ways.add(item['id'])

    def second_iteration(self, item):
        # remove ways used in relations from self._useless_ways
        if item['tag'] == 'relation':
            ways = self._useless_ways
            for d in item['members']:
                if d['type'] == 'way':
                    way_id = d['ref']
                    if way_id in ways:
                        ways.remove(way_id)

    def get_iterations_required(self):
        return 2

    def finish(self, output_dir):
        save_ways(output_dir + 'errors/way/useless/', self._useless_ways, _USELESS_WAY)
        save_ways(output_dir + 'errors/way/empty/', self._empty_ways, _EMPTY_WAY)
