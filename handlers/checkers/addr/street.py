from handlers.handler import Handler

_UNKNOWN_STREET = {
    'title':'Нет дороги с названием этой улицы',
    'help_text':"""http://wiki.openstreetmap.org/wiki/RU:Key:addr

    addr:street - Основное название объекта, по которому ведётся соответствующая нумерация
    (например, название улицы). В случае улицы поблизости должна находиться линия
    с тегом highway=* и тегом name=* со значением, совпадающим с addr:street=* у здания.
    """
}

_BAD_STREET_NAME = {
    'title': 'Некорректное название улицы',
    'help_text':"""http://wiki.openstreetmap.org/wiki/RU:%D0%92%D0%B8%D0%BA%D0%B8%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%82_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F/%D0%A1%D0%BE%D0%B3%D0%BB%D0%B0%D1%88%D0%B5%D0%BD%D0%B8%D0%B5_%D0%BE%D0%B1_%D0%B8%D0%BC%D0%B5%D0%BD%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B8_%D0%B4%D0%BE%D1%80%D0%BE%D0%B3"""
}


class StreetChecker(Handler):
    def __init__(self):
        self._streets = set()
        self._unknown_street = []
        self._bad_street_name = []

    def process_iteration(self, obj, iteration):
        if iteration == 0:
            if 'addr:street' in obj:
                street = obj['addr:street']
                valid = True
                if 'Улица' in street:
                    valid = False
                if valid and 'ул.' in street:
                    valid = False
                if not valid:
                    self._bad_street_name.append((obj['@type'], obj['@id']))

            if 'highway' in obj and 'name' in obj:
                self._streets.add(obj['name'])
        elif iteration == 1:
            if 'building' in obj and 'addr:street' in obj and obj['addr:street'] not in self._streets:
                self._unknown_street.append((obj['@type'], obj['@id']))

    def is_iteration_required(self, iteration):
        return iteration < 2

    def finish(self, issues):
        issues.add_issue_type('errors/addr/unknown_street', _UNKNOWN_STREET)
        for obj_type, obj_id in self._unknown_street:
            issues.add_issue_obj('errors/addr/unknown_street', obj_type, obj_id)

        issues.add_issue_type('errors/addr/bad_street_name', _BAD_STREET_NAME)
        for obj_type, obj_id in self._bad_street_name:
            issues.add_issue_obj('errors/addr/bad_street_name', obj_type, obj_id)
