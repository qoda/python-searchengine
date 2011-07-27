#!/usr/bin/env python

import httplib
import optparse
import os
import urlparse

from searchengine.db import MongoDB
from searchengine.logger import Logging
from searchengine.settings import CONNECTION_TIMEOUT

class SyncDB(object):
    """
    Sync the database with a predefined list of urls to crawl. This needs to be
    a comma-delimited text file, see the example file in samples/syncdb.txt.
    """
    def __init__(self, *args, **kwargs):
        self.log = kwargs.get('log', Logging(verbose=kwargs.get('verbose', False)))
        self.retry_failed = kwargs.get('retry_failed', 0)
        self.file_path = kwargs.get('file_path', None)
        self.test_exists = kwargs.get('test_exists', False)
        self.database = kwargs.get('database', MongoDB(
            collection_name="crawler_urls",
            unique_indexes=['url'],
        ))
        
    def exists(self, url):
        """
        Open the url connection and poll the HEAD to see if the correct
        response is returned.
        """
        url = urlparse.urlparse(url)
        connection = httplib.HTTPConnection(url.hostname, timeout=CONNECTION_TIMEOUT)
        
        try:
            connection.request("HEAD", url.geturl())
            response = connection.getresponse()
        except:
            return False
        
        if str(response.status)[0] not in ["2", "3"]:
            return False
        
        connection.close()
        return True
        
    def save(self, url):
        """
        Save the url to the database and crawler collection.
        """
        self.database.insert({
            'url': url,
            'last_crawled': None,
            'valid': True,
            'sub_urls': [],
        })
    
    def run(self, valid_urls=[], invalid_urls=[]):
        """
        Iterate through the urls and add them to the database to be crawled,
        testing if they exists if required.
        """
        self.log.info("SyncDB", "run", "Syncing to database from %s started." % self.file_path)
        
        # open the file or raise exception if it doesn't exist
        try:
            file_buffer = open(self.file_path)
        except IOError:
            self.log.error("SyncDB", "run", "Sync file path not set or can't be found.")
        
        # instantiate the url to be processed
        if not invalid_urls:
            url_list = file_buffer.readlines()
        else:
            url_list = invalid_urls
            invalid_urls = []
        
        # iterate through the url list, test if the file exists and save to the database
        for url in url_list:
            
            # clean up the url
            url = url.strip()
            
            valid = True
            if self.test_exists:
                valid = self.exists(url)
                if not valid:
                    invalid_urls.append(url)
            if valid:
                valid_urls.append(url)
            
            # save the valid url to the database
            self.save(url)
            self.log.info("SyncDB", "run", "Saved: %s" % url)
        
        # handle invalid urls and retry depending on users choice
        if invalid_urls and  self.retry_failed:
            while i > self.retry_failed:
                self.retry_failed -= 1
                self.run(valid_urls, invalid_urls)
        else:
            self.log.info("SyncDB", "run", "Completed. %s urls added." % len(valid_urls))
    
if __name__ == '__main__':
    
    # parse through the system arguments
    usage = "Usage: %prog [options] filepath"
    parser = optparse.OptionParser()
    parser.add_option("-t", "--test-exists", dest="test_exists", action="store_true", default=False, help="test that each url exists")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="set the application verbosity")
    parser.add_option("-f", "--retry-failed", dest="retry_failed", default=0, type="int", help="number of times to retry saving a failed url")
    options, args = parser.parse_args()
    
    # check that the file path has been sent
    try:
        options.file_path = args[0]
    except IndexError:
        exit(usage)
    
    # sync the database
    sync = SyncDB(**options.__dict__)
    sync.run()
