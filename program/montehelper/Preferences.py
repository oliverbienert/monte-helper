'''
Created on Sep 14, 2012

@author: oliver
'''
import ConfigParser
import io
import os
import sys

class Preferences(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Get module directory
        if getattr(sys, 'frozen', None):
            basedir = sys._MEIPASS  #@UndefinedVariable
        else:
            basedir = os.path.dirname(__file__)
        # Get default config file
        default_cfgfile = os.path.join(basedir, 'config/.config')
        homedir = os.path.expanduser('~')
        # Default path for database file. Will be substituded in config file
        defaults = {'homedir':homedir}
        self.config = ConfigParser.ConfigParser(defaults,allow_no_value=True)
        self.config.read(default_cfgfile)
        # Now look for a user saved config file and read it
        mhdir = os.path.join(homedir, '.montehelper')
        if not os.path.exists(mhdir):
            os.makedirs(mhdir)
        self.configfile = os.path.join(mhdir, '.config')
        self.config.read(self.configfile)
        
    def WriteConfig(self):
        with open(self.configfile, 'wb') as configfile:
            self.config.write(configfile)
    
    def GetProperty(self, section, propkey):
        return self.config.get(section, propkey)
    
    def SetProperty(self, section, option, value):
        self.config.set(section, option, value)
    
        