NB: NO LONGER UNDER DEVELOPMENT
===============================


python-searchengine
===================
A simple search engine which utilises whoosh, a custom html scraper and simple
crawler/spider.

Requirements
------------

System:
~~~~~~~

- python 2.6+

Python:
~~~~~~~

- whoosh
- pymongo

Installation
------------

1. From git::

    $ git clone git@github.com:qoda/python-searchengine.git
    $ cd python-searchengine
    $ python setup.py install

Usage
-----

Simple Usage::
~~~~~~~~~~~~~~

1. Use from class::
    
    from searchengine import SearchEngine
    
    search_engine = SearchEngine()
    search_engine.search('"Python Search Engine" GitHub -bitbucket')
        
2. Use from method::
        
    from searchengine import searchengine
    
    searchengine(query='"Python Search Engine" GitHub -bitbucket')
        
3. Use from commandline (installed)::
    
    $ python -m searchengine.main '"Python Search Engine" GitHub -bitbucket'
    
Required Arguments:
~~~~~~~~~~~~~~~~~~~

- **query** - query the index

Optional Arguments:
~~~~~~~~~~~~~~~~~~~

- **index** (default: /path/to/app/index)
