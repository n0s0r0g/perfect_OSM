from handlers.simplehandler import Handler

# To debug possibly bad relation download osm data:
# https://www.openstreetmap.org/api/0.6/relation/{relation_id}/full


_BAD_MEMBERS = {
    'title': 'Неправильные члены отношения',
    'help_text': """""",
}

_BAD_GEOMETRY = {
    'title': 'Неправильная геометрия отношения',
    'help_text': """""",
}


def check_multipolygon(obj, ways):
    outer_pairs = []
    inner_pairs = []
    for m in obj['@members']:
        if m['ref'] not in ways:
            return True
        nodes = ways[m['ref']]
        if m['role'] == 'outer':
            outer_pairs.append((nodes[0], nodes[-1]))
        if m['role'] == 'inner':
            inner_pairs.append((nodes[0], nodes[-1]))
    return _simplify_pairs(inner_pairs) and _simplify_pairs(outer_pairs)


def _simplify_pairs(pairs_list):
    p = None
    changed = True
    while pairs_list and changed:
        changed = False
        if p is None:
            tmp = pairs_list.pop()
            p = [tmp[0], tmp[1]]

        not_used = []
        for p2 in reversed(pairs_list):
            used = False
            if p[0] == p2[0]:
                p[0] = p2[1]
                used = True
            elif p[0] == p2[1]:
                p[0] = p2[0]
                used = True
            elif p[1] == p2[0]:
                p[1] = p2[1]
                used = True
            elif p[1] == p2[1]:
                p[1] = p2[0]
                used = True
            if not used:
                not_used.append(p2)
            else:
                changed = True
        if p[0] == p[1]:
            p = None
            changed = True
        pairs_list = not_used
    return (p is None) and (not bool(pairs_list))


class MultipolygonChecker(Handler):
    def __init__(self):
        self._resolve_ways = set()
        self._ways = dict()
        self._bad_members = set()
        self._bad_geometry = []

    def process_iteration(self, obj, iteration):
        if iteration == 0:
            self.first_iteration(obj)
        elif iteration == 1:
            self.second_iteration(obj)
        elif iteration == 2:
            self.third_iteration(obj)

    def first_iteration(self, obj):
        if obj['@type'] == 'relation' and obj.get('type') == 'multipolygon':
            valid = True
            for m in obj['@members']:
                if m['type'] == 'way' and m['role'] in {'inner', 'outer'}:
                    self._resolve_ways.add(m['ref'])
                else:
                    valid = False
                    # Exceptions
                    if m['type'] == 'node' and m['role'] == 'label': # type=boundary?
                        valid = True
                    if not valid:
                        break
            if not valid:
                self._bad_members.add(obj['@id'])

    def second_iteration(self, obj):
        if obj['@type'] == 'way' and obj['@id'] in self._resolve_ways:
            self._ways[obj['@id']] = obj['@nodes']

    def third_iteration(self, obj):
        if obj['@type'] == 'relation' and obj.get('type') == 'multipolygon' and obj['@id'] not in self._bad_members:
            valid = check_multipolygon(obj, self._ways)
            if not valid:
                self._bad_geometry.append(obj['@id'])

    def is_iteration_required(self, iteration):
        if iteration == 0:
            return True
        elif 1 <= iteration <= 2:
            return bool(self._resolve_ways)
        else:
            return False

    def finish(self, issues):
        issues.add_issue_type('errors/relation/multipolygon/bad_members', _BAD_MEMBERS)
        for relation_id in self._bad_members:
            issues.add_issue_obj('errors/relation/multipolygon/bad_members', 'relation', relation_id)

        issues.add_issue_type('errors/relation/multipolygon/bad_geometry', _BAD_GEOMETRY)
        for relation_id in self._bad_geometry:
            issues.add_issue_obj('errors/relation/multipolygon/bad_geometry', 'relation', relation_id)
