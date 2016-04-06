from handlers.handler import Handler


class SimpleHandler(Handler):
    def get_iterations_required(self):
        return 1

    def process_iteration(self, o, iteration):
        if iteration == 0:
            self.process(item)
        else:
            raise Exception('invalid iteration = %d (max: %d)' % (iteration, self.get_iterations_required()))

    def process(self, item):
        raise NotImplementedError('Not implemented.')

    def finish(self, output_dir):
        raise NotImplementedError('Not implemented.')
