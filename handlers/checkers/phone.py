import re

from common.routines import composite_value
from handlers.simplehandler import SimpleHandler

_BAD_PHONE = {
    'title': 'Некорректный формат номера телефона',
    'help_text': """Номер телефона указан в некорректном формате.""",
}

_PHONE_RE = re.compile(r'^\+(?P<country>\d+)(?P<delim>[- ])(?P<area>\d+)(?P=delim)(?P<local>\d+)$')


class PhoneChecker(SimpleHandler):
    def __init__(self):
        self._bad_phone = []

    def process(self, obj):
        phones = []
        for tag in ['phone', 'fax', 'contact:phone', 'contact:fax']:
            if tag in obj:
                phones.append(obj[tag])

        for phone in phones:
            bad_phone = False
            # TODO: Document in Wiki - multiple phone numbers separated by ';'
            items = composite_value(phone)
            for item in items:
                if not _PHONE_RE.match(item):
                    bad_phone = True
                    break
            if bad_phone:
                self._bad_phone.append((obj['@type'], obj['@id']))

    def finish(self, issues):
        issues.add_issue_type('warnings/phone/bad_format', _BAD_PHONE)
        for obj_type, obj_id in self._bad_phone:
            issues.add_issue_obj('warnings/phone/bad_format', obj_type, obj_id)
