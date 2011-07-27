#!/usr/bin/env python

# TODO: Write tests

import optparse
import time

from searchengine.db import MongoDB
from searchengine.search import SearchIndex

class Profile(object):
    """
    Simple profiler which returns number of indexed urls and average search
    speed.
    """
    def get_num_items(self):
        """
        Get the number of indexed items.
        """
        search_index = SearchIndex()
        print "Number of indexed items: %s" % search_index.index_obj.doc_count()
        search_index.close()
    
    def get_num_indexed_urls(self):
        """
        Get the number of indexed urls.
        """
        database = MongoDB(collection_name="crawler_urls")
        print "Number of indexed urls being crawled: %s" % database.collection.find().count()
    
    def get_search_speed(self):
        """
        Get the average speed at which searches are performed over a predefined
        list of random keywords.
        """
        search_index = SearchIndex()
        result_time = []
        for q in ['dog', 'cat', 'website', 'news', 'social']:
            start_time = time.clock()
            results = search_index.search(q)
            end_time = time.clock()
            result_time.append(end_time - start_time)
        
        search_index.close()
        print "Average search speed: %s secs" % (round(sum(result_time) / len(result_time), 2))
    
if __name__ == '__main__':
    
    # parse through the system arguments
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser()
    parser.add_option("-n", "--num-items", dest="num_items", action="store_true", default=False, help="output the number of indexed items")
    parser.add_option("-u", "--num-urls", dest="num_urls", action="store_true", default=False, help="output the number of indexed urls being crawled")
    parser.add_option("-s", "--search-speed", dest="search_speed", action="store_true", default=False, help="output the average speed at which searches are performed")
    parser.add_option("-a", "--all", dest="all", action="store_true", default=False, help="output all profiled values")
    options, args = parser.parse_args()
    
    profiler = Profile()
    
    # output the profile result depending on the options
    if options.num_items or options.all:
        profiler.get_num_items()
    
    if options.num_urls or options.all:
        profiler.get_num_indexed_urls()
        
    if options.search_speed or options.all:
        profiler.get_search_speed()
