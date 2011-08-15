# pymorphy version info

VERSION = (0, 5, 5)
__version__ = '.'.join(map(str, VERSION))

def speedups_version_is_correct(warn=True):
    # speedups are available, check if version is correct
    try:
        from pymorphy_speedups.version import __version__ as speedups_version
    except ImportError: # 0.5.1 doesn't have __version__ defined
        speedups_version = '0.5.1'

    if __version__ != speedups_version:
        if warn:
            import warnings

            msg = """
pymorphy-speedups version (%s) is not the same as pymorphy
version (%s). This can lead to incorrect parsing so *speedups are disabled*.

Please uninstall pymorphy-speedups to remove this warning or install
the correct pymorphy-speedups version (%s) to enable speedups.
""" % (speedups_version, __version__, __version__)

            warnings.warn(msg)
        return False
    return True

