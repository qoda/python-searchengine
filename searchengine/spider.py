#!/usr/bin/env python

import optparse
from urlparse import urlparse, urljoin

from searchengine.db import MongoDB
from searchengine.logger import Logging
from searchengine.scraper import HTMLScraper

class Spider(object):
    """
    Simple spider which uses your existing url collection to spider and look
    for new urls.
    """
    def __init__(self, *args, **kwargs):
        self.log = kwargs.get('log', Logging(verbose=kwargs.get('verbose', False)))
        self.database = kwargs.get('database', MongoDB(collection_name="crawler_urls"))
        self.scraper = kwargs.get('database', MongoDB(collection_name="crawler_urls"))
        
    def get_links(self, url):
        """
        Use the scraper class to scrape the links for the given url.
        """
        scraper = HTMLScraper(url=url)
        links = [link[1] for link in scraper.get_content()['links']]
        return links
    
    def is_external_link(self, base_url, url):
        """
        Test if the link is an external link.
        """
        return urlparse(base_url).hostname == urlparse(url).hostname
    
    def run(self):
        """
        Get a list of current urls, spider each url independantly to look for
        more urls to add to the database.
        """
        new_url_count = 0
        obj_list = [obj for obj in self.database.find()]
        if not obj_list:
            self.log.error("Spider", "run", "No urls found to spider.")
            
        # start spidering the urls
        self.log.info("Spider", "run", "Started spidering %s sites for new urls" % len(obj_list))
        for obj in obj_list:
            links = self.get_links(obj['url'])
            for link in links:
                
                # ensure the full url is used rather than the relative link
                if not link.startswith("http"):
                    link = urljoin(obj['url'], link)
                
                # check the link has not already been added, else add it
                if link not in obj['sub_urls'] and not self.is_external_link(obj['url'], link):
                    self.log.info("Spider", "run", "Found new internal url for %s: %s" % (obj['url'], link))
                    new_url_count += 1
                    obj['sub_urls'].append(link)
                    self.database.update(query_data={'_id': obj['_id']}, data={'sub_urls': obj['sub_urls']})
                    
                # if its an external link add it to the database
                elif self.is_external_link(obj['url'], link):
                    self.log.info("Spider", "run", "Found new external url: %s" % link)
                    new_url_count += 1
                    self.database.insert({
                        'url': link,
                        'last_crawled': None,
                        'valid': True,
                        'sub_urls': [],
                    })
        
        self.log.info("Spider", "run", "Spidering %s sites completed. %s new urls found." % new_url_count)

if __name__ == '__main__':
    
    # parse through the system arguments
    usage = "Usage: %prog [options]"
    parser = optparse.OptionParser()
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="set the application verbosity")
    options, args = parser.parse_args()
    
    spider = Spider(**options.__dict__)
    spider.run()
    
