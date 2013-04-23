'''
Created on Jan 8, 2013

@author: oliver
'''
import unittest
import collections
import tempfile
import os
import shutil
import errno
from operator import itemgetter
from dateutil.parser import parse
from Database import Database

class Test(unittest.TestCase):
    
    def setUp(self):
        # For a fresh test each time, we copy the unittest database
        # in a temporary directory and work with that temporary database.
        tmp_dir = tempfile.gettempdir()
        tmp_dir = os.path.join(tmp_dir, '.montehelper')
        try:
            os.makedirs(tmp_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        tmp_database = os.path.join(tmp_dir, 'montehelper_unittest.db')
        # Copy unittest database to temporary directory
        shutil.copy('/home/oliver/montehelper_unittest.db', tmp_database)
        self.db = Database()
        self.db.dbfile = tmp_database

    def tearDown(self):
        pass
    
    def test_getadults(self):
        l = self.db.getadults()
        # Order the list
        l.sort(key=itemgetter('adult_id'))
        # This is the result we expect
        el = [
            {'adult_id':1,'firstname':'Dirk','name':'Seifert','work':'03334-288548'},
            {'adult_id':2,'firstname':'Oliver','name':'Bienert','home':'03334-3693346'},
            {'adult_id':3, 'firstname':'Jenny','name':'Ehlert'},
            {'adult_id':4, 'firstname':'Sabrina','name':'Bonk'}
        ]
        self.__comparelstdicts(l, el)

    def test_getchildren(self):
        l = self.db.getchildren()
        # Order the list
        l.sort(key=itemgetter('child_id'))
        # This is the result we expect
        el = [
            {'child_id':5,'firstname':'Deborian','name':'Brosche','birthdate':parse('2002-10-29'),'yearcalculated':3, 'yc_description':'3rd year', 'ry_description':'2nd year'},
            {'child_id':6,'firstname':'Tarek','name':'Eglin','birthdate':parse('2003-03-04'),'yearcalculated':3, 'yc_description':'3rd year', 'ry_description':None},
            {'child_id':7,'firstname':'Paul','name':'Bonk','birthdate':parse('2003-02-24'),'yearcalculated':3, 'yc_description':'3rd year', 'ry_description':None},
            {'child_id':8,'firstname':'Ida','name':'Bonk','birthdate':parse('2006-10-10'),'yearcalculated':0, 'yc_description':'Kindergarten', 'ry_description':None}
        ]
        self.__comparelstdicts(l, el)
        
    def test_getadult(self):
        d = self.db.getadult(1)
        # The expected result
        ed = {'adult_id':1,'firstname':'Dirk','name':'Seifert','address_id':1,'street':'Schicklerstr.','number':'1','postcode':'16225','city':'Eberswalde','householdsize':5}
        self.__comparedicts(d, ed)
        
    def test_getfonnumbers(self):
        l = self.db.getfonnumbers(1)
        # Order the list
        l.sort(key=itemgetter('fonnumber_id'))
        # Expected result
        el = [{'fonnumber_id':1,'number':'03334-288548','fonnumbertype_id':'work','description':'Business'}]
        self.__comparelstdicts(l, el)
        
    def test_getemail(self):
        l = self.db.getemail(1)
        # Order the list
        l.sort(key=itemgetter('email_id'))
        # Expected result
        el = [{'email_id':1,'email':'info@fmbe.de','note':'Allgemeine Schuladresse'}]
        self.__comparelstdicts(l, el)
        
    def test_getincome(self):
        l = self.db.getincome(1)
        # Order the list
        l.sort(key=itemgetter('income'))
        # Expected result
        el = [
            {'incometype_id':'less','income':85,'description':'Less'},
            {'incometype_id':'salary','income':1355,'description':'Salary'}
        ]
        self.__comparelstdicts(l, el)
        
    def test_getpositions(self):
        l = self.db.getpositions(1)
        # Order the list
        l.sort(key=itemgetter(0))
        # Expected result
        el = [('organization',),('staff',)]
        self.__comparelists(l, el)
        
    def test_getchild(self):
        d = self.db.getchild(5)
        # The expected result
        ed = {'child_id':5,'firstname':'Deborian','name':'Brosche','birthdate':parse('2002-10-29'),'year':2,'benefit':185,'yearcalculated':3, 'yc_description':'3rd year', 'joindate':None, 'separationdate':None}
        self.__comparedicts(d, ed)
        
    def test_getparents(self):
        l = self.db.getparents(5)
        # Order the list
        l.sort(key=itemgetter('adult_id'))
        el = [{'adult_id': 1,'name':'Seifert','firstname':'Dirk','relation_id':'father','description':'Father','calc':True,'pay':True}]
        self.__comparelstdicts(l, el)
        
    def test_getrulings(self):
        l = self.db.getrulings(5)
        # Order the list
        l.sort(key=itemgetter('ruling_id'))
        el = [{'ruling_id':'extendeddaytime','description':'Extended day time','startdate':parse('2012-08-01'),'enddate':parse('2013-07-31')}]
        self.__comparelstdicts(l, el)
        
    def test_getadults_for_calcfee(self):
        l = self.db.getadults_for_calcfee(1)
        # Order the list
        l.sort(key=itemgetter('income'))
        el = [
            {'adult_id':1,'name':'Seifert','firstname':'Dirk','relation_id':'father','income':85,'incometype_id':'less','size':5,'flags':3},
            {'adult_id':1,'name':'Seifert','firstname':'Dirk','relation_id':'father','income':1355,'incometype_id':'salary','size':5,'flags':3}
        ]
        self.__comparelstdicts(l, el)
        
    def test_getchildren_for_calcfee(self):
        l = self.db.getchildren_for_calcfee(1, '2013-02-05')
        # Order the list
        l.sort(key=itemgetter('child_id'))
        # Expected result
        el = [{'child_id':5,'name':'Brosche','firstname':'Deborian','birthdate':parse('2002-10-29'),'benefit':185,'year_id':2,'exdt':1}]
        self.__comparelstdicts(l, el)
        
    def test_getaddress(self):
        d = self.db.getaddress(1)
        # Expected result
        ed = {'name':'Seifert','firstname':'Dirk','street':'Schicklerstr.','number':'1','postcode':'16225', 'city':'Eberswalde'}
        self.__comparedicts(d, ed)
        
    def test_getlookup(self):
        # Get the data from the test database
        d = self.db.getlookup('l_fonnumbertypes')
        # Make a ordered dictionary from the result
        d = collections.OrderedDict(sorted(d.items()))
        # This is the result we expect
        ed = {'home':'Private','work':'Business','mobile':'Mobile'}
        ed = collections.OrderedDict(sorted(ed.items()))
        self.failUnless(len(d) == len(ed), "Database query returned %d records, should be %d" % (len(d), len(ed)))
        for a, b in zip(d, ed):
            self.failIf(a != b, "Keys %s and %s doesn't match" % (a, b))
            self.failIf(d[a] != ed[b], "Values %s and %s doesn't match" % (d[a], ed[b]))
            
    def test_setadult(self):
        data = {'name':'Brosche','firstname':'Dorothee','householdsize':5,'street':'Schicklerstr.','number':'1','postcode':'16225','city':'Eberswalde'}
        positions = ('organization',)
        fonnumbers = [
            {'fonnumbertype_id':'work','number':'03334-288548'},
            {'fonnumbertype_id':'home','number':'03334-123456'}
        ]
        email = [
            {'email':'dorothee.brosche@gmx.de','note':'Privat'}
        ]
        income = [
            {'income':85,'incometype_id':'less'},
            {'income':35,'incometype_id':'misc'},
            {'income':700,'incometype_id':'salary'}
        ]
        r = self.db.setadult(data, positions, fonnumbers, email, income)
        self.failUnless(r == True, "Database statement rolled back")
        d = self.db.getadult(9)
        # The expected result
        ed = {'adult_id':9,'firstname':'Dorothee','name':'Brosche','address_id':1,'street':'Schicklerstr.','number':'1','postcode':'16225','city':'Eberswalde','householdsize':5}
        self.__comparedicts(d, ed)
        l = self.db.gettable('addresses')
        # Order the list
        l.sort(key=itemgetter('address_id'))
        el = [
            {'address_id':1,'street':'Schicklerstr.','number':'1','postcode':'16225', 'city':'Eberswalde'},
            {'address_id':2,'street':'Ruhlaer Str.','number':'18','postcode':'16225', 'city':'Eberswalde'},
            {'address_id':3,'street':'Karlswerk','number':'18','postcode':'16248', 'city':'Niederfinow'}
        ]
        self.__comparelstdicts(l, el)
        l = self.db.gettable('positions', getdict=False)
        # Order the list
        l.sort()
        el = ((1,'organization'),(1,'staff'),(9,'organization'))
        self.__comparelists(l, el)
        l = self.db.gettable('adults_fonnumbers', getdict=False)
        # Order the list
        l.sort()
        el = ((1,1,'work'),(2,2,'home'),(9,1,'work'),(9,3,'home'))
        self.__comparelists(l, el)
        l = self.db.gettable('fonnumbers', getdict=False)
        # Order the list
        l.sort()
        el = ((1,'03334-288548'),(2,'03334-3693346'),(3,'03334-123456'))
        self.__comparelists(l, el)
        l = self.db.gettable('adults_emailaddresses', getdict=False)
        # Order the list
        l.sort()
        el = ((1,1,'Allgemeine Schuladresse'),(9,2,'Privat'))
        self.__comparelists(l, el)
        l = self.db.gettable('emailaddresses', getdict=False)
        # Order the list
        l.sort()
        el = ((1,'info@fmbe.de'),(2,'dorothee.brosche@gmx.de'))
        self.__comparelists(l, el)
        l = self.db.gettable('income', getdict=False)
        # Order the list
        l.sort()
        el = ((1,85,'less'),(1,1355,'salary'),(4,1500,'unemployment'),(9,35,'misc'),(9,85,'less'),(9,700,'salary'))
        self.__comparelists(l, el)
    
    def test_setchild(self):
        data = {'name':'Ehlert','firstname':'Annabelle','birthdate':parse('2005-12-15'),'benefit':185, 'joindate':parse('2008-08-01'), 'separationdate':None}
        parents = [
            {'adult_id':3,'relation_id':'mother','calc':True,'pay':True}
        ]
        rulings = [
            {'ruling_id':'extendeddaytime','description':'Extended day time','startdate':parse('2012-08-01'),'enddate':parse('2013-07-31')}
        ]
        r = self.db.setchild(data, parents, rulings)
        self.failUnless(r == True, "Database statement rolled back")
        d = self.db.getchild(9)
        ed = {'child_id':9,'firstname':'Annabelle','name':'Ehlert','birthdate':parse('2005-12-15'),'year':None,'benefit':185,'yearcalculated':0, 'yc_description':'Kindergarten', 'joindate':parse('2008-08-01'), 'separationdate':None}
        self.__comparedicts(d, ed)   
        l = self.db.gettable('childbenefit', getdict=False)
        # Order the list
        l.sort()
        el = ((5,185),(6,185),(9,185))
        self.__comparelists(l, el)
        l = self.db.gettable('realyear', getdict=False)
        # Order the list
        l.sort()
        el = ((5,1),)
        self.__comparelists(l, el)
        l = self.db.gettable('adults_children', getdict=False)
        # Order the list
        l.sort()
        el = ((1,5,'father',3),(3,9,'mother',3),(4,7,'mother',3),(4,8,'mother',3))
        self.__comparelists(l, el)
        l = self.db.gettable('rulings', getdict=False)
        # Order the list
        l.sort()
        el = ((5,'extendeddaytime','2012-08-01','2013-07-31'),(6,'extendeddaytime','2012-08-01','2013-07-31'),(8,'extendeddaytime','2012-08-01','2013-07-31'),(9,'extendeddaytime','2012-08-01T00:00:00','2013-07-31T00:00:00'))
        self.__comparelists(l, el)
        
    def test_getchildren_for_quarterannouncement(self):
        l = self.db.getchildren_for_quarterannouncement('2012-12-01')
        # Order the list
        l.sort(key=itemgetter('child_id'))
        # Expected results
        el = [
            {'child_id':5, 'name': 'Brosche', 'firstname': 'Deborian', 'birthdate':parse('2002-10-29'),'address':'Schicklerstr. 1','postcode':'16225','city':'Eberswalde','district':'BAR','year_id':2,'exdt':1},
            {'child_id':7, 'name': 'Bonk', 'firstname': 'Paul', 'birthdate':parse('2003-02-24'),'address':'Karlswerk 18','postcode':'16248','city':'Niederfinow','district':'BAR','year_id':3,'exdt':None},
            {'child_id':8, 'name': 'Bonk', 'firstname': 'Ida', 'birthdate':parse('2006-10-10'),'address':'Karlswerk 18','postcode':'16248','city':'Niederfinow','district':'BAR','year_id':0,'exdt':1}
        ]
        self.__comparelstdicts(l, el)


    def __comparelstdicts(self, l, el):
        self.failUnless(len(l) == len(el), "Database query returned %d records, should be %d" % (len(l), len(el)))
        for a, b in zip(l, el):
            self.__comparedicts(a, b)

    def __comparedicts(self, a, b):
        # a and b are dictionaries. Order them.
        oa = collections.OrderedDict(sorted(a.items()))
        ob = collections.OrderedDict(sorted(b.items()))
        for c, d in zip(oa, ob):
            self.failIf(c != d, "Keys %s and %s doesn't match" % (c, d))
            self.failIf(oa[c] != ob[d], "Values %s and %s doesn't match" % (oa[c], ob[d]))
            
    def __comparelists(self, l, el):
        self.failUnless(len(l) == len(el), "Database query returned %d records, should be %d" % (len(l), len(el)))
        for a, b in zip(l, el):
            self.failIf(a != b, "Values %s and %s doesn't match" % (a, b))
                       
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_getlookup']
    unittest.main()