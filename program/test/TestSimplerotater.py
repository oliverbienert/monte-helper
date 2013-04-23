'''
Created on Jan 3, 2013

@author: oliver
'''
import unittest
import tempfile
import os
import glob
import errno
from SimpleRotater import SimpleRotater

class Test(unittest.TestCase):
    """Unit tests for montehelper"""
    def setUp(self):
        self.testfilename = None
        self._gettmpfile()
        self.sfile = SimpleRotater(self.testfilename)
        
    def test_backup(self):
        """Tests method backup of class SimpleRotater"""
        i = 0
        while i < 10:
            self.sfile.backup()
            i += 1
        # Now there should be just four versions of the temporary testfile:
        expectedSuffixes = [".txt", ".backup-7", ".backup-8", ".backup-9"]
        self._checkfiles(expectedSuffixes)

    def _checkfiles(self, expectedSuffixes):
        matchingFiles = glob.glob("%s*" % self.testfilename)
        matchingFiles.sort()
        for filename in matchingFiles:
            suffix = os.path.splitext(filename)[1]
            self.failUnless(suffix in expectedSuffixes, "Found unexpected file %s.\n" % filename) 
            expectedSuffixes.remove(suffix)
        self.failIf(expectedSuffixes, "Expected file suffixes not found\n:%s" % "\n".join(expectedSuffixes))
    
    def _gettmpfile(self):
        tmp_dir = tempfile.gettempdir()
        mytmpdir = os.path.join(tmp_dir, '.montehelper')
        try:
            os.makedirs(mytmpdir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                self.fail(exception.errno)
        fh = tempfile.NamedTemporaryFile(dir=mytmpdir, suffix='.txt', delete=False)
        self.testfilename = fh.name
        fh.write("Unit testing")
        fh.close()
            
    def tearDown(self):
        matchingFiles = glob.glob("%s*" % self.testfilename)
        for filename in matchingFiles:
            os.remove(filename)
