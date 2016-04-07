class Handler:
    def process_iteration(self, obj, iteration):
        raise NotImplementedError('Not implemented.')

    def is_iteration_required(self, iteration):
        raise NotImplementedError('Not implemented.')

    def finish(self, issues):
        raise NotImplementedError('Not implemented.')
