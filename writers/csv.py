import os

from writers.writer import Writer


class CSVWriter(Writer):
    def __init__(self, output_dir):
        self._output_dir = output_dir

        # _output - list:
        #    item - tuple:
        #        0 - obj_type ('node', 'way', 'relation')
        #        1 - obj_id (int, osm object id)
        #        2 - issue_type_id
        #        3 - title (str)
        self._output = []

        self._resolve_relations = set()
        self._relations = dict()
        self._resolve_ways = set()
        self._ways = dict()
        self._resolve_nodes = set()
        self._nodes = dict()

    def process_issues(self, issue_types, issues):
        for issue_type_id, issue_objs_list in issues.items():
            title = issue_types[issue_type_id]['title']
            for issue_objs in issue_objs_list:
                if issue_objs['type'] == 'single':
                    obj_type, obj_id = issue_objs['obj']
                    self._output.append((obj_type, obj_id, issue_type_id, title))
                    if obj_type == 'node':
                        self._resolve_nodes.add(obj_id)
                    if obj_type == 'way':
                        self._resolve_ways.add(obj_id)
                    if obj_type == 'relation':
                        self._resolve_relations.add(obj_id)

    def process_geometry(self, obj, iteration):
        if iteration == 0:
            self._process_relations(obj)
        elif iteration == 1:
            self._process_ways(obj)
        elif iteration == 2:
            self._process_nodes(obj)

    def _process_relations(self, obj):
        if obj['@type'] == 'relation' and obj['@id'] in self._resolve_relations:
            has_node = False
            for m in obj['@members']:
                if m['type'] == 'node':
                    has_node = True
                    node_id = m['ref']
                    break
            if has_node:
                self._relations[obj['@id']] = ('node', node_id)
                self._resolve_nodes.add(node_id)
            else:
                has_way = False
                for m in obj['@members']:
                    if m['type'] == 'way':
                        has_way = True
                        way_id = m['ref']
                        break
                if has_way:
                    self._relations[obj['@id']] = ('way', way_id)
                    self._resolve_ways.add(way_id)
                else:
                    # FIXME: relations of relations are not yet supported
                    self._relations[obj['@id']] = None

    def _process_ways(self, obj):
        if obj['@type'] == 'way' and obj['@id'] in self._resolve_ways:
            first_node = obj['@nodes'][0]
            self._resolve_nodes.add(first_node)
            self._ways[obj['@id']] = first_node

    def _process_nodes(self, obj):
        if obj['@type'] == 'node' and obj['@id'] in self._resolve_nodes:
            self._nodes[obj['@id']] = (obj['@lat'], obj['@lon'])

    def is_iteration_required(self, iteration):
        return iteration < 3

    def _get_marker(self, obj_type, obj_id):
        if obj_type == 'relation':
            tmp = self._relations.get(obj_id)
            if tmp is None:
                return None
            tmp_type, tmp_id = tmp
            if tmp_type == 'node':
                coord = self._nodes.get(tmp_id)
            if tmp_type == 'way':
                coord = self._nodes.get(self._ways.get(tmp_id))
        if obj_type == 'way':
            coord = self._nodes.get(self._ways.get(obj_id))
        if obj_type == 'node':
            coord = self._nodes.get(obj_id)
        return coord

    def save(self):
        markers = []

        for obj_type, obj_id, issue_type_id, title in self._output:
            coord = self._get_marker(obj_type, obj_id)
            if coord is None:
                lat, lon  = '', ''
            else:
                lat, lon = coord
            markers.append((lat, lon, obj_type, obj_id, issue_type_id, title))

        # prepare csv file content
        l = []
        for lat, lon, obj_type, obj_id, issue_type_id, title in markers:
            tmp = '{lat};{lon};{obj_type};{obj_id};{issue_type_id};{title}'
            l.append(tmp.format(lat=lat, lon=lon, obj_type=obj_type, obj_id=obj_id,
                                issue_type_id=issue_type_id, title=title))

        output_dir = self._output_dir
        os.makedirs(output_dir, exist_ok=True)
        fn = output_dir + 'issues.csv'
        with open(fn, 'wt') as f:
            f.write('\n'.join(l))
