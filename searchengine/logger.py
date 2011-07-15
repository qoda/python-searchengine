#!/usr/bin/env python

import logging
import os

from searchengine.settings import LOG_FILE_NAME, LOG_FORMAT, LOG_PATH, DEBUG

class Logging(object):
    """
    Global logging method. Saved to path as defined in setting.LOG_PATH and
    settings.LOG_FILE_NAME.
    """
    def __init__(self, *args, **kwargs):
        self.path = kwargs.get('path', LOG_PATH)
        self.log_format = kwargs.get('log_format', LOG_FORMAT)
        self.log_file_name = kwargs.get('log_file_name', LOG_FILE_NAME)
        self.log_file = os.path.join(self.path, self.log_file_name)
        self.debug = kwargs.get('debug', DEBUG)
        self.verbose = kwargs.get('verbose', False)
        
        # setup the logger object
        logging.basicConfig(filename=self.log_file, format=self.log_format)
    
    def log(self, cls_name, method_name, message, type):
        """
        Instantiate the logger obj and log to file depending on the msg type.
        """
        logger = logging.getLogger("%s.%s" % (cls_name, method_name))
        
        # print the message out if the logger is set to be verbose
        if self.verbose:
            print "%s: [%s.%s()] %s" % (type.upper(), cls_name, method_name, message)
        
        # add extra params
        extras = {
            'class': cls_name,
            'method': method_name,
        }
        
        # determine the logging type and set as required - options are info, warning, error
        if type == 'info':
            if self.debug:
                logger.setLevel(logging.INFO)
                logger.info(message, extra=extras)
                
        elif type == 'warning':
            logger.setLevel(logging.WARNING)
            logger.warning(message, extra=extras)
            
        elif type == 'error':
            logger.setLevel(logging.ERROR)
            logger.error(message, extra=extras)
            raise Exception("%s: %s" % (type.upper(), message))
            
        elif type == 'critical':
            logger.setLevel(logging.CRITICAL)
            logger.critical(message, extra=extras)
            raise Exception("%s: %s" % (type.upper(), message))
    
    def info(self, cls_name, method_name, message):
        self.log(cls_name, method_name, message, type='info')
    
    def warning(self, cls_name, method_name, message):
        self.log(cls_name, method_name, message, type='warning')
    
    def error(self, cls_name, method_name, message):
        self.log(cls_name, method_name, message, type='error')
    
    def critical(self, cls_name, method_name, message):
        self.log(cls_name, method_name, message, type='critical')
