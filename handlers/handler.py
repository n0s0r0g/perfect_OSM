class Handler:
    def process_iteration(self, obj, iteration):
        raise NotImplementedError('Not implemented.')

    def is_iteration_required(self, iteration):
        raise NotImplementedError('Not implemented.')

    def finish(self, output_dir):
        raise NotImplementedError('Not implemented.')
