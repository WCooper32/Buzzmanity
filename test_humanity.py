import unittest
from humanity import Humanity

class HumanityTestCase(unittest.TestCase):
    def setup(self):
        import csv2dict as c2d

        k = c2d.csv2dict('.keys.txt')

        user_id = k.get('user_id')
        passwd = k.get('passwd')
        client_id = k.get('client_id')
        client_secret = k.get('client_secret')

        self.h = Humanity(user_id,passwd,client_id,client_secret)

    def test_clockin(self):
        assert(True)