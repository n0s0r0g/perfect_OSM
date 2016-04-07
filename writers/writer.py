class Writer:
    def process_issues(self, issue_types, issues):
        raise NotImplementedError('Not implemented.')

    def process_geometry(self, o, iteration):
        raise NotImplementedError('Not implemented.')

    def is_iteration_required(self, iteration):
        raise NotImplementedError('Not implemented.')

    def save(self):
        raise NotImplementedError('Not implemented.')
