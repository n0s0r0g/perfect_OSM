from handlers.handler import Handler


class CompositeHandler(Handler):
    def __init__(self):
        self._handlers = []

    def add_handler(self, handler):
        self._handlers.append(handler)

    def get_iterations_required(self):
        m = 0
        for handler in self._handlers:
            t = handler.get_iterations_required()
            if t > m:
                m = t
        return m

    def process_iteration(self, o, iteration):
        for handler in self._handlers:
            if handler.get_iterations_required() > iteration:
                handler.process_iteration(o, iteration)

    def finish(self, output_dir):
        for handler in self._handlers:
            handler.finish(output_dir)
