'''
Created on Jan 3, 2013

@author: oliver
'''
import unittest
import tempfile
import os
import glob
import errno
import versionedfile as v

class Test(unittest.TestCase):
    """Unit tests for montehelper"""
    def setUp(self):
        self.testfilename = None
        self._gettmpfile()
        self.vfile = v.VersionedOutputFile(self.testfilename)
        
    def test_backup(self):
        """Tests method backup of class VersionedOutputFile"""
        i = 1
        while i < 10:
            self.vfile.backup()
            i += 1
        # Now there should be just four versions of TestFile.txt:
        expectedSuffixes = ["", ".~7~", ".~8~", ".~9~"]
        self._checkfiles(expectedSuffixes)
        
    def _checkfiles(self, expectedSuffixes):
        expectedVersions = []
        for suffix in expectedSuffixes:
            expectedVersions.append("%s%s" % (self.testfilename, suffix))
        expectedVersions.sort()
        matchingFiles = glob.glob("%s*" % self.testfilename)
        matchingFiles.sort()
        for filename in matchingFiles:
            self.failUnless(filename in expectedVersions, "Found unexpected file %s.\n" % filename) 
            expectedVersions.remove(filename)
        self.failIf(expectedVersions, "Not found expected file\n:%s" % "\n".join(expectedVersions))
    
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
