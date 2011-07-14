try:
    from pymorphy_speedups._morph import *

    # speedups are available, check if version is correct
    from pymorphy.version import __version__ as pymorphy_version
    try:
        from pymorphy_speedups.version import __version__ as speedups_version
    except ImportError: # 0.5.1 doesn't have __version__ defined
        speedups_version = '0.5.1'

    if pymorphy_version != speedups_version:
        import warnings

        msg = """
pymorphy-speedups version (%s) is not the same as pymorphy
version (%s). This can lead to incorrect parsing so *speedups are disabled*.

Please uninstall pymorphy-speedups to remove this warning or install
the correct pymorphy-speedups version (%s) to enable speedups.
""" % (speedups_version, pymorphy_version, pymorphy_version)

        warnings.warn(msg)

        from pymorphy._morph import *

except ImportError:
    from pymorphy._morph import *
