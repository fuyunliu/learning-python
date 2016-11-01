# -*- coding: utf-8 -*-

import json

data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
print('DATA:', repr(data))

print('NORMAL:', json.dumps(data, sort_keys=True))
print('INDENT:', json.dumps(data, sort_keys=True, indent=2))
