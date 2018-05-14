
import unittest

class Basic(unittest.TestCase):

    def setUp(self):
        print("Setup Called")

    def test_proof_of_concept(self):
        self.assertEqual(1,int('1'))