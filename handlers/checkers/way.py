from routines.output import save_ways
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
        save_ways(output_dir + 'errors/useless_ways/', self._ways, _USELESS_WAY)
