import os

from writers.writer import Writer


class StatisticsWriter(Writer):
    def __init__(self, output_dir):
        self._output_dir = output_dir

        # _output - dict
        #     key - issue type
        #     value - issues count
        self._output = {}

    def process_issues(self, issue_types, issues):
        for issue_type_id, issue_objs in issues.items():
            self._output[issue_type_id] = len(issue_objs)

    def is_iteration_required(self, iteration):
        return False

    def save(self):
        tmp = list(self._output.items())
        tmp.sort(reverse=True, key=lambda x: x[1])
        l = []
        for k, v in tmp:
            l.append('%s = %d' % (k, v))

        out_dir = self._output_dir
        os.makedirs(out_dir, exist_ok=True)
        fn = out_dir + 'statistics.txt'
        with open(fn, 'wt') as f:
            f.write('\n'.join(l))
