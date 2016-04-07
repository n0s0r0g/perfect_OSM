from handlers.handler import Handler


class ExampleHandler(Handler):
    def __init__(self):
        pass

    def process_iteration(self, obj, iteration):
        pass

    def is_iteration_required(self, iteration):
        return iteration == 0

    def finish(self, output_dir):
        pass
