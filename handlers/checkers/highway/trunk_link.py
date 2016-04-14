from handlers.simplehandler import SimpleHandler

_TRUNK_LINK_NO_ONEWAY = {
    'title': 'Не указан oneway=*',
    'help_text': """Для вьезда/сьезда с трассы (highway=trunk_link) не задан тег oneway.
Для избежания неоднозначности, рекомендуется всегда добавлять тег oneway=*.

Ссылки по теме:
- http://wiki.openstreetmap.org/wiki/RU:Key:highway
""",
}


class HighwayTrunkLinkChecker(SimpleHandler):
    def __init__(self):
        self._no_oneway = set()

    def process(self, obj):
        if obj['@type'] == 'way' and obj.get('highway') == 'trunk_link':
            if 'oneway' not in obj:
                self._no_oneway.add(obj['@id'])

    def finish(self, issues):
        issues.add_issue_type('warnings/highway/trunk_link/no_oneway', _TRUNK_LINK_NO_ONEWAY)
        for way_id in self._no_oneway:
            issues.add_issue_obj('warnings/highway/trunk_link/no_oneway', 'way', way_id)
