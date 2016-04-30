import re

from handlers.simplehandler import SimpleHandler

_TRUNK_NO_MAXSPEED = {
    'title':'Не указано ограничение скорости',
    'help_text': """На трассе (highway=trunk) не указан maxspeed.

Что нужно сделать:
1. Выяснить, какое ограничение скорости на данном участке трассы (явное - знак ограничения скорости, либо неявное)
2. Добавить тег maxspeed с ограничением

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dtrunk
- http://wiki.openstreetmap.org/wiki/RU:Key:maxspeed
""",
}

_TRUNK_NO_LIT = {
    'title': 'Не указано наличие освещения',
    'help_text': """На трассе (highway=trunk) не указано наличие освещения (lit=*).

Что нужно сделать:
1. Выяснить, освещается ли данный участок трассы.
2. Добавить тег lit

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dtrunk
- http://wiki.openstreetmap.org/wiki/Key:lit

Список найденных трасс (highway=trunk): ways.txt
""",
}

_TRUNK_NO_LANES = {
    'title': 'Не указано количество полос',
    'help_text': """На трассе (highway=trunk) не указано количество полос (lanes=*).

Что нужно сделать:
1. Выяснить, сколько полос на данном участке трассы.
2. Добавить тег lanes

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:lanes
- http://wiki.openstreetmap.org/wiki/RU:Tag:highway%3Dtrunk

Список найденных участков трасс (highway=trunk): ways.txt
""",
}

_TRUNK_NO_REF = {
    'title':'Не указан учетный номер дороги',
    'help_text':'http://wiki.openstreetmap.org/wiki/RU:Key:ref',
}

_TRUNK_BAD_REF = {
    'title': 'Некорректный учетный номер дороги',
    'help_text': 'http://wiki.openstreetmap.org/wiki/RU:Key:ref',
}

_ref_re = (
    # Дороги федерального значения
    re.compile('^М-\d{1,}$'),
    re.compile('^Р-\d{2,}$'),
    re.compile('^А-\d{3,}$'),

    # Дороги регионального и межмуниципального значения
    re.compile('^\d{2}[РАКН]-\d{1,}$'),
)


def _check_ref(ref):
    if ';' in ref:
        items = ref.split(';')
    else:
        items = [ref]
    for item in items:
        valid = False
        for _re in _ref_re:
            if _re.match(item):
                valid = True
                break
        if not valid:
            return False
    return True


_int_ref_re = (
    re.compile('^E \d{2,}$'), # Европейские маршруты
    re.compile('^AH\d{1,}$'), # Азиатские маршруты
)


def _check_int_ref(ref):
    if ';' in ref:
        items = ref.split(';')
    else:
        items = [ref]
    for item in items:
        valid = False
        for _re in _int_ref_re:
            if _re.match(item):
                valid = True
                break
        if not valid:
            return False
    return True


class HighwayTrunkChecker(SimpleHandler):
    def __init__(self):
        self._no_maxspeed = []
        self._no_lit = []
        self._no_lanes = []
        self._no_ref = []
        self._bad_ref = []

    def process(self, obj):
        if obj['@type'] == 'way' and obj.get('highway') == 'trunk':
            if 'maxspeed' not in obj:
                self._no_maxspeed.append(obj['@id'])
            if 'lit' not in obj:
                self._no_lit.append(obj['@id'])
            if 'lanes' not in obj:
                self._no_lanes.append(obj['@id'])
            if not ('ref' in obj or 'int_ref' in obj or 'name' in obj):
                self._no_ref.append(obj['@id'])
            if 'ref' in obj:
                if not _check_ref(obj['ref']):
                    self._bad_ref.append(obj['@id'])
            if 'int_ref' in obj:
                if not _check_int_ref(obj['int_ref']):
                    self._bad_ref.append(obj['@id'])

    def finish(self, issues):
        issues.add_issue_type('todo/highway/trunk/no_maxspeed', _TRUNK_NO_MAXSPEED)
        for way_id in self._no_maxspeed:
            issues.add_issue_obj('todo/highway/trunk/no_maxspeed', 'way', way_id)

        issues.add_issue_type('todo/highway/trunk/no_lanes', _TRUNK_NO_LANES)
        for way_id in self._no_lanes:
            issues.add_issue_obj('todo/highway/trunk/no_lanes', 'way', way_id)

        issues.add_issue_type('todo/highway/trunk/no_lit', _TRUNK_NO_LIT)
        for way_id in self._no_lit:
            issues.add_issue_obj('todo/highway/trunk/no_lit', 'way', way_id)

        issues.add_issue_type('todo/highway/trunk/no_ref', _TRUNK_NO_REF)
        for way_id in self._no_ref:
            issues.add_issue_obj('todo/highway/trunk/no_ref', 'way', way_id)

        issues.add_issue_type('errors/highway/trunk/bad_ref', _TRUNK_BAD_REF)
        for way_id in self._bad_ref:
            issues.add_issue_obj('errors/highway/trunk/bad_ref', 'way', way_id)
