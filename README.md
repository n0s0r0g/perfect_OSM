# Perfect OSM
`perfect_OSM` is a simple tool to process OpenStreetMap data.

## Requirements

- Python 3 (https://www.python.org)

## Usage:
Command line:

`python3 perfect_OSM.py osm_file output_dir`

- `osm_file` - Open Street Map data (.osm, .osm.bz2)
- `output_dir` - directory to store the results

## Where to get OSM data?

- Russia regions: http://gis-lab.info/projects/osm_dump/
- JOSM -> Download the area -> Save As... -> .osm file

## How to add your own handler?

1. Create .py file inside `handlers/` package.
2. Create new class (for example, `ExampleHandler`) from `Handler` (multi-pass handler) or `SimpleHandler` (single-pass handler) and implement required methods.
3. Add `from handlers.xxx import xxx` to `perfect_OSM.py`.
4. Add your handler after the line: `# Add your handlers here:`
