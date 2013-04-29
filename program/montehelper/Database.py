# -*- coding: utf-8 -*-
'''
Database queries. All queries and statements are to be placed in this class.
Each public method returns the result of a database query
or updates a database record. Database inherits from SQLiteDB, which makes
the actual connection to the sqlite database.

Created on Jun 1, 2012

@author: Oliver Bienert
'''

from dateutil.parser import parse
from SqliteDB import SqliteDB
from Helpers import Helpers
import logging

# Logger
logger = logging.getLogger('montehelper.%s' % __name__)

class Database(SqliteDB, Helpers):
    '''
    Each public method returns either a result set of a database query
    or executes updates or inserts into the database.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(Database, self).__init__()
        
    def updatedb(self, version):
        '''
        Check and update database if necessary
        @param version: Program version to be compared against database version
        '''
        ret = True
        try:
            # Wrap in transaction
            self.transact_start()
            # First check if version table exists in database
            dbversion = self.__initversion()
            # When database version differs from program version,
            # exec all update methods starting from database version + 1
            # up to program version if any.
            while (dbversion < version):
                # set method name
                method = '_Database__update%i' % dbversion
                if method in dir(self):
                    # Execute update method
                    callableobj = getattr(self, method)
                    callableobj()
                    logger.info('Update %i called' % dbversion)
                dbversion += 1
            self.transact_commit()
        except Exception, e:
            ret = False
            print "Writing to database failed:", e
            self.transact_rollback()
        finally:
            self.transact_close()
        return ret
        
    
        
    def getadults(self):
        '''
        Get all adult records from the database and join with fon numbers.
        
        @return: List of dictionaries, each dictionary representing
            an adult_id, using column names as dictionary keys
        @rtype: list        
        '''
        # Create a dict of dicts, using adult_id as the key for the parent dict
        dct = {}
        # Read statement from file
        self.connect('getadults')
        for item in self.result:
            # item is dict representing a row of the result set
            adult_id = item['adult_id']
            fonnumbertype_id = item['fonnumbertype_id']
            number = item['number']
            # Test if we have already an entry for this adult_id
            if dct.has_key(adult_id) == False:
                # Init a new dict entry using key adult_id
                dct[adult_id] = {'adult_id':adult_id,'name':item['name'],'firstname':item['firstname']}
            # We use the first found entry for a fon type only:
            # If the subdict has the appropriate key already, then don't insert again
            if fonnumbertype_id and dct[adult_id].has_key(fonnumbertype_id) == False:
                dct[adult_id][fonnumbertype_id] = number
        return dct.values()
    
    def getchildren(self):
        '''
        Get children records to be put into main frame.
        
        @return: List of dictionaries, each dictionary representing a row
            of the result set, using column names as dictionary keys
        @rtype: list      
        '''
        lst = []
        # If a different year is defined for a child, use this look-up
        # to get the year name
        dct = self.getlookup('l_year')
        # Read statement from file
        self.connect('getchildren')
        for item in self.result:
            # Cast sqlite3.Row to dictionary 
            d = dict(item)
            # Convert birthdate string into datetime object
            d['birthdate'] = parse(d['birthdate'])
            d['ry_description'] = None
            try:
                realyear = int(item['year_id'])
                # Adjust with the difference stored in realyear
                year_id = item['yearcalculated'] - realyear
                d['ry_description'] = dct[year_id]
            except (ValueError, TypeError):
                pass
            del d['year_id']
            lst.append(d)
        return lst
    
    def gettable(self, tablename, getdict=True):
        '''
        Get all records from specified table
        '''
        lst = []
        query = """select * from %s""" % (tablename,)
        self.connect(query, return_as_dict=getdict)
        if getdict:
            for item in self.result:
                # Cast sqlite3.Row to dictionary 
                d = dict(item)
                lst.append(d)
        else:
            lst = self.result[:]
        return lst
    
    def getadult(self, adult_id):
        '''
        Get the names and address data for given adult_id.
        
        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: First row of result set as dictionary using column names as keys
        @rtype: dict
        '''
        # Read statement from file
        self.connect('getadult', (adult_id,))
        # Get first row of result set and cast to dict
        return dict(self.result[0])
    
    def getfonnumbers(self, adult_id):
        '''
        Get fon numbers for the given adult_id.
        
        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        @rtype: list
        '''
        lst = []
        self.connect('getfonnumbers', (adult_id,))
        for item in self.result:
            # Cast sqlite3.Row to dictionary 
            d = dict(item)
            lst.append(d)
        return lst

    def getemail(self, adult_id):
        '''
        Get email addresses for the given adult_id.

        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        '''
        lst = []
        self.connect('getemail', (adult_id,))
        for item in self.result:
            # Cast sqlite3.Row to dictionary 
            d = dict(item)
            lst.append(d)
        return lst
    
    def getincome(self, adult_id):
        '''
        Get all income records for specified id.

        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        '''
        lst = []
        self.connect('getincome', (adult_id,))
        for item in self.result:
            # Cast sqlite3.Row to dictionary 
            d = dict(item)
            lst.append(d)
        return lst
    
    def getpositions(self, adult_id):
        '''
        Get all positions for specified id.

        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: List of position keywords
        @rtype: list
        '''
        self.connect('getpositions', (adult_id,), return_as_dict=False)
        return self.result[:]
    
    def getchild(self, child_id):
        '''
        Get the record for specified child_id.

        @param child_id: Unique child identifier
        @type child_id: int
        @return: First row of result set as dictionary using column names as keys
        @rtype: dict
        '''
        self.connect('getchild', (child_id,))
        # Result set is a tuple of dicts, get the first row of result set only
        result = dict(self.result[0])
        # Parse the ISO format from database to datetime object
        result['birthdate'] = parse(result['birthdate'])
        if not result['joindate'] == None:
            result['joindate'] = parse(result['joindate'])
        if not result['separationdate'] == None:
            result['separationdate'] = parse(result['separationdate'])
        try:
            realyear = int(result['year'])
            # Adjust with the difference stored in realyear
            result['year'] = result['yearcalculated'] - realyear 
        except (ValueError, TypeError):
            pass
        return result
    
    def getparents(self, child_id):
        '''
        Get the parents for the specified child_id

        @param child_id: Unique adult identifier
        @type child_id: int
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        '''
        lst = []
        self.connect('getparents', (child_id,))
        for item in self.result:
            # Cast sqlite3.Row to dictionary
            d = dict(item)
            # Testing the flags:
            # Include this adult in calculation of fee
            d['calc'] = True if d['flags'] & (1 << 0) else False
            # Adult liable to pay (Payer)
            d['pay'] = True if d['flags'] & (1 << 1) else False
            del d['flags']
            lst.append(d)
        return lst
    
    def getrulings(self, child_id):
        '''
        Get rulings for this child_id.

        @param child_id: Unique adult identifier
        @type child_id: int
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        '''
        lst = []
        self.connect('getrulings', (child_id,))
        for item in self.result:
            # Cast sqlite3.Row to dictionary
            d = dict(item)
            # We have the dates as ISO datetime strings in the database,
            # convert to python date object.
            d['startdate'] = parse(d['startdate'])
            d['enddate'] = parse(d['enddate'])
            lst.append(d)
        return lst
    
    def getadults_for_calcfee(self, adult_id):
        '''
        Get adults and their incomes for calculation of parent's fee

        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        @rtype: list        
        '''
        lst = []
        # For a given adult_id, select all children that have given this adult as its parent,
        # then select all adults for the child_id's found that are liable to pay.
        self.connect('getadults_for_calcfee', (adult_id,))
        for item in self.result:
            # Cast sqlite3.Row to dictionary
            d = dict(item)
            lst.append(d)
        return lst
    
    def getchildren_for_calcfee(self, adult_id, date):
        '''
        Return all children to be included in the calculation, ordered by birthdate

        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        @rtype: list        
        '''
        lst = []
        self.connect('getchildren_for_calcfee', (date, date, adult_id))
        for item in self.result:
            # Cast sqlite3.Row to dictionary
            d = dict(item)
            # ISO-String to python datetime object
            d['birthdate'] = parse(d['birthdate'])
            year_id = item['yearcalculated']
            try:
                realyear = int(d['year_id'])
                # Adjust with the difference stored in realyear
                year_id = d['yearcalculated'] - realyear
            except (ValueError, TypeError):
                pass
            del d['yearcalculated']
            d['year_id'] = year_id
            lst.append(d)
        return lst
    
    def getchildren_for_quarterannouncement(self, date):
        '''
        Return all children to be included in quarter announcement,
        ordered by year, name, first name and child_id
        @return: List of dictionaries, each dictionary a row
            of the result set, using column names as dictionary keys
        @rtype: list
        '''
        lst = []
        self.connect('getchildren_for_quarterannouncement', (date, date))
        for item in self.result:
            # Cast sqlite3.Row to dictionary
            d = dict(item)
            # ISO-String to python datetime object
            d['birthdate'] = parse(d['birthdate'])
            year_id = d['yearcalculated']
            try:
                realyear = int(d['year_id'])
                # Adjust with the difference stored in realyear
                year_id = d['yearcalculated'] - realyear
            except (ValueError, TypeError):
                pass
            del d['yearcalculated']
            d['year_id'] = year_id
            lst.append(d)
        return lst
            

    def getaddress(self, adult_id):
        '''
        Get address data for given adult_id

        @param adult_id: Unique adult identifier
        @type adult_id: int
        @return: First row of result set as dictionary using column names as keys
        @rtype: dict
        '''
        self.connect('getaddress', (adult_id,))
        # Cast sqlite3.Row to dictionary
        return dict(self.result[0])
    
    def getfees_lookup(self):
        '''
        Returns the l_fees table
        
        @return: List of tuples of fees
        @rtype: list
        '''
        query = """select * from l_fees"""
        self.connect(query, return_as_dict=False)
        return self.result[:]

    def getlookup(self, query_key):
        '''
        Get all values from a lookup table
        
        @param query_key: Table name
        @type query_key: String
        @return: Dictionary using the value of the id column as key and
            the value of the description column as value
        @rtype: Dictionary
        '''
        dct = {}
        query = """select * from %s""" % (query_key,)
        self.connect(query, return_as_dict=False)
        for item in self.result:
            dct[item[0]] = item[1]
        return dct
  
    def setadult(self, data, positions, fonnumbers, email, income):
        '''
        Write an adult record back to database or insert a new one.
        
        @param data: Dict with fields for table adults to be updated
        @type data: Dictionary
        @param positions: List of position keywords
        @type positions: list
        @param fonnumbers: List of fonnumbers and their type
        @type fonnumbers: list
        @param email: List of email-addresses
        @type email: list
        @param income: List of incomes and thei respective type
        @type income: list       
        '''
        ret = True
        try:
            self.transact_start()
            if data.has_key('adult_id'):
                # Update existing record.
                adult_id = data['adult_id']
                self.__updateadult(data)
            else:
                # insert new record
                adult_id = self.__insertadult(data)
            self.__updatehouseholdsize(adult_id, data)
            self.__updateaddresses(adult_id, data)
            self.__updatepositions(adult_id, positions)
            self.__updatefonnumbers(adult_id, fonnumbers)
            self.__updateemail(adult_id, email)
            self.__updateincome(adult_id, income)
            self.transact_commit()
        except Exception, e:
            ret = False
            print "Writing to database failed:", e
            self.transact_rollback()
        finally:
            self.transact_close()
        return ret
        
    def deleteadult(self, adult_id):
        '''
        Delete an adult record.
        '''
        ret = True
        try:
            self.transact_start()
            self.transact_query('deletepeople', (adult_id,))
            self.__cleanaddresses()
            self.__cleanemailaddresses()
            self.__cleanfonnumbers()
            self.transact_commit()
        except Exception, e:
            ret = False
            print "Writing to database failed:", e
            self.transact_rollback()
        finally:
            self.transact_close()
        return ret
    
    def setchild(self, data, parents, rulings):
        ret = True
        try:
            self.transact_start()
            if data.has_key('child_id'):
                child_id = data['child_id']
                self.__updatechild(data)
            else:
                # insert new record
                child_id = self.__insertchild(data)
            self.__updatebirthdate(child_id, data)
            self.__updatechildbenefit(child_id, data)
            self.__updaterealyear(child_id,data)
            self.__updatejoindate(child_id,data['joindate'], 'school')
            self.__updateseparationdate(child_id, data['separationdate'], 'school')
            self.__updateparents(child_id, parents)
            self.__updaterulings(child_id, rulings)
            self.transact_commit()
        except Exception, e:
            ret = False
            print "Writing to database failed:", e
            self.transact_rollback()
        finally:
            self.transact_close()
        return ret
            
    def deletechild(self, child_id):
        '''
        Delete a child record.
        '''
        ret = True
        try:
            self.transact_start()
            self.transact_query('deletepeople', (child_id,))
            self.transact_commit()
        except Exception, e:
            ret = False
            print "Writing to database failed:", e
            self.transact_rollback()
        finally:
            self.transact_close()
        return ret
    
    def __initversion(self):
        '''
        Initialize version control for database
        '''
        # Create version table if it doesn't exist
        self.transact_query('createversion')
        # Ask for version
        self.transact_query('getversion')
        if not len(self.result):
            # Table just created, set version to 0
            # and insert version record.
            dbversion = 0
            self.transact_query('initversion') 
        else:
            # Get database version
            dct = dict(self.result[0])
            dbversion = dct['build']
        return dbversion
    
    def __update0(self):
        self.transact_query('registrationdate')
        self.transact_query('updateversion', (1,))

    def __updateadult(self, data):
        '''
        Update the adults table part of an adult record.
        '''
        self.transact_query('updatepeople', (data['name'], data['firstname'], data['adult_id']))
    
    def __insertadult(self, data):
        '''
        Insert a new row in the adults table and return
        the new adult_id
        '''
        self.transact_query('insertpeople', (data['name'], data['firstname'], 'adult'))
        adult_id = self.lrid
        return adult_id
    
    def __updatehouseholdsize(self, adult_id, data):
        '''
        Update table householdsize as part of adult record.
        '''
        self.transact_query('deletehouseholdsize', (adult_id,))
        householdsize = data['householdsize']
        try:
            householdsize = int(householdsize)
        except (ValueError, TypeError):
            return
        self.transact_query('inserthouseholdsize', (adult_id, householdsize))
        
    
    def __updateaddresses(self, adult_id, data):
        '''
        Update tables addresses and adults_addresses as part of adult record.
        '''
        # Make a string by joining address data
        strfromdict = "".join("%s" % data[key].strip() for key in ('street','number','postcode','city'))
        # Check if there is an address registered for the given adult_id
        result = self.transact_query('checkaddress', (adult_id,))
        if (result.__len__() == True):
            address_id = result[0][0]
            # Check if the edited address differs from the old address
            strfromdb = "".join("%s" % tup.strip() for tup in result[0][1:])
            if (strfromdb.lower() == strfromdict.lower()):
                # no need to change anything
                return
            else:
                # Edited address differs:
                # Delete adult_id from adult_addresses
                self.transact_query('deleteadults_addresses', (adult_id,))
        self.__cleanaddresses()
        # Check if an address has been registered
        if (len(strfromdict) == 0):
            return 
        # Check if address exists
        tu = tuple([data[key].strip() for key in ('street','number','postcode','city')])
        result = self.transact_query('compareaddresses', tu)
        if (result.__len__() == True):
            address_id = result[0][0]
        else:
            # insert new address
            self.transact_query('insertaddresses', tu)
            address_id = self.lrid
        # Insert id's into adults_addresses
        self.transact_query('insertadults_addresses', (adult_id, address_id))
         
    def __updatepositions(self, adult_id, positions):
        self.transact_query('deletepositions', (adult_id,))
        for position in positions:
            self.transact_query('insertpositions', (adult_id, position))

    def __updatefonnumbers(self, adult_id, fonnumbers):
        # Delete all entries for adult_id in adults_fonnumbers
        self.transact_query('deletefonnumbers', (adult_id,))
        self.__cleanfonnumbers()
        # Insert new numbers
        for line in fonnumbers:
            # Check if number exists
            result = self.transact_query('checkfonnumber', (line['number'],))
            if (result.__len__() == True):
                fonnumber_id = result[0][0]
            else:
                self.transact_query('insertfonnumber', (line['number'],))
                fonnumber_id = self.lrid
            self.transact_query('insertadults_fonnumbers', (adult_id, fonnumber_id, line['fonnumbertype_id']))
    
    def __updateemail(self, adult_id, email):
        # Delete all entries for adult_id in adults_emailaddresses
        self.transact_query('deleteemail', (adult_id,))
        self.__cleanemailaddresses()
        # Insert new addresses
        for line in email:
            # Check if email address exists
            result = self.transact_query('checkemail', (line['email'],))
            if (result.__len__() == True):
                email_id = result[0][0]
            else:
                self.transact_query('insertemail', (line['email'],))
                email_id = self.lrid
            self.transact_query('insertadults_emailaddresses', (adult_id, email_id, line['note']))
    
    def __updateincome(self, adult_id, income):
        # Delete all lines in income for this adult_id
        self.transact_query('deleteincome', (adult_id,))
        # Insert all incomes
        for line in income:
            self.transact_query('insertincome', (adult_id, line['income'], line['incometype_id']))
            
    def __updatechild(self, data):
        self.transact_query('updatepeople', (data['name'], data['firstname'], data['child_id']))
        
    def __insertchild(self, data):
        self.transact_query('insertpeople', (data['name'], data['firstname'], 'child'))
        child_id = self.lrid
        return child_id
    
    def __updatebirthdate(self, child_id, data):
        self.transact_query('deletebirthdate', (child_id,))
        birthdate = data['birthdate'].isoformat()
        self.transact_query('insertbirthdate', (child_id, birthdate))
    
    def __updatechildbenefit(self, child_id, data):
        self.transact_query('deletechildbenefit', (child_id,))
        if 'benefit' not in data:
            return
        benefit = data['benefit']
        try:
            benefit = int(benefit)
        except (ValueError, TypeError):
            return
        self.transact_query('insertchildbenefit', (child_id, benefit))
            
    def __updaterealyear(self, child_id, data):
        self.transact_query('deleterealyear', (child_id,))
        if 'year' not in data:
            return
        year = data['year']
        birthdate = data['birthdate'].isoformat()
        yearcalculated = self.calculate_year(birthdate)
        try:
            year = int(year)
            # store the difference to calculated year
            year = yearcalculated - year
        except (ValueError, TypeError):
            return
        self.transact_query('insertrealyear', (child_id, year))
        
    def __updatejoindate(self, people_id, date, type_id):
        self.transact_query('deletejoindate', (people_id, type_id))
        if not date == None:
            date = date.isoformat()
            self.transact_query('insertjoindate', (people_id, date, type_id))
        
    def __updateseparationdate(self, people_id, date, type_id):
        self.transact_query('deleteseparationdate', (people_id, type_id))
        if not date == None:
            date = date.isoformat()
            self.transact_query('insertseparationdate', (people_id, date, type_id))
        
    def __updateparents(self, child_id, parents):
        self.transact_query('deleteparents', (child_id,))
        for line in parents:
            flags = 0
            if line['calc']: flags |= (1 << 0)
            if line['pay']: flags |= (1 << 1)
            self.transact_query('insertparents', (line['adult_id'], child_id, line['relation_id'], flags))

    def __updaterulings(self, child_id, rulings):
        self.transact_query('deleterulings', (child_id,))
        for line in rulings:
            startdate = line['startdate'].isoformat()
            enddate = line['enddate'].isoformat()
            self.transact_query('insertrulings', (child_id, line['ruling_id'], startdate, enddate))
    
    def __cleanaddresses(self):
        # Check if there are still other adult_id's pointing
        # to this address
        self.transact_query('cleanaddresses')

    def __cleanfonnumbers(self):
        # Delete numbers not used anymore by any person
        self.transact_query('cleanfonnumbers')

    def __cleanemailaddresses(self):
        # Delete email addresses not used anymore by any person
        self.transact_query('cleanemailaddresses')
    

        
        
       
       
        

        
        
