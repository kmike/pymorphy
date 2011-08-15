try:
    from pymorphy_speedups._morph import *

    #noinspection PyUnresolvedReferences
    from pymorphy.version import speedups_version_is_correct
    if not speedups_version_is_correct():
        from pymorphy._morph import *

except ImportError:
    from pymorphy._morph import *
