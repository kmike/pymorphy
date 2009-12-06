def _mprint(obj, level=0):
    def pr(obj, lev=level):
        print " "*(lev*4), obj

    if isinstance(obj, (str, unicode)):
        pr('"'+obj+'"')
    elif isinstance(obj, (int, float)):
        pr(obj)
    elif isinstance(obj, dict):
        pr('{')
        for key in obj:
            pr("%s: "% key, level+1)
            _mprint(obj[key], level+2)
        pr('}')
    elif isinstance(object, tuple):
        pr('(')
        for item in obj:
            _mprint(item, level+1)
        pr(')')
    elif hasattr(obj,'__iter__') or hasattr(obj,'__iteritems__'):
        pr('[')
        for item in obj:
            _mprint(item, level+1)
        pr(']')

def mprint(obj):
    return _mprint(obj)
