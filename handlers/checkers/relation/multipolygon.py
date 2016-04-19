from handlers.simplehandler import Handler

_BAD_MEMBERS = {
    'title': 'Неправильные члены мультиполигона',
    'help_text': """""",
}


class MultipologonChecker(Handler):
    def __init__(self):
        self._bad_members = []

    def process_iteration(self, obj, iteration):
        if iteration == 0:
            self.first_iteration(obj)

    def first_iteration(self, obj):
        if obj['@type'] == 'relation' and obj.get('type') == 'multipolygon':
            valid = True
            for m in obj['@members']:
                if not (m['type'] == 'way' and m['role'] in {'inner', 'outer'}):
                    valid = False
                    # Exceptions
                    # FIXME: type=boundary?
                    if m['type'] == 'node' and m['role'] == 'label':
                        valid = True
                    # End Exceptions
                    if not valid:
                        break
            if not valid:
                self._bad_members.append(obj['@id'])

    def is_iteration_required(self, iteration):
        if iteration == 0:
            return True
        return False

    def finish(self, issues):
        issues.add_issue_type('errors/relation/multipolygon/bad_members', _BAD_MEMBERS)
        for relation_id in self._bad_members:
            issues.add_issue_obj('errors/relation/multipolygon/bad_members', 'relation', relation_id)
