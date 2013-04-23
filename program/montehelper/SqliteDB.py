'''
Created on May 24, 2012

@author: oliver
'''

import sqlite3 as lite
#import versionedfile as v
from Preferences import Preferences
import os.path
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from datetime import datetime
from Helpers import Helpers

class SqliteDB(Helpers):
    '''
    SqliteDB layer. Connects and works with main sqlite database.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        Helpers.__init__(self)
        cfg = Preferences()
        self.dbfile = cfg.GetProperty('sqlite', 'dbfile')
        self.result = []
        # self._transaction_state = False
        self.lrid = None
        self.con = None
        self.queries = {}
        # The reference date for a child to move to next year (grade)
        self.querydate = datetime.now()
            
    def connect(self, query, parameters=(), return_as_dict=True):
        '''
        Connects to database and executes the given command
        '''
        con = lite.connect(self.dbfile, lite.PARSE_DECLTYPES)
        con.create_function('calcyear',1,self.calculate_year)
        if return_as_dict:
            # Return a dictionary cursor, so we can access results by column name
            con.row_factory = lite.Row
        try:
            with con:
                cur = con.cursor()
                self.__pragma(cur)
                query = self.__getquery(query)
                self.__query(cur, query, parameters)
        except (lite.Warning, lite.Error), e:
            print 'Invalid input:', e
            
    def transact_start(self):
        '''
        Start a transaction
        '''
        self.con = lite.connect(self.dbfile)
        self.con.create_collation("caseinsensitive", self.__collate_cmpnocase)
        cur = self.con.cursor()
        self.__pragma(cur)
        # self._transaction_state = True
                 
    def transact_query(self, query, parameters=()):
        query = self.__getquery(query)
        cur = self.con.cursor()
        cur.execute(query, parameters)
        self.lrid = cur.lastrowid
        result = cur.fetchall()
        return result
    
    def transact_commit(self): 
        self.con.commit()
        # self._transaction_state = False
        
    def transact_rollback(self):
        self.con.rollback()
        # self._transaction_state = False
        
    def transact_close(self):
        if self.con:
            self.con.close()
            
    def calculate_year(self, birthdate):
        '''
        Calculates the year the pupil should be in, assuming the
        global reference date
        
        @param birthdate: Child's birthdate
        @type birthdate: datetime
        @var referencedate: The reference date for a child to move to next year (grade)
        @type referencedate: datetime
        @return: Calculated year
        @rtype: int  
        '''
        referencedate = self.__getreferencedate(self.querydate)
        # Convert to python datetime object
        birthdate = parse(birthdate)
        # Calculate age
        age = relativedelta(referencedate, birthdate).years
        # Calculate year (grade)
        yc = age - 6
        if (yc < 1):
            yc = 0
        return yc
        
    def __pragma(self, cur):
        '''
        Will be called after connection to initialize database parameters
        '''
        cur.execute("PRAGMA synchronous = OFF;")
        cur.execute("PRAGMA foreign_keys = ON;")
        
        
    def __select(self, cur, **params):
        '''
        Select records from the given table
        '''
        query = 'SELECT ' + params['fieldlist'] + ' FROM ' + params['table']
        if (params['whereclause']):
            query += ' ' + params['whereclause']
        cur.execute(query)
        self.result = cur.fetchall()
        
    def __query(self, cur, query, parameters):
        cur.execute(query, parameters)
        self.result = cur.fetchall()
        
    def __getquery(self, query):
        if len(query.split()) == 1:
            # Probably a filename, try to open or read from dict
            if query not in self.queries:
                filename = os.path.join('sql', query + '.sql')
                self.queries[query] = self.read_from_file(filename)
            return self.queries[query]
        else:
            return query

    def __getreferencedate(self, date):
        year = date.year
        referencedate = datetime(year, 9, 30)
        if '{:%m-%d}'.format(date) < '{:%m-%d}'.format(referencedate):
            referencedate = referencedate+relativedelta(years=-1)
        return referencedate
    
    def __collate_cmpnocase(self, string1, string2):
        '''
        Collation clause for use in sqlite database. Compares 2 strings case-insensitive.
        @param string1: 1. String to compare
        @type string1: string
        @param string2: 2. String to compare
        @type string2: string
        @return: Result of comparison (0, 1, or -1)
        @rtype: int  
        '''
        return cmp(string1.lower(), string2.lower())
    
    
        
    
        
            