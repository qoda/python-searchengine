#!/usr/bin/env python

import optparse
import urlparse

from searchengine.logger import Logging
from searchengine.settings import SYNC_FILE_PATH, CONNECTION_TIMEOUT

class SyncDatabase(object):
    """
    Sync the database with a predefined list of urls to crawl. This needs to be
    a comma-delimited text file, see the example file in samples/syncdb.txt.
    """
    def __init__(self, *args, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        self.log = kwargs.get('log', Logging(verbose=self.verbose))
        self.path = kwargs.get('path', SYNC_FILE_PATH)
        self.test = kwargs.get('test', False)
        
    def exists(self, url):
        host_name = urlparse.urlparse(url)
        connection = httplib.HTTPConnection(self.url.hostname, timeout=CONNECTION_TIMEOUT)
        url_handler = urllib2.urlopen(self.url)
        html_content = url_handler.read()
        url_handler.close()
    
    def run():
        """
        Iterate through the urls and add them to the database to be crawled.
        """
        self.log.info("SyncDatabase", "run", "Syncing to database from %s started." % self.path)
        
        # open the file and add each line to the database
        file_buffer = open(self.path)
        for line in file_buffer.readlines():
            if self.test:
                self.exists(line)
            dosomthing
        
        self.log.info("SyncDatabase", "run", "Syncing to database completed.")
        
        if raw_input("%s urls added, %s urls rejected. Would you like to retry rejected urls (Y|N)?" % success_count, failed_count).lower() == "y":
            dosomthing
    
if __name__ == '__main__':
    
    # parse through the system arguments
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser()
    parser.add_option("-F", "--file-path", dest="path", default=SYNC_FILE_PATH, help="path to sync file")
    parser.add_option("-t", "--test", dest="test", action="store_true", default=False, help="test that each url exists")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="set the application verbosity")
    options, args = parser.parse_args()
    
    # sync the database
    sync = SyncDatabase(path=options.path)
    sync.run()
