import os

from handlers.simplehandler import SimpleHandler

_NO_OPENING_HOURS = """Для магазина (shop=*) не указано время работы (opening_hours=*).

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:shop
- http://wiki.openstreetmap.org/wiki/RU:Key:opening_hours
"""


class ShopChecker(SimpleHandler):
    def __init__(self):
        self._no_opening_hours = set()

    def process(self, item):
        if 'shop' in item:
            if not 'opening_hours' in item:
                self._no_opening_hours.add((item['tag'], item['id']))

    def finish(self, output_dir):
        if self._no_opening_hours:
            fn = output_dir + 'todo/shop/no_opening_hours/help.txt'
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn, 'wt') as f:
                f.write(_NO_OPENING_HOURS)
            fn = output_dir + 'todo/shop/no_opening_hours/items.txt'
            with open(fn, 'wt') as f:
                for item_tag, item_id in self._no_opening_hours:
                    f.write('https://www.openstreetmap.org/%s/%d\n' % (item_tag, item_id))
