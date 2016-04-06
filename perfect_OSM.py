import argparse
import bz2
import functools
import os
import sys
import time

from parsers import osmxml

from handlers.compositehandler import CompositeHandler
from handlers.example import ExampleHandler

def process_file(fn, output_dir, handler):
    fn = os.path.abspath(fn)
    output_dir = os.path.abspath(output_dir)
    if not output_dir.endswith('/'):
        output_dir += '/'

    i = 0
    while handler.is_iteration_required(i):
        print('iteration: %d' % (i,))
        t0 = time.time()
        if fn.endswith('.osm.bz2'):
            with bz2.BZ2File(fn) as f:
                osmxml.parse(f, functools.partial(handler.process_iteration, iteration=i))
        elif fn.endswith('.osm'):
            with open(fn, 'rt') as f:
                osmxml.parse(f, functools.partial(handler.process_iteration, iteration=i))
        t1 = time.time()
        print('time: %d seconds' % (int(t1 - t0)))
        i += 1
    handler.finish(output_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='perfect_OSM: a tool to process OpenStreetMap data')
    parser.add_argument('osm_file', type=str, help='Input file with OSM data (.osm, .osm.bz2)')
    parser.add_argument('output_dir', type=str, help='Directory to store the results')
    args = parser.parse_args()

    if not os.path.isfile(args.osm_file):
        print('Error:', file=sys.stderr)
        print('\tFile not found:', args.osm_file, file=sys.stderr)
        sys.exit(1)

    composite_handler = CompositeHandler()
    # Add your handlers here:
    composite_handler.add_handler(ExampleHandler())
    # End of handlers

    process_file(args.osm_file, args.output_dir, composite_handler)
    print('Done!')
