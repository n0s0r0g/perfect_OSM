import os

from writers.writer import Writer


class OSMLinksWriter(Writer):
    def __init__(self, output_dir):
        self._output_dir = output_dir

        # _output - dict
        #     key - sub-dir name
        #     value - list
        #          item - link to OSM.org (str)
        self._output = {}

    def process_issues(self, issue_types, issues):
        for issue_type_id, issue_objs in issues.items():
            if issue_type_id not in self._output:
                self._output[issue_type_id] = []

            for objs in issue_objs:
                if objs['type'] == 'single':
                    obj_type, obj_id = objs['obj']
                    self._output[issue_type_id].append('https://www.openstreetmap.org/%s/%d' % (obj_type, obj_id))

    def is_iteration_required(self, iteration):
        return False

    def save(self):
        for subdir_name, osm_links in self._output.items():
            out_dir = self._output_dir + subdir_name + '/'
            os.makedirs(out_dir, exist_ok=True)

            fn = out_dir + 'osm_links.txt'
            with open(fn, 'wt') as f:
                f.write('\n'.join(osm_links))
