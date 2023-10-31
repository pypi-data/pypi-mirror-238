# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E1101,E0611


"composite"


import unittest


from obj import Object


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.aaa = "test"
        self.assertEqual(obj.obj.aaa, "test")
