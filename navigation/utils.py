import json
from collections import OrderedDict


def get_icons():
    res = []
    with open('navigation/font_awesome.json') as fa:
        for key, value in json.loads(fa.read(), object_pairs_hook=OrderedDict).items():
            res.append((key, value))
    return sorted(res)
