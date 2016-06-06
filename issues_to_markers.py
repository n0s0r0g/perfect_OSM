# Script converts issues.csv to markers.csv
#
# issues.csv
# lat;lon;obj_type;obj_id;issue_type_id;title
#
# markers.csv
# lat;lon;popup

import argparse

_POPUP_TEXT = ''.join(["<b>{title}</b>:<br>",
                       "<a href='https://www.openstreetmap.org/{obj_type}/{obj_id}' target='_blank'>",
                       "Открыть на OSM.org</a><br>",
                       "<a href='http://localhost:8111/load_and_zoom?left={lon_left}&right={lon_right}&top={lat_top}&bottom={lat_bottom}&select={obj_type}{obj_id}&zoom_mode=download' target='_blank'>",
                       "Открыть в JOSM</a><br>",
                       "<a href='http://level0.osmz.ru/?url={obj_type}/{obj_id}' target='_blank'>",
                       "Открыть в OSMZ</a><br>",
                       "<a href='http://www.openstreetmap.org/edit?editor=id&lat={lat}&lon={lon}&zoom=18&{obj_type}={obj_id}' target='_blank'>Открыть в ID</a>"])

_DELTA = 0.002


def prepare_popup(lat, lon, obj_type, obj_id, issue_type_id, title):
    lat_top = float(lat) + _DELTA
    lat_bottom = float(lat) - _DELTA
    lon_left = float(lon) - _DELTA
    lon_right = float(lon) + _DELTA
    return _POPUP_TEXT.format(title=title, obj_type=obj_type, obj_id=obj_id,
                              lat=lat, lon=lon,
                              lat_top=lat_top, lat_bottom=lat_bottom,
                              lon_left=lon_left, lon_right=lon_right)


def issues_to_markers(issues_fn, markers_fn):
    l = []
    for line in open(issues_fn, 'rt'):
        lat, lon, obj_type, obj_id, issue_type_id, title = line.strip('\n\r\t ').split(';')
        if lat != '' and lon != '':
            popup_text = prepare_popup(lat, lon, obj_type, obj_id, issue_type_id, title)
            l.append('{lat};{lon};{popup_text}'.format(lat=lat, lon=lon, popup_text=popup_text))

    with open(markers_fn, 'wt') as f:
        f.write('\n'.join(l))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='issues_to_markers: a tool to convert '
                                                 'issues csv file to markers csv file')
    parser.add_argument('issues', type=str, help='issues csv file')
    parser.add_argument('markers', type=str, help='markers csv file')
    args = parser.parse_args()

    issues_fn = args.issues
    markers_fn = args.markers

    issues_to_markers(issues_fn, markers_fn)
