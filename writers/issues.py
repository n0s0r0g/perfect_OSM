class Issues:
    def __init__(self):
        self.issue_types = {}
        self.issues = {}

    def add_issue_type(self, issue_type_id, issue_type_info):
        self.issue_types[issue_type_id] = issue_type_info

    def add_issue_obj(self, issue_type_id, obj_type, obj_id):
        if issue_type_id not in self.issue_types:
            raise Exception('Invalid issue_type_id: %s' % (issue_type_id,))
        if obj_type not in {'node', 'way', 'relation'}:
            raise Exception('Invalid obj_type: %s' % (obj_type,))
        if issue_type_id not in self.issues:
            self.issues[issue_type_id] = []
        self.issues[issue_type_id].append({'type':'single', 'obj':(obj_type, obj_id)})