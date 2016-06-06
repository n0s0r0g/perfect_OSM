import os
import argparse
import shutil


def copy_html(output_dir):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    shutil.copytree(script_dir + '/dist/html_map', output_dir)


# markers.csv
# lat;lon;popup text

def create_markers(output_dir, markers_file):
    l = ['var markerPoints = [']
    for line in open(markers_file, 'rt'):
        lat, lon, popup = line.strip('\n\r\t ').split(';', maxsplit=3)
        if lat != '' and lon != '':
            l.append('  [{lat}, {lon}, "{popup}"],'.format(lat=lat, lon=lon, popup=popup))
    l.append('];')

    fn = output_dir + 'markers.js'
    with open(fn, 'wt') as f:
        f.write('\n'.join(l))


def create_map_with_markers(markers_fn, output_dir):
    # if directory exists - remove it
    output_dir = os.path.abspath(args.output_dir)
    if not output_dir.endswith('/'):
        output_dir += '/'
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    copy_html(output_dir)
    create_markers(output_dir, markers_fn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create_map: a tool to create html map with markers')
    parser.add_argument('markers', type=str, help='csv file with markers: lat;lon;popup')
    parser.add_argument('output_dir', type=str, help='directory to store map files')
    args = parser.parse_args()

    markers_fn = args.markers
    output_dir = args.output_dir

    create_map_with_markers(markers_fn, output_dir)
