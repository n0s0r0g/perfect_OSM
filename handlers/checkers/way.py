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

    def first_iteration(self, obj):
        if obj['@type'] == 'way':
            # add way without user-specified tags
            if set(obj.keys()) == {'@id', '@type', '@user', '@timestamp', '@version', '@changeset', '@nodes'}:
                self._useless_ways.add(obj['@id'])
            if not obj.get('@nodes'):
                self._empty_ways.add(obj['@id'])

    def second_iteration(self, obj):
        # remove ways used in relations from self._useless_ways
        if obj['@type'] == 'relation':
            ways = self._useless_ways
            for d in obj['@members']:
                if d['type'] == 'way':
                    way_id = d['ref']
                    if way_id in ways:
                        ways.remove(way_id)

    def is_iteration_required(self, iteration):
        return iteration < 2

    def finish(self, output_dir):
        save_ways(output_dir + 'errors/way/useless/', self._useless_ways, _USELESS_WAY)
        save_ways(output_dir + 'errors/way/empty/', self._empty_ways, _EMPTY_WAY)
