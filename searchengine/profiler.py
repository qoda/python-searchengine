#!/usr/bin/env python

# TODO: Write tests

import optparse
import time

from searchengine.search import SearchIndex

class Profile(object):
    """
    Simple profiler which returns number of indexed urls and average search
    speed.
    """
    def __init__(self, *args, **kwargs):
        self.search_index = kwargs.get('search_index', SearchIndex())
    
    def get_num_items(self):
        """
        Get the number of indexed items.
        """
        print "Number of indexed items: %s" % self.search_index.index_obj.doc_count()
    
    def get_search_speed(self):
        """
        Get the average speed at which searches are performed over a predefined
        list of random keywords.
        """
        result_time = []
        for q in ['dog', 'cat', 'website', 'news', 'social']:
            start_time = time.clock()
            results = self.search_index.search(q)
            end_time = time.clock()
            result_time.append(end_time - start_time)
        
        print "Average search speed: %s secs" % (round(sum(result_time) / len(result_time), 2))
        
    def close(self):
        """
        Close the database connection and search index.
        """
        self.search_index.close()
    
if __name__ == '__main__':
    
    # parse through the system arguments
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser()
    parser.add_option("-n", "--num-items", dest="num_items", action="store_true", help="output the number of indexed items")
    parser.add_option("-s", "--search-speed", dest="search_speed", action="store_true", help="output the average speed at which searches are performed")
    parser.add_option("-a", "--all", dest="all", action="store_true", default=True, help="output all profiled values")
    options, args = parser.parse_args()
    
    profiler = Profile()
    
    # output the profile result depending on the options
    if options.num_items or options.all:
        profiler.get_num_items()
        
    if options.search_speed or options.all:
        profiler.get_search_speed()
    
    # close all connections
    profiler.close()
