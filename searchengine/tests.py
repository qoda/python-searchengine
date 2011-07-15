#!/usr/bin/env python

import os
import shutil
import time
import unittest
import urllib

from searchengine.db import MongoDB
from searchengine.logger import Logging
from searchengine.main import SearchEngine, searchengine
from searchengine.scraper import HTMLScraper, TagSelector
from searchengine.search import SearchIndex
from searchengine.sync import SyncDB

def dummy_search_index():
    search_index = SearchIndex(
        index_path="test",
        log=Logging(log_file_name="test.log"),
    )
    search_index.add(
        content_id=u'1',
        content=u'Testing ABC',
    )
    search_index.add(
        content_id=u'2',
        content=u'Testing DEF',
    )
    return search_index

def dummy_db(data):
    database = MongoDB(
        log=Logging(log_file_name="test.log"),
        database_name="test_database",
        collection_name="test_collection_content",
        unique_indexes=['text'],
    )
    id = database.insert(data)
    return database, id

class MongoDBTestCase(unittest.TestCase):
    def setUp(self):
        self.data1 = {"text": "ABC", "tags": ["test", "python"]}
        self.database, self.id1 = dummy_db(self.data1)
        self.data2 = {"text": "DEF", "tags": ["test", "mongo"]}
        self.database, self.id2 = dummy_db(self.data2)
        
        # entry should not be created as text is not unique
        self.data3 = {"text": "DEF", "tags": ["python", "mongo_indexing"]}
        self.database, self.id3 = dummy_db(self.data3)
    
    def test_insert(self):
        
        # test that the inserts in setUp return the correct number of entries
        self.assertEqual(self.database.find(self.data1).count(), 1)
        self.assertEqual(self.database.find().count(), 2)
        
        # test the correct indexes were set on the collection
        self.assertTrue(u"text_1" in self.database.collection.index_information().keys())
        
    def test_update(self):
        
        # test updating an entry using the id_obj as a unique identifier
        self.database.update(id_obj=self.id1, data={"text": "CBA"})
        self.assertEqual(self.database.find({"text": "CBA"}).count(), 1)
        
        # test updating an entry using the data as a unique identifier
        self.database.update(query_data={"text": "CBA"}, data={"text": "ABC"})
        self.assertEqual(self.database.find({"text": "ABC"}).count(), 1)
        
    def test_remove(self):
        
        # test removing a single entry using the id_obj param as unique identifier
        self.database.remove(id_obj=self.id1)
        self.assertEqual(self.database.find().count(), 1)
        
        # test removing a single entry using the query_dict param as unique identifier
        self.database.remove(query_data={"text": "DEF"})
        self.assertEqual(self.database.find().count(), 0)
        
    def test_find(self):
        self.assertEqual(self.database.find().count(), 2)
        self.assertEqual(self.database.find({"text": "ABC"}).count(), 1)
    
    def test_get(self):
        entry1 = self.database.get(id_obj=self.id1)
        entry2 = self.database.get(query_data=self.data2)
        
        # test that a single entry dict is returned using a query_dict and id_obj to find one entry
        self.assertEqual(entry1['text'], "ABC")
        self.assertTrue(isinstance(entry1, dict))
        self.assertEqual(entry2['text'], "DEF")
        self.assertTrue(isinstance(entry2, dict))
    
    def tearDown(self):
        self.database.remove()

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.html = """
            <html>
            <head>
                <title>title</title>
            </head>
            <body>
                <div>div<a href="http://www.google.com">link</a></div>
            </body>
            </html>
        """
        self.url = "http://www.google.com"
        self.selector = TagSelector()
        self.scraper = HTMLScraper(url=self.url)
        
    def test_attr_dict(self):
        self.assertEqual(self.selector.attr_dict([]), {})
        self.assertEqual(self.selector.attr_dict([('class', 'test_class')]), {'class': 'test_class'})
    
    def test_tag_selector_handle_starttag(self):
        current_tag = "div"
        current_attrs = [('class', 'test_class')]
        self.selector.handle_starttag(current_tag, current_attrs)
        
        # test the current attrs and tag has been set correctly
        self.assertEqual(self.selector.current_tag, current_tag)
        self.assertEqual(self.selector.current_attrs, self.selector.attr_dict(current_attrs))
        
    def test_tag_selector_get_data(self):
        self.selector.feed(self.html)
        data = self.selector.get_data()
        self.assertEqual(data, {'content': ['title', 'div', 'link'], 'links': [('link', 'http://www.google.com')], 'title': 'title'})
    
    def test_html_scraper_get_url_content(self):
        self.assertNotEqual(self.scraper.get_url_content(), "")
        
    def test_html_scraper_get_content(self):
        content = self.scraper.get_content()
        self.assertNotEqual(content, {})
        self.assertTrue("Google" in content['content'])
        self.assertTrue("Google" in content['title'])
        self.assertEqual(self.url, content['url'])
    
    def tearDown(self):
        pass

class SearchTestCase(unittest.TestCase):
    def setUp(self):
        self.search_index = dummy_search_index()
        
    def test_get(self):
        result = self.search_index.get(1)
        
        # test that an obj is returned by id and is a dict
        self.assertNotEqual(result, {})
        self.assertTrue(isinstance(result, dict))
        
        # test that only one obj is returned
        self.assertEqual(int(result['content_id']), 1)
        
    def test_add(self):
        with self.assertRaises(Exception):
            self.search_index.add(id2=1)
        
    def test_search(self):
        
        # test that the output is not empty
        results = self.search_index.search("ABC")
        self.assertTrue(len(results) > 0)
        self.assertTrue(len(results) <= 1)
        
        # test that the output is empty
        results = self.search_index.search("CBA")
        self.assertEqual(len(results), 0)
        
        # test that the output doesn't contain more than one result
        results = self.search_index.search("ABC")
        self.assertEqual(len(results), 1)
        
        # test that the output contains two results
        results = self.search_index.search("Testing")
        self.assertEqual(len(results), 2)
        
    def tearDown(self):
        shutil.rmtree(self.search_index.index_path)
        self.search_index.close()
        
class SyncDBTestCase(unittest.TestCase):
    def setUp(self):
        self.file_path = "/tmp/test.txt"
        self.syncdb = SyncDB(
            file_path=self.file_path,
            database=MongoDB(
                collection_name='test_collection_urls',
                database_name='test_database',
            ),
            test_exists=True,
        )
        
        # create a dummy file to parse through
        file_buffer = open(self.file_path, "w+")
        file_buffer.write('http://www.google.com \r\n http://www.example.com')
        file_buffer.close()
        
    def test_exists(self):
        
        # test that the url is tested as existing correctly
        self.assertTrue(self.syncdb.exists("http://www.google.com"))
        self.assertFalse(self.syncdb.exists("http://www.g.com"))
        
    def test_run(self):
        
        # test that the url is added to the db and the file is parsed correctly
        self.syncdb.run()
        self.assertEqual(self.syncdb.database.find().count(), 2)
    
    def tearDown(self):
        self.syncdb.database.remove()
        os.remove(self.file_path)

if __name__ == '__main__':
    unittest.main()
