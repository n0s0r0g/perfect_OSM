from handlers.simplehandler import SimpleHandler

_FIXME = {
    'title': 'На объекте указан тег fixme',
    'help_text': """На объекте указан тег fixme.""",
}


class FixmeChecker(SimpleHandler):
    def __init__(self):
        self._fixme = []

    def process(self, obj):
        if 'fixme' in obj:
            self._fixme.append((obj['@type'], obj['@id']))

    def finish(self, issues):
        issues.add_issue_type('todo/fixme', _FIXME)
        for obj_type, obj_id in self._fixme:
            issues.add_issue_obj('todo/fixme', obj_type, obj_id)
