import os

from writers.writer import Writer

_GPX_HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.0">"""

_GPX_FOOTER = """</gpx>"""

_GPX_WPT = """  <wpt lat="{lat}" lon="{lon}">
    <name>{text}</name>
  </wpt>"""

_GPX_TRK_START = """<trk><trkseg>"""
_GPX_TRK = """<trkpt lat="{lat}" lon="{lon}"></trkpt>"""
_GPX_TRK_END = """</trkseg></trk>"""

class GPXWriter(Writer):
    def __init__(self, output_dir):
        self._output_dir = output_dir

        # _output - dict:
        #    key - sub-dir name
        #    value - list:
        #        item - tuple:
        #            0 - obj_type ('node', 'way', 'relation')
        #            1 - obj_id (int, osm object id)
        #            2 - title (str)
        self._output = dict()

        # _resolve_node_loc - set:
        #     item: node_id (int, osm object id)
        self._resolve_node_loc = set()

        # _node_loc - dict:
        #     key - node_id (int, osm node id)
        #     value - tuple (node_lat, node_lon)
        self._node_loc = dict()

        ## way location

        # _way_nodes:
        #     key = way_id (int, osm way id)
        #     value - list of node_id
        self._way_nodes = dict()

        # _resolve_way_node_loc = set:
        #     value: node_id (int, osm object id)
        self._resolve_way_node_loc = set()

    def process_issues(self, issue_types, issues):
        for issue_type_id, issue_objs_list in issues.items():
            title = issue_types[issue_type_id]['title']
            for issue_objs in issue_objs_list:
                if issue_objs['type'] == 'single':
                    obj_type, obj_id = issue_objs['obj']
                    if issue_type_id not in self._output:
                        self._output[issue_type_id] = []
                    self._output[issue_type_id].append((obj_type, obj_id, title))
                    if obj_type == 'node':
                        self._resolve_node_loc.add(obj_id)
                    if obj_type == 'way':
                        self._way_nodes[obj_id] = None
                    if obj_type == 'relation':
                        pass  # TODO: implement relation -> gpx

    def process_geometry(self, obj, iteration):
        if iteration == 0:
            # find (lat, lon) for nodes from self._resolve_node_loc
            if obj['@type'] == 'node' and obj['@id'] in self._resolve_node_loc:
                self._node_loc[obj['@id']] = (obj['@lat'], obj['@lon'])
            # find list(nodes) for ways from self._way_nodes
            #     and add these nodes to self._resolve_way_nodes
            if obj['@type'] == 'way' and obj['@id'] in self._way_nodes:
                self._way_nodes[obj['@id']] = list(obj['@nodes'])
                for node_id in obj['@nodes']:
                    self._resolve_way_node_loc.add(node_id)
        elif iteration == 1:
            if obj['@type'] == 'node' and obj['@id'] in self._resolve_way_node_loc:
                self._node_loc[obj['@id']] = (obj['@lat'], obj['@lon'])

    def is_iteration_required(self, iteration):
        if iteration == 0:
            return self._resolve_node_loc or self._way_nodes
        elif iteration == 1:
            return self._resolve_way_node_loc
        else:
            return False

    def save(self):
        for subdir_name, disp_objs in self._output.items():
            out_dir = self._output_dir + subdir_name + '/'
            os.makedirs(out_dir, exist_ok=True)

            waypoints = []
            tracks = []

            for obj_type, obj_id, title in disp_objs:
                if obj_type == 'node':
                    tmp = self._node_loc.get(obj_id)
                    if tmp is None:
                        continue
                    lat, lon = tmp
                    waypoints.append((lat, lon, title))
                elif obj_type == 'way':
                    nodes = self._way_nodes[obj_id]

                    first_node_id = nodes[0]
                    tmp = self._node_loc.get(first_node_id)
                    if tmp is None:
                        continue
                    lat, lon = tmp
                    waypoints.append((lat, lon, title))

                    track = []
                    bad_track = False
                    for node_id in nodes:
                        tmp = self._node_loc.get(node_id)
                        if tmp is None:
                            bad_track = True
                            break
                        lat, lon = tmp
                        track.append((lat, lon))
                    if not bad_track:
                        tracks.append(track)

                elif obj_type == 'relation':
                    # TODO: implement relation -> gpx
                    pass

            # prepare gpx file content
            l = [_GPX_HEADER]
            for lat, lon, title in waypoints:
                l.append(_GPX_WPT.format(lat=lat, lon=lon, text=title))
            for track in tracks:
                l.append(_GPX_TRK_START)
                for lat, lon in track:
                    l.append(_GPX_TRK.format(lat=lat, lon=lon))
                l.append(_GPX_TRK_END)
            l.append(_GPX_FOOTER)

            fn = out_dir + 'markers.gpx'
            with open(fn, 'wt') as f:
                f.write('\n'.join(l))
