#!/usr/bin/env python

import os
import optparse

class Crawler(object):
    """
    Simple crawler which crawls all urls in the crawler_url collection.
    """
    def __init__(self, *args, **kwargs):
        self.log = kwargs.get('log', Logging(verbose=kwargs.get('verbose', False)))
        self.file_path = kwargs.get('file_path', None)
        self.test_exists = kwargs.get('test_exists', False)
        self.database = kwargs.get('database', MongoDB(
            collection_name="crawler_urls",
            unique_indexes=['url'],
        ))
        
if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()
    
