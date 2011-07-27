#!/usr/bin/env python

from hashlib import md5
import optparse
import os
import time

from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh import qparser
from whoosh.store import LockError

from searchengine.logger import Logging
from searchengine.settings import INDEX_PATH

class SearchIndex(object):
    """
    Object utilising Whoosh (http://woosh.ca/) to create a search index of all
    crawled rss feeds, parse queries and search the index for related mentions.
    """
    def __init__(self, *args, **kwargs):
        """
        Instantiate the whoosh schema and writer and create/open the index.
        """
        self.schema = kwargs.get('schema', Schema(
            content_id=ID(stored=True, unique=True),
            content=TEXT(),
        ))
        self.log = kwargs.get('log', Logging())
        
        # get the absolute path and create the dir if required
        self.index_path = kwargs.get('index_path', INDEX_PATH)
        if self.create(self.index_path):
            self.log.info("SearchIndex", "__init__", "New index created.")
        
        # create an index obj and buffered writer
        self.index_obj = open_dir(self.index_path)
    
    def create(self, path):
        """
        Create the index directory if it hasn't already been created.
        """
        if not os.path.exists(path):
            os.mkdir(path)
            create_in(self.index_path, self.schema)
            return True
        return False
        
    def commit(self, writer):
        """
        Commit the data to index.
        """
        try:
            writer.commit()
            return True
        except LockError, e:
            self.log.warning("SearchIndex", "commit", e)
            time.sleep(0.5)
            self.commit(writer)
        
    def add(self, *args, **kwargs):
        """
        Add an item to the index. If commit is set to False, remember to commit
        the data to the index manually using self.commit().
        """
        # instantiate the writer
        try:
            writer =  self.index_obj.writer()
        except LockError:
            self.log.warning("SearchIndex", "commit", "Index returned a LockError")
            time.sleep(0.5)
            self.add(*args, **kwargs)
        
        # check that the correct kwargs have been given
        for k in kwargs.keys():
            if not k in self.schema:
                self.log.error("SearchIndex", "add", "'%s' doesn't match the default scheam fields." % k)
        
        # add the document to the search index and commit
        writer.add_document(
            content_id=kwargs['content_id'],
            content=kwargs['content']
        )
        self.commit(writer)
    
    def get(self, id):
        """
        Get an index object by its hashed id.
        """
        searcher = self.index_obj.searcher()
        result = searcher.document(content_id=unicode(id))
        searcher.close()
        return result
    
    def parse_query(self, query):
        """
        Parses the the string query into a usable format.
        """
        try:
            query = unicode(query)
        except UnicodeDecodeError:
            query = ""
        parser = qparser.QueryParser("content", self.index_obj.schema)
        
        return parser.parse(query)
    
    def search(self, query):
        """
        Search the index and return the results list to be processed further.
        """
        searcher = self.index_obj.searcher()
        
        # create a results list from the search results
        results = []
        for result in searcher.search(self.parse_query(query)):
            results.append(dict(result))
        searcher.close()
        return results
    
    def close(self):
        """
        Closes the searcher obj. Must be done manually.
        """
        self.index_obj.close()
