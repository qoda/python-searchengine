#!/usr/bin/env python

"""
A list of all required settings as employed by most modules and classes in the
application.
"""

import os

# debug mode setting - logs info msgs
DEBUG = False

# mongodb settings
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "rsscrawlers.sqlite")
SYNC_FILE_PATH = ""

# url connection settings
CONNECTION_TIMEOUT = 30

# whoosh index settings
INDEX_PATH = "/var/whoosh/rssindex"

# crawler settings
CRAWL_DEPTH = 3

# logging settings
LOG_PATH = "/tmp/"
LOG_FORMAT = "%(levelname)s [%(class)s.%(method)s]: %(message)s (%(asctime)-15s)"
LOG_FILE_NAME = "searchengine.log"

# backup settings
BACKUP_PATH = "/var/backups/rsscrawler"

# general settings
MAX_PROCESS_RECURSION = 3
