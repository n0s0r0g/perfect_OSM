from handlers.simplehandler import SimpleHandler
from routines.output import save_items

_NO_OPENING_HOURS = """Для магазина (shop=*) не указано время работы (opening_hours=*).

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:shop
- http://wiki.openstreetmap.org/wiki/RU:Key:opening_hours
"""


class ShopChecker(SimpleHandler):
    def __init__(self):
        self._no_opening_hours = set()

    def process(self, obj):
        if 'shop' in obj:
            if not 'opening_hours' in obj:
                self._no_opening_hours.add((obj['@type'], obj['@id']))

    def finish(self, output_dir):
        save_items(output_dir + 'todo/shop/no_opening_hours/', self._no_opening_hours, _NO_OPENING_HOURS)
