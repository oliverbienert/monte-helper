'''
Created on Aug 31, 2012

@author: oliver
'''
import bisect
from collections import defaultdict
from Helpers import Helpers

class CalcFee(Helpers):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        Helpers.__init__(self)
        self.adult = defaultdict(dict)
        self.child = defaultdict(dict)
        self.totalincome = 0
        self.lenAdults = 0
        self.hhsize = 0
        self.reduction2 = 0
        self.payer = None
        
    def calc(self, adults, children, fees):
        self.fees = fees
        self.__totals(adults)
        self.__reduction2(adults, len(children))
        self.__fee(children)
        dct = {}
        dct['adults'] = [item for item in self.adult.values()]
        dct['children'] = [item for item in self.child.values()]
        dct['payer'] = self.payer
        return dct
        
    def __totals(self, adults):
        adult_ids = []
        for line in adults:
            adult_id = line['adult_id']
            # Collect adult_id's
            if (adult_id in adult_ids) == False:
                adult_ids.append(adult_id)
                # Initialize total income for this adult
                self.adult[adult_id]['totalincome'] = 0
            try:
                # Check if a value for householdsize has been inserted
                hhsize = int(line['size'])
                if hhsize > self.hhsize:
                    self.hhsize = hhsize
            except (ValueError, TypeError):
                pass
            # If income type is 'less', substract value from total
            if (line['incometype_id'] == 'less'):
                self.adult[adult_id]['totalincome'] -= line['income']
            else:
                self.adult[adult_id]['totalincome'] += line['income']
            # income type and value
            self.adult[adult_id][line['incometype_id']] = line['income']
            self.adult[adult_id]['name'] = line['name']
            self.adult[adult_id]['firstname'] = line['firstname']
            # Check if payer flag is set
            pay = True if line['flags'] & (1 << 1) else False
            # If flag payer has been defined, usae this adult
            # as the payer
            if pay:
                self.payer = adult_id
            # If no payer has been defined, use this adult
            if self.payer == None:
                self.payer = adult_id 
        self.lenAdults = len(adult_ids)
        self.totalincome = sum(value.get('totalincome', 0) for value in self.adult.values())
    
    def __reduction2(self, adults, lenChildren):
        '''
        Compute reduction:
        5 percent for each additional child of household
        not in this school or Kita
        '''
        total = self.lenAdults + lenChildren
        if total < self.hhsize:
            addHouseholdMembers = self.hhsize - total
            # 5% reduction per additional household member not in school
            self.reduction2 = addHouseholdMembers * 0.05
            
    def __fee(self, children):
        '''
        Calc fee for each child
        '''
        reduction1 = 0
        for line in children:
            child_id = line['child_id']
            income = self.totalincome
            self.child[child_id]['income'] = income
            try:
                cb = int(line['benefit'])
                self.child[child_id]['benefit'] = cb
                income += cb
            except (ValueError, TypeError):
                pass
            # 20 % reduction for each further child
            income *= 1 - reduction1
            self.child[child_id]['reduction1'] = reduction1
            
            reduction1 += 0.2
            income *= 1 - self.reduction2
            self.child[child_id]['reduction2'] = self.reduction2
            year = line['year_id']
            # Now compute the column to look-up the fee at
            if year > 0:
                col = 3
            else:
                col = 1   
                if line['exdt'] == 1:
                    # extended day time (more than 6 hours)
                    col += 1
            self.child[child_id]['extendeddaytime'] = line['exdt']
            pos = bisect.bisect_right(self.fees, (income,))
            self.child[child_id]['incomeapplied'] = income
            self.child[child_id]['fee'] = self.fees[pos][col]
            self.child[child_id]['name'] = line['name']
            self.child[child_id]['firstname'] = line['firstname']
            
            


            

                
            