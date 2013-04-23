'''
Created on Jan 28, 2013

@author: oliver
'''
import unittest
from operator import itemgetter
from Calcfee import CalcFee
import datetime
import collections


class Test(unittest.TestCase):


    def setUp(self):
        self.fees = [
            (0, 200, 300, 300),
            (725, 31, 44, 80),
            (780, 34, 46, 80),
            (836, 36, 49, 80),
            (891, 39, 52, 80),
            (947, 41, 55, 80),
            (1002, 44, 58, 85),
            (1058, 46, 61, 89), 
            (1113, 48, 64, 94), 
            (1169, 51, 67, 99), 
            (1224, 54, 70, 104), 
            (1280, 56, 73, 108), 
            (1335, 58, 77, 113), 
            (1391, 61, 80, 118), 
            (1446, 63, 84, 122), 
            (1502, 66, 88, 127), 
            (1557, 69, 91, 132), 
            (1613, 71, 95, 137), 
            (1668, 74, 99, 141), 
            (1724, 77, 103, 146), 
            (1779, 80, 107, 151), 
            (1835, 83, 112, 155), 
            (1890, 86, 116, 160), 
            (1946, 89, 120, 165), 
            (2001, 92, 125, 170), 
            (2057, 95, 129, 174), 
            (2112, 98, 134, 179), 
            (2168, 101, 139, 184), 
            (2223, 105, 144, 188), 
            (2279, 108, 149, 193), 
            (2334, 111, 154, 198), 
            (2390, 115, 159, 203), 
            (2445, 118, 164, 207), 
            (2501, 122, 170, 212), 
            (2556, 125, 175, 217), 
            (2612, 129, 181, 222), 
            (2667, 133, 186, 226), 
            (2723, 137, 192, 231), 
            (2778, 141, 198, 236), 
            (2834, 144, 204, 240), 
            (2889, 148, 210, 245), 
            (2945, 152, 216, 250), 
            (3000, 157, 222, 255), 
            (3056, 161, 228, 259), 
            (3111, 165, 235, 264),
            (3167, 169, 241, 269),
            (3222, 173, 248, 273),
            (3278, 178, 254, 278),
            (3333, 182, 261, 283),
            (3389, 186, 268, 288),
            (3444, 191, 275, 292),
            (3500, 196, 282, 297)
        ]

    def tearDown(self):
        pass


    def test_calc(self):
        adults = [
            {'adult_id': 3, 'name': u'Bonk', 'firstname': u'Sabrina', 'relation_id': u'mother', 'flags': 3, 'incometype_id': u'unemployment', 'income': 1500, 'size': 4}
        ]
        children = [
            {'name': u'Bonk', 'firstname': u'Paul', 'year_id': 4, 'birthdate': datetime.datetime(2003, 2, 24, 0, 0), 'benefit': None, 'exdt': None, 'child_id': 1},
            {'name': u'Bonk', 'firstname': u'Ida', 'year_id': 0, 'birthdate': datetime.datetime(2006, 10, 10, 0, 0), 'benefit': None, 'exdt': 1, 'child_id': 3}
        ]
        cf = CalcFee()
        data = cf.calc(adults, children, self.fees)
        l = data['adults']
        # Order the list
        l.sort(key=itemgetter('name'))
        # Expected result
        el = [{'totalincome': 1500, 'name': u'Bonk', 'firstname': u'Sabrina', u'unemployment': 1500}]
        self.__comparelstdicts(l, el)
        l = data['children']
        # Order the list
        l.sort(key=itemgetter('fee'))
        # Expected result
        el = [
            {'fee': 67, 'name': u'Bonk', 'firstname': u'Ida', 'reduction2': 0.05, 'reduction1': 0.2, 'income': 1500, 'incomeapplied': 1140.0, 'extendeddaytime': 1},  
            {'fee': 122, 'name': u'Bonk', 'firstname': u'Paul', 'reduction2': 0.05, 'reduction1': 0, 'income': 1500, 'incomeapplied': 1425.0, 'extendeddaytime': None}
        ]
        self.__comparelstdicts(l, el)
        payer = data['payer']
        self.assertEqual(payer, 3, 'Payer should be %i, but is %i' % (3, payer))

    def __comparelstdicts(self, l, el):
        self.failUnless(len(l) == len(el), "Method returned %d records, should be %d" % (len(l), len(el)))
        for a, b in zip(l, el):
            self.__comparedicts(a, b)

    def __comparedicts(self, a, b):
        # a and b are dictionaries. Order them.
        oa = collections.OrderedDict(sorted(a.items()))
        ob = collections.OrderedDict(sorted(b.items()))
        for c, d in zip(oa, ob):
            self.failIf(c != d, "Keys %s and %s doesn't match" % (c, d))
            self.failIf(oa[c] != ob[d], "Key %s: Values %s and %s doesn't match" % (c, oa[c], ob[d]))
            
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()