# coding: utf8
from __future__ import unicode_literals
import random
from pymorphy.morph_tests.base import MorphTestCase
from pymorphy.morph_tests.dicts import morph_ru

# http://www.caktusgroup.com/blog/2009/05/26/testing-django-views-for-concurrency-issues/
def test_concurrently(times):
    """
    Add this decorator to small pieces of code that you want to test
    concurrently to make sure they don't raise exceptions when run at the
    same time.  E.g., some Django views that do a SELECT and then a subsequent
    INSERT might fail when the INSERT assumes that the data has not changed
    since the SELECT.
    """
    def test_concurrently_decorator(test_func):
        def wrapper(*args, **kwargs):
            exceptions = []
            import threading
            def call_test_func():
                try:
                    test_func(*args, **kwargs)
                except Exception as e:
                    exceptions.append(e)
                    raise
            threads = []
            for i in range(times):
                threads.append(threading.Thread(target=call_test_func))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            if exceptions:
                raise Exception('test_concurrently intercepted %s exceptions: %s' % (len(exceptions), exceptions))
        return wrapper
    return test_concurrently_decorator


class SqliteThreadingTest(MorphTestCase):

    @test_concurrently(100)
    def test_sqlite(self):
        words = {1: 'КОММЕНТАРИЙ', 2: 'КОММЕНТАРИЯ'}
        num = random.choice([1,2])
        inflected = morph_ru.pluralize_inflected_ru('КОММЕНТАРИЙ', num)
        self.assertEqualRu(inflected, words[num])

