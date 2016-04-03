import os


def _prepare_output_dir(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    if not output_dir.endswith('/'):
        output_dir += '/'
    return output_dir


def _save_help(output_dir, help_text):
    fn = output_dir + 'help.txt'
    with open(fn, 'wt') as f:
        f.write(help_text)


def save_nodes(output_dir, nodes, help_text):
    if nodes:
        output_dir = _prepare_output_dir(output_dir)
        _save_help(output_dir, help_text)
        fn = output_dir + 'nodes.txt'
        with open(fn, 'wt') as f:
            for node_id in nodes:
                f.write('https://www.openstreetmap.org/node/%d\n' % (node_id,))


def save_ways(output_dir, ways, help_text):
    if ways:
        output_dir = _prepare_output_dir(output_dir)
        _save_help(output_dir, help_text)
        fn = output_dir + 'nodes.txt'
        with open(fn, 'wt') as f:
            for way_id in ways:
                f.write('https://www.openstreetmap.org/way/%d\n' % (way_id,))


def save_relations(output_dir, relations, help_text):
    if relations:
        output_dir = _prepare_output_dir(output_dir)
        _save_help(output_dir, help_text)
        fn = output_dir + 'nodes.txt'
        with open(fn, 'wt') as f:
            for relation_id in relations:
                f.write('https://www.openstreetmap.org/relation/%d\n' % (relation_id,))


def save_items(output_dir, items, help_text):
    if items:
        output_dir = _prepare_output_dir(output_dir)
        _save_help(output_dir, help_text)
        fn = output_dir + 'items.txt'
        with open(fn, 'wt') as f:
            for item_tag, item_id in items:
                f.write('https://www.openstreetmap.org/%s/%d\n' % (item_tag, item_id))
