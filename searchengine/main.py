#!/usr/bin/env python

import os
import optparse

class SearchEngine(object):
    """
    
    """
    
    def __init__(self, *args, **kwargs):
        pass
    
        
def searchengine(*args, **kwargs):
    wkhp = SearchEngine(*args, **kwargs)
    
if __name__ == '__main__':
    
    # parse through the system argumants
    usage = "Usage: %prog [options] url output_file"
    parser = optparse.OptionParser()
    
    parser.add_option("-F", "--flash-plugin", action="store_true", dest="flash_plugin", default=True, help="use flash plugin")
    parser.add_option("-J", "--disable-javascript", action="store_true", dest="disable_javascript", default=False, help="disable javascript")
    parser.add_option("-b", "--no-background", action="store_true", dest="no_background", default=False, help="do not print background")
    parser.add_option("-g", "--grayscale", action="store_true", dest="grayscale", default=False, help="make grayscale")
    parser.add_option("-d", "--redirect-delay", dest="delay", default=0, help="page delay before convertion")
    parser.add_option("-O", "--orientation", dest="orientation", default='Portrait', help="page orientation")
    parser.add_option("-D", "--dpi", dest="dpi", default=100, help="print dpi")
    parser.add_option("-U", "--username", dest="http_username", default="", help="http username")
    parser.add_option("-P", "--password", dest="http_password", default="", help="http password")
    
    options, args = parser.parse_args()
    
    # call the main method with parsed argumants
    searchengine(*args, **options.__dict__)
    
