import os
import argparse
import shutil

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


def copy_html(output_dir):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree(script_dir + '/dist/html_map', output_dir)


def create_markers(output_dir, csv_file):
    l = ['var markerPoints = [']
    for line in open(csv_file, 'rt'):
        lat, lon, obj_type, obj_id, issue_type_id, title = line.strip('\n\r\t ').split(';')
        if lat != '' and lon != '':
            popup = prepare_popup(lat, lon, obj_type, obj_id, issue_type_id, title)
            l.append('  [{lat}, {lon}, "{title}"],'.format(lat=lat, lon=lon, title=popup))
    l.append('];')

    fn = output_dir + 'markers.js'
    with open(fn, 'wt') as f:
        f.write('\n'.join(l))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='csv2map: a tool to visualize issues from csv on html map')
    parser.add_argument('csv_file', type=str, help='Input csv file')
    parser.add_argument('output_dir', type=str, help='Directory to store the results')
    args = parser.parse_args()

    output_dir = args.output_dir
    # if directory exists - remove it
    output_dir = os.path.abspath(args.output_dir)
    if not output_dir.endswith('/'):
        output_dir += '/'
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    csv_file = args.csv_file
    copy_html(output_dir)
    create_markers(output_dir, csv_file)
