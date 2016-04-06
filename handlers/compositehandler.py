from handlers.handler import Handler


class CompositeHandler(Handler):
    def __init__(self):
        self._handlers = []

    def add_handler(self, handler):
        self._handlers.append(handler)

    def is_iteration_required(self, iteration):
        for handler in self._handlers:
            if handler.is_iteration_required(iteration):
                return True
        return False

    def process_iteration(self, o, iteration):
        for handler in self._handlers:
            if handler.is_iteration_required(iteration):
                handler.process_iteration(o, iteration)

    def finish(self, output_dir):
        for handler in self._handlers:
            handler.finish(output_dir)
