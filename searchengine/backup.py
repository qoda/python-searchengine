#!/usr/bin/env python

import os
import tarfile
import time

from searchengine.logger import Logging
from searchengine.settings import BACKUP_PATH, DATABASES, INDEX_PATH

class Backup(object):
    """
    Copies and compresses the search index and sqlite database and save to a
    predetermined path.
    """
    def __init__(self, *args, **kwargs):
        self.backup_path = kwargs.get('backup_path', BACKUP_PATH)
        self.index_path = kwargs.get('index_path', INDEX_PATH)
        self.database_path = kwargs.get('database_path', DATABASES['local']['DB_NAME'])
        self.log = kwargs.get('log', Logging(verbose=True))

    def compress(self, path):
        """
        Compress the file/dir prior to saving it.
        """
        
        # create and open the tar file 
        tar_path = os.path.join(
            self.backup_path,
            "%s_%s.tar.gz" % (
                os.path.split(path)[-1],
                time.strftime("%Y%m%d_%H%M%S", time.localtime())
            )
        )
        print tar_path
        tar_buffer = tarfile.open(tar_path, "w:gz")
        
        # write the file/s to tar buffer
        if os.path.isdir(path):
            for name in os.listdir(path):
                tar_buffer.add(os.path.join(path, name))
        else:
            tar_buffer.add(path)
        
        # close tar buffer
        tar_buffer.close()
        
    def save(self):
        """
        Save the compressed file to the specified path.
        """
        self.log.info("Backup", "save", "Backing up index file.")
        self.compress(self.index_path)
        self.log.info("Backup", "save", "Backing up database file.")
        self.compress(self.database_path)

if __name__ == '__main__':
    backup = Backup()
    backup.save()
