def composite_value(value):
    if ';' in value:
        items = []
        first = True
        for tmp in value.split(';'):
            if not first and tmp.startswith(' '):
                tmp = tmp[1:]
            items.append(tmp)
            first = False
    else:
        items = [value]
    return items
