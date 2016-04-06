from handlers.handler import Handler


class SimpleHandler(Handler):
    def process_iteration(self, obj, iteration):
        self.process(obj)

    def process(self, o):
        raise NotImplementedError('Not implemented.')

    def is_iteration_required(self, iteration):
        return iteration == 0

    def finish(self, output_dir):
        raise NotImplementedError('Not implemented.')
