import unittest

from preserves import cmp

class PreservesTestCase(unittest.TestCase):
    def assertPreservesEqual(self, a, b, msg=None):
        if msg is None:
            msg = 'Expected %s to be Preserves-equal to %s' % (a, b)
        self.assertTrue(cmp(a, b) == 0, msg)
