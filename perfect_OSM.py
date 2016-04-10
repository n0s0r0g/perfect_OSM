import argparse
import bz2
import functools
import os
import sys
import time

from parsers import osmxml

from handlers.compositehandler import CompositeHandler
from handlers.checkers.node import NodeChecker
from handlers.checkers.way import WayChecker
from handlers.checkers.highway.trunk import HighwayTrunkChecker
from handlers.checkers.highway.trunk_link import HighwayTrunkLinkChecker
from handlers.checkers.highway.track import HighwayTrackChecker
from handlers.checkers.shop import ShopChecker
from handlers.checkers.highway.crossing import HighwayCrossingChecker
from handlers.checkers.highway.traffic_calming import HighwayTrafficCalmingChecker
from handlers.checkers.website import WebsiteChecker
from handlers.checkers.highway.surface import HighwaySurfaceChecker
from handlers.checkers.type import TypeChecker
from handlers.checkers.phone import PhoneChecker

from writers.issues import Issues
from writers.compositewriter import CompositeWriter
from writers.helptext import HelpTextWriter
from writers.osm_links import OSMLinksWriter
from writers.gpx import GPXWriter


def process_file(fn, handler, writer):
    fn = os.path.abspath(fn)

    i = 0
    while handler.is_iteration_required(i):
        print('check iteration: %d' % (i,))
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

    issues = Issues()
    handler.finish(issues)

    writer.process_issues(issues.issue_types, issues.issues)

    i = 0
    while writer.is_iteration_required(i):
        print('geometry iteration: %d' % (i,))
        t0 = time.time()
        if fn.endswith('.osm.bz2'):
            with bz2.BZ2File(fn) as f:
                osmxml.parse(f, functools.partial(writer.process_geometry, iteration=i))
        elif fn.endswith('.osm'):
            with open(fn, 'rt') as f:
                osmxml.parse(f, functools.partial(writer.process_geometry, iteration=i))
        t1 = time.time()
        i += 1
        print('time: %d seconds' % (int(t1 - t0)))

    writer.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='perfect_OSM: a tool to process OpenStreetMap data')
    parser.add_argument('osm_file', type=str, help='Input file with OSM data (.osm, .osm.bz2)')
    parser.add_argument('output_dir', type=str, help='Directory to store the results')
    args = parser.parse_args()

    if not os.path.isfile(args.osm_file):
        print('Error:', file=sys.stderr)
        print('\tFile not found:', args.osm_file, file=sys.stderr)
        sys.exit(1)

    output_dir = os.path.abspath(args.output_dir)
    if not output_dir.endswith('/'):
        output_dir += '/'

    composite_handler = CompositeHandler()
    # Add your handlers here:
    composite_handler.add_handler(NodeChecker())
    composite_handler.add_handler(WayChecker())
    composite_handler.add_handler(HighwayTrunkChecker())
    composite_handler.add_handler(HighwayTrunkLinkChecker())
    composite_handler.add_handler(HighwayTrackChecker())
    composite_handler.add_handler(ShopChecker())
    composite_handler.add_handler(HighwayCrossingChecker())
    composite_handler.add_handler(HighwayTrafficCalmingChecker())
    # composite_handler.add_handler(WebsiteChecker()) # very slow - opens every website from the map!
    composite_handler.add_handler(HighwaySurfaceChecker())
    composite_handler.add_handler(TypeChecker())
    composite_handler.add_handler(PhoneChecker())
    # End of handlers

    # Writers
    composite_writer = CompositeWriter()
    composite_writer.add_writer(HelpTextWriter(output_dir))
    composite_writer.add_writer(OSMLinksWriter(output_dir))
    composite_writer.add_writer(GPXWriter(output_dir))
    # End of writers

    process_file(args.osm_file, composite_handler, composite_writer)
    print('Done!')
