# -*- coding: utf-8 -*-
import unittest
from turon.session import Session


class TestSession(unittest.TestCase):
    def setUp(self):
        self.base_url = 'https://pylon.turon.io'
        self.session = Session(self.base_url)

    def test_base_url(self):
        self.assertEqual(self.session.base_url, self.base_url)


if __name__ == '__main__':
    unittest.main()
