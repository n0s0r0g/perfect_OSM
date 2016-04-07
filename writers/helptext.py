import os

from writers.writer import Writer


class HelpTextWriter(Writer):
    def __init__(self, output_dir):
        self._output_dir = output_dir
        self._output = []

    def process_issues(self, issue_types, issues):
        for issue_type_id, _issue_objs_list in issues.items():
            subdir_name = issue_type_id
            help_text = issue_types[issue_type_id].get('help_text', '')
            self._output.append((subdir_name, help_text))

    def is_iteration_required(self, iteration):
        return False

    def save(self):
        for subdir_name, help_text in self._output:
            out_dir = self._output_dir + subdir_name + '/'
            os.makedirs(out_dir, exist_ok=True)

            fn = out_dir + 'help.txt'
            with open(fn, 'wt') as f:
                f.write(help_text)