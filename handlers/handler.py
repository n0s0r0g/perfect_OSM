class Handler:
    def process_iteration(self, o, iteration):
        raise NotImplementedError('Not implemented.')

    def get_iterations_required(self):
        raise NotImplementedError('Not implemented.')

    def finish(self, output_dir):
        raise NotImplementedError('Not implemented.')
