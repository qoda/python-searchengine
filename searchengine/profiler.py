#!/usr/bin/env python

# TODO: Write tests

import optparse
import time

from rsscrawler.db import Database
from rsscrawler.search import SearchIndex

class Profile(object):
    """
    Simple index profiler which returns number of index items, search speed and
    number of urls being indexed.
    """
    def __init__(self, *args, **kwargs):
        self.database = kwargs.get('database', Database())
        self.search_index = kwargs.get('search_index', SearchIndex())
    
    def get_num_items(self):
        """
        Get the number of indexed items.
        """
        print "Number of indexed items: %s" % self.search_index.index_obj.doc_count()
    
    def get_indexed_urls(self):
        """
        Get the number of currently indexed and valid urls.
        """
        print "Number of indexed urls: %s" % len(self.database.list("SELECT id FROM global_rss WHERE valid = 1"))
    
    def get_search_speed(self):
        """
        Get the average speed at which searches are performed over a predefined
        list of random keywords.
        """
        result_time = []
        for q in ['vodacom', 'investec rugby', 'investec -rugby', 'news', 'finance']:
            start_time = time.clock()
            results = self.search_index.search(q)
            end_time = time.clock()
            result_time.append(end_time - start_time)
        
        print "Average search speed: %s secs" % (round(sum(result_time) / len(result_time), 2))
        
    def close(self):
        """
        Close the database connection and search index.
        """
        self.database.close()
        self.search_index.close()
    
if __name__ == '__main__':
    
    # parse through the system arguments
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser()
    parser.add_option("-n", "--num-items", dest="num_items", action="store_true", help="output the number of indexed items")
    parser.add_option("-i", "--indexed-urls", dest="indexed_urls", action="store_true", help="output the number of currently indexed urls")
    parser.add_option("-s", "--search-speed", dest="search_speed", action="store_true", help="output the average speed at which searches are performed")
    parser.add_option("-a", "--all", dest="all", action="store_true", default=True, help="output all profiled values")
    options, args = parser.parse_args()
    
    profiler = Profile()
    
    # output the profile result depending on the options
    if options.num_items or options.all:
        profiler.get_num_items()
    
    if options.indexed_urls or options.all:
        profiler.get_indexed_urls()
        
    if options.search_speed or options.all:
        profiler.get_search_speed()
        
    # close all connections
    profiler.close()
