from xml.etree import ElementTree


def parse(osm_fn, f):
    context = ElementTree.iterparse(osm_fn, events=("start", "end"))
    context = iter(context)
    event, root = next(context)
    for event, elem in context:
        if event == "end" and elem.tag in {'node', 'way', 'relation'}:
            obj = {'@type': elem.tag, '@id': int(elem.get('id'))}
            for k in 'user', 'timestamp', 'version', 'changeset':
                obj['@' + k] = elem.get(k)

            if elem.tag == 'node':
                for k in ['lon', 'lat']:
                    obj['@' + k] = elem.get(k)
                for p in elem.iter():
                    if p.tag == 'tag':
                        obj[p.get('k')] = p.get('v')

            if elem.tag == 'way':
                nodes = []
                for p in elem.iter():
                    if p.tag == 'tag':
                        obj[p.get('k')] = p.get('v')
                    if p.tag == 'nd':
                        nodes.append(int(p.get('ref')))
                obj['@nodes'] = nodes

            if elem.tag == 'relation':
                members = []
                for p in elem.iter():
                    if p.tag == 'tag':
                        obj[p.get('k')] = p.get('v')
                    if p.tag == 'member':
                        member = {'type': p.get('type'),
                                  'ref': int(p.get('ref')),
                                  'role': p.get('role')}
                        members.append(member)
                obj['@members'] = members

            f(obj)
            elem.clear()
            root.clear()
