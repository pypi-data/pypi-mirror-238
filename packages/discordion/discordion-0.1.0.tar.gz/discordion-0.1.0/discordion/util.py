def pick(d, keys):
    return {k: v for k, v in d.items() if k in keys}


def enum_to_string(arr, name):
    vals = ','.join(arr)
    return f'{{{name}|{vals}}}'