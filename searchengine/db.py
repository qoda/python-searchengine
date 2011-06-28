#!/usr/bin/env python

from searchengine.logger import Logging
from searchengine.settings import DATABASES

class Database(object):
    """
    Object to connect to mysql and sqlite databases and execute queries.
    Connections should be closed after use.
    """
    def __init__(self, *args, **kwargs):
        self.db_driver = None
        self.db_settings = DATABASES[kwargs.get('db_settings', 'main')]
        
        # instantiate logging object
        self.log = kwargs.get('log', Logging())
        
        # database connection settings
        self.db_host = kwargs.get('db_host', self.db_settings['DB_HOST'])
        self.db_type = kwargs.get('db_type', self.db_settings['DB_TYPE'])
        self.db_name = kwargs.get('db_name', self.db_settings['DB_NAME'])
        self.db_username = kwargs.get('db_username', self.db_settings['DB_USERNAME'])
        self.db_password = kwargs.get('db_password', self.db_settings['DB_PASSWORD'])
        
        # instantiate the cursor and connection objects
        self.connection = self.connection()
        self.cursor = self.connection.cursor()
        if self.db_type == "sqlite":
            self.cursor.row_factory = self._dict_factory
        
    def _dict_factory(self, cursor, row):
        """
        A results dict method to output results in a valid python dict rather
        than a tuple.
        """
        result_dict = {}
        [result_dict.update({c[0]: row[i]}) for i, c in enumerate(self.cursor.description)]
        return result_dict
        
    def connection(self):
        """
        Connect to the select database type and return the connection object.
        """
        # connect to a local sqlite database
        if self.db_type == "sqlite":
            import sqlite3
            
            # connect to the sqlite database
            return sqlite3.connect(self.db_name)
        
        # connect to a mysql database
        elif self.db_type == 'mysql':
            import MySQLdb
            from MySQLdb.cursors import DictCursor
            
            # check to ensure all required attributes are available
            required_attrs = ['db_host', 'db_username', 'db_password', 'db_name']
            for attr in required_attrs:
                if not hasattr(self, attr):
                    error_msg = "%s is required to make a connection to a MySQL database." % attr
                    log.error("Database", "connection", error_msg)
                    raise Exception(error_msg)
            
            # connect to the MySQL database
            return MySQLdb.connect(
                host=self.db_host,
                user=self.db_username,
                passwd=self.db_password,
                db=self.db_name,
                cursorclass=DictCursor,
            )
            
        else:
            self.log.error("Database", "connection", "Invaid database type selected.")
            raise Exception("%s is not a valid database type." % self.db_type)
    
    def execute(self, sql, params=()):
        """
        Execute any valid sql query else logs the error and raises a
        ProgrammingError or OperationalError.
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.connection.commit()
            return True
        except self.connection.OperationalError, e:
            self.log.error("Database", "query", e)
            raise self.connection.OperationalError(e)
            self.close()
        except self.connection.ProgrammingError, e:
            self.log.error("Database", "query", e)
            raise self.connection.ProgrammingError(e)
            self.close()
        
        return False
        
    def create_table(self, table_name, schema):
        """
        Create a new database table and associated columns as defined in a
        schema tuple.
        """
        sql = "CREATE TABLE %s (%s)" % (table_name, ", ".join(["%s %s" % (s[0], s[1]) for s in schema]))
        try:
            self.cursor.execute(sql)
            return True
        except self.connection.OperationalError, e:
            self.log.error("Database", "query", e)
        return False
        
    def list(self, sql, params=()):
        """
        Return a list of results based on a valid sql statement.
        """
        if sql.find("SELECT") == 1:
            error_msg = "SQL must contain a SELECT statement."
            log.error("Database", "list", error_msg)
            raise Exception(error_msg)
        if self.execute(sql, params):
            return list(self.cursor.fetchall())
        return []
        
    def get(self, sql, params=()):
        """
        Query the database and return a single result.
        """
        results = self.list(sql, params)
        try:
            return results[0]
        except IndexError:
            return None
            
    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()
