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


class HighwayTrunkChecker(SimpleHandler):
    def __init__(self):
        self._no_maxspeed = set()
        self._no_lit = set()
        self._no_lanes = set()

    def process(self, obj):
        if obj['@type'] == 'way' and obj.get('highway') == 'trunk':
            if 'maxspeed' not in obj:
                self._no_maxspeed.add(obj['@id'])
            if 'lit' not in obj:
                self._no_lit.add(obj['@id'])
            if 'lanes' not in obj:
                self._no_lanes.add(obj['@id'])

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
