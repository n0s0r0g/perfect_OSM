from handlers.simplehandler import SimpleHandler

_NO_OPENING_HOURS = {
    'title': 'Не указано время работы',
    'help_text': """Для магазина (shop=*) не указано время работы (opening_hours=*).

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:shop
- http://wiki.openstreetmap.org/wiki/RU:Key:opening_hours
""",
}


class ShopChecker(SimpleHandler):
    def __init__(self):
        self._no_opening_hours = set()

    def process(self, obj):
        if 'shop' in obj:
            if not 'opening_hours' in obj:
                self._no_opening_hours.add((obj['@type'], obj['@id']))

    def finish(self, issues):
        issues.add_issue_type('todo/shop/no_opening_hours/', _NO_OPENING_HOURS)
        for obj_type, obj_id in self._no_opening_hours:
            issues.add_issue_obj('todo/shop/no_opening_hours/', obj_type, obj_id)
