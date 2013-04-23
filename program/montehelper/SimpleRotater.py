'''
Created on Jan 4, 2013

@author: oliver

Parts of code
Copyright (c) 2012 Max Harper
'''

from datetime import datetime
from glob import iglob
import re
import os
import shutil

FILE_NAME_GLOB = '*.backup-*'
FILE_NAME_REGEX = r'backup-(?P<rotation_id>\d+)$'
FILE_NAME_TMPL = ".%(datetime_str)s.backup-%(rotation_id)d"
DATETIME_FORMAT = '%Y-%m-%d-%H%M%S'

class SimpleRotater(object):
    '''
    Rotating file backups (FIFO)
    '''

    def __init__(self, path, num_rotation_slots=3):
        self.path = path
        self.num_rotation_slots = num_rotation_slots
            
    def backup(self):
        "FIFO implementation."
        dir_name, file_name = os.path.split(self.path)
        last_rotation_id = self._most_recent_rotated_file_or_none(self.path)
        next_rotation_id = last_rotation_id + 1 if last_rotation_id is not None else 0
        to_delete = [p for p in self._locate_files_to_delete(self.path, next_rotation_id)]
        # rotate in the new file
        new_file_suffix = FILE_NAME_TMPL % \
            {'datetime_str': datetime.now().strftime(DATETIME_FORMAT), 'rotation_id': next_rotation_id}
        new_path = os.path.join(dir_name, file_name + new_file_suffix)
        shutil.copy(self.path, new_path)
        # remove old files
        for f in to_delete:
            os.remove(f)

    def _id_to_slot(self, rotation_id):
        '''Returns slot number of rotation set'''
        return rotation_id % self.num_rotation_slots

    def _rotated_files(self, path):
        '''Generator. Yields the next rotated file as a tuple: (path, sequence)'''
        for globbed_path in iglob(path + FILE_NAME_GLOB):
            match = re.search(FILE_NAME_REGEX, globbed_path)
            if match:
                yield globbed_path, int(match.group('rotation_id'))
    
    def _most_recent_rotated_file_or_none(self, path):
        '''Looks for rotater generated files in the passed-in path, returns the maximum rotation_id found.'''
        rotated_files = [(path, rotation_id) for (path, rotation_id) in self._rotated_files(path)]
        if not rotated_files:
            return None
        else:
            highest_rotated_file = max(rotated_files, key=lambda x: x[1])
            return highest_rotated_file[1]

    def _locate_files_to_delete(self, path, rotation_id):
        '''Looks for rotater generated files that occupy the same slot that will be given to rotation_id.'''
        rotation_slot = self._id_to_slot(rotation_id)
        for a_path, a_rotation_id in [(p, n) for (p, n) in self._rotated_files(path)]:
            if rotation_slot == self._id_to_slot(a_rotation_id):
                yield a_path

