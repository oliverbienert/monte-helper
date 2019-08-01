'''
Created on Jun 18, 2012

@author: oliver
'''

import os
import sys
import logging
from Database import Database
from pubsub import setupkwargs #@UnusedImport
from pubsub import pub
from Calcfee import CalcFee
from Report import Report
from Preferences import Preferences
from datetime import datetime

# Logger
logger = logging.getLogger('montehelper.%s' % __name__)

class Listeners(object):
    '''
    classdocs
    '''
    def __init__(self, **params):
        self.db = Database()
        pub.subscribe(self.CheckDatabase, 'main.checkdatabase') #@UndefinedVariable
        pub.subscribe(self.DialogAdultPopulate, 'dialog.adult.activated') #@UndefinedVariable
        pub.subscribe(self.StoreAdult, 'dialog.adult.senddata') #@UndefinedVariable
        pub.subscribe(self.CalculateParentsFee, 'mainframe.edit.calcfee') #@UndefinedVariable
        pub.subscribe(self.CreateFeeReport, 'dialog.calcfree.senddata') #@UndefinedVariable
        pub.subscribe(self.DialogChildPopulate, 'dialog.child.activated') #@UndefinedVariable
        pub.subscribe(self.DialogParentPopulate, 'dialog.parent.created') #@UndefinedVariable
        pub.subscribe(self.DialogChildNewParent, 'dialog.parent.objectselected') #@UndefinedVariable
        pub.subscribe(self.StoreChild, 'dialog.child.senddata') #@UndefinedVariable
        pub.subscribe(self.DialogPreferencesPopulate, 'dialog.preferences.activated') #@UndefinedVariable
        pub.subscribe(self.StorePreferences, 'dialog.preferences.save') #@UndefinedVariable
        pub.subscribe(self.DeleteAdult, 'mainframe.delete.adult') #@UndefinedVariable
        pub.subscribe(self.DeleteChild, 'mainframe.delete.child') #@UndefinedVariable
        pub.subscribe(self.DialogAdultFillCB, 'dialog.adult.created') #@UndefinedVariable
        pub.subscribe(self.DialogChildFillCB, 'dialog.child.created') #@UndefinedVariable
        pub.subscribe(self.CreateQuarterAnnouncement, 'mainframe.edit.quarterannouncement')  #@UndefinedVariable
        
    def CheckDatabase(self, init=True):
        '''Called when the main widget is ready or when preferences dialog is closed'''
        # Get location of database file
        cfg = Preferences()
        dbfile = cfg.GetProperty('sqlite', 'dbfile')
        exists = os.path.exists(dbfile)
        if exists == True:
            # Instantiate database object
            adults = self.db.getadults()
            children = self.db.getchildren()
            # Populate notebook listviews
            pub.sendMessage('main.populate.adults', adults=adults) #@UndefinedVariable
            pub.sendMessage('main.populate.children', children=children) #@UndefinedVariable
        elif exists == False and init == True:
            pub.sendMessage('main.activatepreferencesdlg') #@UndefinedVariable
        else:
            sys.exit()

    def DialogAdultPopulate(self, arg1):
        '''Called when EditAdultFrame is activated and ready to receive data'''
        # Query database and get data for selected adult
        self.data = self.db.getadult(arg1)
        self.fonnumbers = self.db.getfonnumbers(arg1)
        self.email = self.db.getemail(arg1)
        self.income = self.db.getincome(arg1)
        positions = self.db.getpositions(arg1)
        # Send data to frame
        pub.sendMessage('dialog.populate.adult', #@UndefinedVariable
                         data=self.data,
                         positions=positions,
                         fonnumbers=self.fonnumbers,
                         email=self.email,
                         income=self.income)
        
    def StoreAdult(self, data, positions, fonnumbers, email, income):
        self.db.setadult(data, positions, fonnumbers, email, income)
        # Refresh main frame listview
        adults = self.db.getadults()
        pub.sendMessage('main.populate.adults', adults=adults) #@UndefinedVariable
        
    def CalculateParentsFee(self, adult_id):
        isodate = '{:%Y-%m-%d}'.format(datetime.now())
        adults = self.db.getadults_for_calcfee(adult_id)
        if len(adults) == 0:
            logger.info('No children found for this adult: %i' % adult_id)
            return
        children = self.db.getchildren_for_calcfee(adult_id, isodate)
        fees = self.db.getfees_lookup()
        cf = CalcFee()
        data = cf.calc(adults, children, fees)
        address = self.db.getaddress(data['payer'])
        pub.sendMessage('dialog.calcfee.populate', data=data, address=address)  #@UndefinedVariable
        
    def CreateFeeReport(self, validfromdate, receiver, calcfees, income, notes):
        ch = Report()
        ch.createFeeReport(
            validfromdate=validfromdate, 
            receiver=receiver, 
            fees=calcfees,
            income=income, 
            notes=notes
        )

    def DialogChildPopulate(self, arg1):
        data = self.db.getchild(arg1)
        parents = self.db.getparents(arg1)
        rulings = self.db.getrulings(arg1)
        pub.sendMessage('dialog.child.populate', data=data, parents=parents, rulings=rulings) #@UndefinedVariable
        
    def DialogParentPopulate(self):
        self.adults = self.db.getadults()
        pub.sendMessage('dialog.parent.populate', data=self.adults) #@UndefinedVariable
        
    def DialogChildNewParent(self, data):
        pub.sendMessage('dialog.child.newparent', data=data) #@UndefinedVariable

    def StoreChild(self, data, parents, rulings):
        self.db.setchild(data, parents, rulings)
        children = self.db.getchildren()
        pub.sendMessage('main.populate.children', children=children) #@UndefinedVariable
    
    def DialogPreferencesPopulate(self):
        dct = {}
        cfg = Preferences()
        dct['dbfile'] = cfg.GetProperty('sqlite', 'dbfile')
        pub.sendMessage('dialog.preferences.populate', data=dct) #@UndefinedVariable
        
    def StorePreferences(self, data):
        cfg = Preferences()
        cfg.SetProperty('sqlite', 'dbfile', data['dbfile'])
        cfg.WriteConfig()
        
    def DeleteAdult(self, person_id):
        self.db.deleteadult(person_id)
        adults = self.db.getadults()
        pub.sendMessage('main.populate.adults', adults=adults) #@UndefinedVariable
        
    def DeleteChild(self, person_id):
        self.db.deletechild(person_id)
        children = self.db.getchildren()
        pub.sendMessage('main.populate.children', children=children) #@UndefinedVariable
        
    def DialogAdultFillCB(self):
        '''Get look-up values from database and send data to editadultframe to fill comboboxes'''
        dct = {}
        dct['fontype'] = self.db.getlookup('l_fonnumbertypes')
        dct['incometype'] = self.db.getlookup('l_incometypes')
        pub.sendMessage('editadultframe.fillcomboboxes', dct=dct) #@UndefinedVariable

    def DialogChildFillCB(self):
        '''Get look-up values from database and send data to editadultframe to fill comboboxes'''
        dct = {}
        dct['year'] = self.db.getlookup('l_year')
        dct['ruling'] = self.db.getlookup('l_rulings')
        dct['relation'] = self.db.getlookup('l_relations')
        pub.sendMessage('editchildframe.fillcomboboxes',  dct=dct) #@UndefinedVariable
        
    def CreateQuarterAnnouncement(self, date):
        setattr(self.db, 'querydate', date)
        isodate = '{:%Y-%m-%d}'.format(date)
        children = self.db.getchildren_for_quarterannouncement(isodate)
        ch = Report()
        ch.createQAReport(children, isodate)


        

            


        


        