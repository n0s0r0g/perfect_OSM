from handlers.simplehandler import SimpleHandler

_NO_TYPE = {
    'title': 'Не указан тип отношения',
    'help_text': """""",
}


class RelationChecker(SimpleHandler):
    def __init__(self):
        self._no_type = []

    def process(self, obj):
        if obj['@type'] == 'relation':
            if 'type' not in obj:
                self._no_type.append(obj['@id'])

    def finish(self, issues):
        issues.add_issue_type('errors/relation/no_type', _NO_TYPE)
        for relation_id in self._no_type:
            issues.add_issue_obj('errors/relation/no_type', 'relation', relation_id)
