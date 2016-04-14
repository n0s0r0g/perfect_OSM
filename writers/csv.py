import os

from writers.writer import Writer


class CSVWriter(Writer):
    def __init__(self, output_dir):
        self._output_dir = output_dir

        # _output - list:
        #    item - tuple:
        #        0 - obj_type ('node', 'way', 'relation')
        #        1 - obj_id (int, osm object id)
        #        2 - title (str)
        self._output = []

        # _resolve_node_loc - set:
        #     item: node_id (int, osm object id)
        self._resolve_node_loc = set()

        # _node_loc - dict:
        #     key - node_id (int, osm node id)
        #     value - tuple (node_lat, node_lon)
        self._node_loc = dict()

        ## way location

        # _way_first_node:
        #     key = way_id (int, osm way id)
        #     value - first node_id
        self._way_first_node = dict()

        # _resolve_way_node_loc = set:
        #     value: node_id (int, osm object id)
        self._resolve_way_node_loc = set()

    def process_issues(self, issue_types, issues):
        for issue_type_id, issue_objs_list in issues.items():
            title = issue_types[issue_type_id]['title']
            for issue_objs in issue_objs_list:
                if issue_objs['type'] == 'single':
                    obj_type, obj_id = issue_objs['obj']
                    self._output.append((obj_type, obj_id, issue_type_id, title))
                    if obj_type == 'node':
                        self._resolve_node_loc.add(obj_id)
                    if obj_type == 'way':
                        self._way_first_node[obj_id] = None
                    if obj_type == 'relation':
                        pass  # TODO: implement relation geometry to csv

    def process_geometry(self, obj, iteration):
        if iteration == 0:
            # find (lat, lon) for nodes from self._resolve_node_loc
            if obj['@type'] == 'node' and obj['@id'] in self._resolve_node_loc:
                self._node_loc[obj['@id']] = (obj['@lat'], obj['@lon'])
            # find first node for ways from self._way_first_node
            # and add this node to self._resolve_way_node_loc
            if obj['@type'] == 'way' and obj['@id'] in self._way_first_node:
                self._way_first_node[obj['@id']] = obj['@nodes'][0]
                self._resolve_way_node_loc.add(obj['@nodes'][0])
        elif iteration == 1:
            if obj['@type'] == 'node' and obj['@id'] in self._resolve_way_node_loc:
                self._node_loc[obj['@id']] = (obj['@lat'], obj['@lon'])

    def is_iteration_required(self, iteration):
        if iteration == 0:
            return self._resolve_node_loc or self._way_first_node
        elif iteration == 1:
            return self._resolve_way_node_loc
        else:
            return False

    def save(self):
        markers = []

        for obj_type, obj_id, issue_type_id, title in self._output:
            if obj_type == 'node':
                lat, lon = self._node_loc[obj_id]
                markers.append((lat, lon, obj_type, obj_id, issue_type_id, title))
            elif obj_type == 'way':
                first_node_id = self._way_first_node[obj_id]
                lat, lon = self._node_loc.get(first_node_id, ('', ''))
                markers.append((lat, lon, obj_type, obj_id, issue_type_id, title))
            elif obj_type == 'relation':
                # TODO: implement relation geometry to csv
                markers.append(('', '', obj_type, obj_id, issue_type_id, title))

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
