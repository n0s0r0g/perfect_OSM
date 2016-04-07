class CompositeWriter:
    def __init__(self):
        self._writers = []

    def add_writer(self, writer):
        self._writers.append(writer)

    def process_issues(self, issue_types, issues):
        for writer in self._writers:
            writer.process_issues(issue_types, issues)

    def process_geometry(self, o, iteration):
        for writer in self._writers:
            if writer.is_iteration_required(iteration):
                writer.process_geometry(o, iteration)

    def is_iteration_required(self, iteration):
        for writer in self._writers:
            if writer.is_iteration_required(iteration):
                return True
        return False

    def save(self):
        for writer in self._writers:
            writer.save()
