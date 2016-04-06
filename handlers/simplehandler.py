from handlers.handler import Handler


class SimpleHandler(Handler):
    def is_iteration_required(self, iteration):
        return iteration == 0

    def process_iteration(self, o, iteration):
        self.process(o)

    def process(self, item):
        raise NotImplementedError('Not implemented.')

    def finish(self, output_dir):
        raise NotImplementedError('Not implemented.')
