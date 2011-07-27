#!/usr/bin/env python

import os
import optparse

class SearchEngine(object):
    """
    
    """
    
    def __init__(self, *args, **kwargs):
        pass
    
        
def searchengine(query, *args, **kwargs):
    search_engine = SearchEngine(*args, **kwargs)
    search_engine.search(query)
    
if __name__ == '__main__':
    
    # parse through the system argumants
    usage = "Usage: %prog [options] query"
    parser = optparse.OptionParser()
    
    options, args = parser.parse_args()
    
    # ensure the query argument has been passed, else fail
    try:
        query = args[0]
    except IndexError:
        exit(usage)
    
    # call the main method with parsed argumants
    searchengine(query, *args, **options.__dict__)
    
