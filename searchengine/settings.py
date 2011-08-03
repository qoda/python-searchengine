#!/usr/bin/env python

"""
A list of all required settings as employed by most modules and classes in the
application.
"""

import os

# debug mode setting - logs info msgs
DEBUG = True

# mongodb settings
MONGO_NAME = "searchengine"
MONGO_HOST = "qoda-macbook.local"
MONGO_PORT = 27017

# url connection settings
CONNECTION_TIMEOUT = 15

# whoosh index settings
INDEX_PATH = "/tmp/searchengine"

# spider settings
MAX_SPIDER_PROCESSES = 10

# crawler settings
CRAWL_DEPTH = 3

# logging settings
LOG_PATH = "/tmp/"
LOG_FORMAT = "%(levelname)s [%(class)s.%(method)s]: %(message)s (%(asctime)-15s)"
LOG_FILE_NAME = "searchengine.log"

# general settings
MAX_PROCESS_RECURSION = 3
