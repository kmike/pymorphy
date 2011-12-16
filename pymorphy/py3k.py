import sys

PY3 = sys.version_info[0] == 3

if PY3:
    string_types, text_type, binary_type = str, str, bytes
else:
    string_types, text_type, binary_type = basestring, unicode, str
