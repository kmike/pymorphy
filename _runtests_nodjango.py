#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from pymorphy.morph_tests.graminfo import *
from pymorphy.morph_tests.utilities import *
from pymorphy.morph_tests.base import *
from pymorphy.morph_tests.dirty import *
from pymorphy.morph_tests.hyphen import *
from pymorphy.morph_tests.tokenizers import *
from pymorphy.morph_tests.thread_bugs import *
from pymorphy.morph_tests.lastnames_ru import *

if __name__ == '__main__':
    unittest2.main()

