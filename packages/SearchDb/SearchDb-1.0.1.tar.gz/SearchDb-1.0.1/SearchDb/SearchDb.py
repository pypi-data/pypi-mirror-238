"""
SearchDB is a dict like object that is backed by SQLite
With the .search* functions it enables you to use fast text search, i.e. a lightweight search engine.

"""

import json
import atexit
import sqlite3
from binascii import crc32
from typing import List, Dict, Union, Iterable, Tuple

__version__ = '1.0.1'

class SearchDbInit:
    """
    Main SearchDb class with information about SQLite database
    """

    def __init__(self, db_file_path: str, key_int=False, thread_unsafe=False):
        self.file_path = db_file_path
        if thread_unsafe:  # yolo
            self.connection: sqlite3.Connection = sqlite3.connect(self.file_path, isolation_level=None, check_same_thread=False)
        else:
            self.connection: sqlite3.Connection = sqlite3.connect(self.file_path)
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        self.tables: List = []
        self.table_info: Dict = {}
        self.__columns: Dict = {}
        self.__query_column: Union[str, None] = None
        self.__query_data: Union[str, None] = None
        self.table_info_update()
        self.table_in_use = "dict"

        # Table Info
        self.__active_table = "dict"
        self.__active_table_key_int = key_int

        # Search table info
        self.search_table_in_use = "textsearch"
        self.search_prevent_duplicate_values = True

        # Multi table info
        self.multi_table_in_use = "multi"

        self.create_database(key_int)
        self.create_search_index()

        atexit.register(self.__exit)

    def __is_sqlite3(self):
        " Check if file is SQLite, this is redundant for now and not used "
        valid = 'SQLite format 3'.encode()
        if open(self.file_path, 'rb').read(15) != valid:
            raise IOError("Not an SQLite file")
        return False

    def table_info_update(self):
        ignore_tables_endswith = ("_data", "_idx", "_content", "_docsize", "_config", "_unique")
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
        self.tables = [table[0] for table in self.cursor.fetchall() if not table[0].endswith(ignore_tables_endswith)]
        self.table_info = dict()
        for table in self.tables:
            self.table_info[table] = {}
            self.cursor.execute(f"PRAGMA table_info({table});")
            """cid  name      type           notnull  dflt_value  pk"""
            for column in self.cursor.fetchall():
                self.table_info[table][column[1]] = {"type": column[2], "pk": column[5], "column_id": column[0]}

        " Add column reverse table lookup "
        for table in self.table_info.keys():
            for column in self.table_info[table]:
                if column not in self.__columns:
                    self.__columns[column] = [table]
                else:
                    if table not in self.__columns[column]:
                        self.__columns[column].append(table)

    def create_database(self, key_int=False):
        """
        Creates a table with indexed keys and values.
        Table consists of: key, value, json
            If the value is a dict, list or similar it will get stored in json.
            json is not indexed

        If key_int is set to True then the key will get stored as an Integer
    
        TODO: Rename to create_table
        """

        if key_int:
            key_type = "INTEGER"
        else:
            key_type = "TEXT"
        creation_sql_string = f"""CREATE TABLE IF NOT EXISTS {self.table_in_use} (
                        key {key_type} NOT NULL,
                        value TEXT,
                        json TEXT,
                        UNIQUE(key)
                        );
                      """

        create_index_list = [
            f""" CREATE INDEX IF NOT EXISTS idx_key ON {self.table_in_use} (key ASC);""",
            f""" CREATE INDEX IF NOT EXISTS idx_value ON {self.table_in_use} (value ASC);""",
        ]

        self.cursor.execute("PRAGMA journal_mode = WAL;")
        self.cursor.execute("PRAGMA synchronous = OFF;")
        self.cursor.execute("PRAGMA cache_size = 100000;")
        self.cursor.execute("PRAGMA temp_store = MEMORY;")
        self.cursor.execute("PRAGMA auto_vacuum = FULL;")
        self.cursor.execute(creation_sql_string)
        for item in create_index_list:
            self.cursor.execute(item)

        # Also create text index
        self.create_search_index()

        #self.table_info_update()  # Generate tables


    def create_search_index(self, __table_name=None):
        """
        Creates a Fast Text Search 5 index that allows you to search large text values quickly
        Creates a duplicate index with key and crc32 int of value to prevent duplicates
        """
        if __table_name:
            self.search_table_in_use = __table_name
        self.cursor.execute(f"CREATE VIRTUAL TABLE IF NOT EXISTS {self.search_table_in_use} USING fts5(key, value)")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.search_table_in_use + str('_unique')} ( 
                                key TEXT NOT NULL,
                                crc32 INTEGER,
                                UNIQUE(key)
                                );
                                """)
        self.cursor.execute(
            f"""CREATE INDEX IF NOT EXISTS {"idx_" + self.search_table_in_use + str('_unique_key')} ON {self.search_table_in_use + str('_unique')} (key ASC);""")
        self.cursor.execute(
            f"""CREATE INDEX IF NOT EXISTS {"idx_" + self.search_table_in_use + str('_unique_crc32')} ON {self.search_table_in_use + str('_unique')} (crc32 ASC);""")
        self.table_info_update()  # Generate tables info

    def multi_create_database(self, column_list, custom_unique_columns=None, table_name=None):
        """
        Create a table with many columns, all are indexed (except for json)
        If you need more than a key-value store, use this.

        Let's say you have information of the type: name, phone_nr, address, waist_size, 
        you call the function like this:
            .create_multi_database(["name", "phone_nr", "address", "waist_size"])


        if you want specific datatypes like TEXT, INTEGER and so on, insert a list with tuples instead:
            [("name", "TEXT"), ("phone_nr", "INTEGER")]

        If you want to store python datatypes like list, dict, tuple use "json" as the key-name. [("json", "TEXT")]
        SearchDB will in turn encode and decode the data from and to JSON.
        
        If you want a custom name of the multi database instead of multi use this:
            .multi_table_in_use first (default "multi")

        By default, all items together are considered unique.
        If you want a custom unique combination add a list of those column names to custom_unique_columns when creating the database
            custom_unique_columns=["name", "phone_nr"]

        :return:
        """

        def verify_database():
            """
            Verify that the database does not exist
            """
            self.table_info_update()
            if self.multi_table_in_use in self.tables:
                raise ValueError(f"Database \'{self.multi_table_in_use}\' already exists")

        def validate_list(column_list):
            """
            Formats list, if the list contains tuples of names and datatypes, join the values, otherwise assume all are TEXT

            Difference between STRING and TEXT:
                STRING tries to store integers as integers, it truncates leading zeroes in a string with only numbers
                If you want to store numbers as strings, use TEXT

            INTEGER = int
            REAL = float
            BLOB = binary data
             """
            acceptable_datatypes = ("NULL", "INTEGER", "REAL", "TEXT", "BLOB", "STRING")

            "Check all are strings"
            if all([isinstance(item, str) for item in column_list]):
                return [(item, "TEXT") for item in column_list]

            " Check if all are tuples "
            if all([isinstance(item, tuple) for item in column_list]):
                for item in column_list:
                    if item[1] not in acceptable_datatypes:
                        raise KeyError(
                            """Datatype has to be either of: "NULL", "INTEGER", "REAL", "TEXT", "BLOB", "STRING" """)
                return column_list

            " If values are a mix of strings and other values, raise key error"
            raise KeyError("Insert list of strings or tuples (column_name, datatype)")

        def create_table(_column_list):
            # Create table
            _validated_string_list = ','.join([i[0] + " " + i[1] for i in _column_list])
            if custom_unique_columns:
                _unique_columns = ','.join([column for column in custom_unique_columns])
            else:
                _unique_columns = ','.join([column[0] for column in _column_list])
            self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.multi_table_in_use} ( 
                                {_validated_string_list},
                                UNIQUE({_unique_columns})
                                    );
                                    """)

        def create_indexes(_column_list):
            for column_item in _column_list:
                if column_item[0] != "json":  # Dont index JSON fields
                    self.cursor.execute(
                        f""" CREATE INDEX IF NOT EXISTS {'idx_' + column_item[0]} ON {self.multi_table_in_use} ({column_item[0]} asc);""")

        if table_name:
            self.multi_table_in_use = table_name
        # Execute all
        verify_database()
        try:
            validated_column_list = validate_list(column_list)
        except KeyError as e:  # TODO Pass on error in a nicer way
            raise KeyError(e)
        create_table(validated_column_list)
        create_indexes(validated_column_list)
        self.table_info_update()  # Update list of tables and dict of columns

    def show_columns(self, table_name=None):
        """
        Return a list of columns in selected table
        If no table is selected, will check self.table_in_use

        The columns are returned in the correct order
        """

        if not table_name:
            table_name = self.table_in_use
        if table_name not in self.tables:
            raise ValueError(f"table {table_name} does not exist")

        column_list = list([None]) * len(self.table_info[table_name])
        for column in self.table_info[table_name]:
            column_list[self.table_info[table_name][column]["column_id"]] = column
        return column_list

    def vacuum(self):
        self.connection.commit()  # Commit the latest thing
        self.connection.execute("VACUUM")
        self.connection.commit()

    def merge(self, database_to_merge_path: str, table_name="dict"):
        """
        Will merge database table with another sqlite databases table
        Path to database and table name is required
            The schema has to be the same
        """
        self.connection.execute("ATTACH DATABASE ? AS toMerge", (database_to_merge_path,))
        self.connection.execute("BEGIN")
        self.connection.execute(f"INSERT OR IGNORE INTO {str(table_name)} SELECT * FROM {'toMerge.' + table_name}")
        self.connection.commit()
        self.connection.execute("DETACH toMerge")

    def drop_table(self, table_name: str, confirm=False):
        if not confirm:
            raise SyntaxError("set confirm=true to really wipe table")
        self.connection.execute(f"DROP TABLE {table_name}")  # , (table_name, ))
        self.connection.commit()
        self.table_info_update()

    def __exit(self):
        """
        Cleanup of SQLite when exiting
        """
        self.connection.commit()
        self.connection.close()


class SearchDb(SearchDbInit):

    def key_add(self, key, value, table_name=None):
        """
        Add key and value to the database
        The value can be any regular type or structure like
            * string
            * int
            * dict
            * list
            * set  ( will get returned as list )
            * bool
        """
        if table_name:
            self.table_in_use = table_name
        # self.table_info[self.table_in_use] should return 3 keys
        self.__validate_db_and_key_int(key)  # If table key is INTEGER then key has to be int
        key, value, json_data = self.__key_val_to_key_val_json(key, value)
        self.cursor.execute(f'INSERT OR REPLACE INTO {self.table_in_use} VALUES (?,?,?)', (key, value, json_data))
        self.connection.commit()


    def add_bulk(self, iterator: Iterable, table_name=None):
        """
        Fastest insertion of values, supply an iterator that yields a tuple with key and value

        """

        def iterator_modifier(input_iterator: Iterable):
            """
            Takes an iterator that yields a tuple with two values, return a generator that returns a tuple with three
            values, (key, value, json) where one of value or json needs to be Null.
            """
            for item in input_iterator:
                self.__validate_db_and_key_int(item[0])  # If table key is INTEGER then key has to be int
                yield self.__key_val_to_key_val_json(item[0], item[1])

        def insert(_iterator):
            self.connection.executemany(f'INSERT OR REPLACE INTO {self.table_in_use} VALUES (?, ?, ?)', _iterator)
            self.connection.commit()

        if hasattr(iterator, '__iter__'):
            " Iterator is an interator "
            new_iterator = iterator_modifier(iterator)
            temp_list = []

            if table_name:  # Change table name if set
                self.table_in_use = table_name

            for item in new_iterator:
                temp_list.append(item)
                if len(temp_list) == 100_000:
                    insert(temp_list)
                    temp_list = []
            insert(temp_list)  # Insert the final items

    def get(self, key, table_name=None):
        """
        Returns the value based on the key
        The database returns (key, stringvalue, jsonvalue)
            Either string value or json value can exist
            If string value exists, return
            if json value exists, convert it to a datatype (dict, list, so on and so on) and return
        """
        if table_name:
            self.table_in_use = table_name
        self.cursor.execute(f'SELECT * FROM {self.table_in_use} WHERE key=?', (key,))
        retval = self.cursor.fetchone()
        if retval:
            if retval[1]:  # Retval should consist of tuple with key and value
                return retval[1]
            elif retval[2]:
                return json.loads(retval[2])
        else:
            raise KeyError(f"Key does not exist")

    def value(self, value, table_name=None):
        """Return a list of keys of the selected value"""
        if table_name:
            self.table_in_use = table_name
        self.cursor.execute(f'SELECT key FROM {self.table_in_use} WHERE value=?', (value,))
        recv_values = self.cursor.fetchall()
        if len(recv_values) > 0:
            return [key[0] for key in recv_values]
        raise ValueError(f"No keys with value {value}")


    def keys(self, key_name="key", table_name=None):
        """
        Return all keys
        """
        if table_name:
            self.table_in_use = table_name
        self.cursor.execute(f'SELECT {key_name} FROM {self.table_in_use}')
        for k in self.cursor.fetchall():
            yield k[0]

    def values(self, value_name="value", table_name=None):
        """Return all values"""
        if table_name:
            self.table_in_use = table_name
        self.cursor.execute(f'SELECT {value_name} FROM {self.table_in_use}')
        for v in self.cursor.fetchall():
            yield v[1]

    def pop(self, key, table_name=None):
        """Delete key, return it's value"""
        value = self.get(key, table_name=table_name)
        self.delete(key)
        return value

    def delete(self, key, table_name=None):
        """Delete key without returning value"""
        if table_name:
            self.table_in_use = table_name
        if self.get(key):
            self.cursor.execute(f'DELETE FROM {self.table_in_use} WHERE key=?', (key,))
            self.connection.commit()
        else:
            raise KeyError(f"Key does not exist")

    def delete_value(self, value, table_name=None):
        """Delete a key if the value is correct"""
        # TODO remove this function since it might remove many things?

        if table_name:
            self.table_in_use = table_name

        if self.value(value):
            self.cursor.execute(f'DELETE FROM {self.table_in_use} WHERE value=?', (value,))
            self.connection.commit()
        else:
            raise KeyError(f"No keys with value {value} exist")

    def delete_key_value(self, key, value, table_name=None):
        """Delete a key if the key and value is correct"""

        if table_name:
            self.table_in_use = table_name

        if self.get(key) == value:
            self.cursor.execute(f'DELETE FROM {self.table_in_use} WHERE key=? AND value=?', (key, value))
            self.connection.commit()
        else:
            raise KeyError(f"No item with key {key} and value {value} exists")

    def len(self, table_name=None):
        """Count length"""
        if not table_name:
            table_name = self.table_in_use
        self.cursor.execute(f'SELECT count() FROM {table_name};')
        return self.cursor.fetchone()[0]

    ### Magic Methods #################################

    def __setitem__(self, key, value):
        """Insert key value, will use default table 'dict' unless changed"""
        self.key_add(key, value)

    def __getitem__(self, key):
        """Returns the value from key, will use default table 'dict' unless changed"""
        return self.get(key)

    def __iter__(self):
        """Iterate all the keys, will use default table 'dict' unless changed """
        self.cursor.execute(f'SELECT * FROM {self.table_in_use}')
        for item in self.cursor.fetchall():
            if item[2]:  # JSON exists, return:
                yield (item[0], item[2])
            else:
                yield (item[0], item[1])

    def __contains__(self, item):
        """
        Check if the database contains the key. 
        It does not check the value.
        """
        try:
            key = self.get(item)
            if key:
                return key
        except KeyError:
            return False

    def __len__(self):
        """Get amounts of items with len()"""
        return self.len()

    def __delitem__(self, key):
        """Deletes key"""
        self.delete(key)

    ### Magic Methods End ###########################


    ### FTS 5 Search functions ###########################################
    """ 
    
        Search functions
        
        This section handles all Fast Text 5 functions of SQLite.
        FTS5 is a reverse index that allows you to index any kind of text and quickly search it. 
    
    
    
    """

    def search_add(self, key, value, table_name=None):
        """
        Add string or sentence that is to be indexed to a reverse search index, will return the keys that match.
        :return:
        """

        if table_name:
            self.search_table_in_use = table_name

        if not isinstance(value, bytes):  # Convert string to byte in order to CRCencode
            value = value.encode()

        self.cursor.execute(f'SELECT key FROM {self.search_table_in_use + "_unique"} WHERE key=?', (key,))
        key_sql_result = self.cursor.fetchone()  # If the key exists, a value is returned
        if not key_sql_result:  # If no value exists, add one
            if self.search_prevent_duplicate_values:
                crc32_result = crc32(value)
                self.cursor.execute(f'SELECT crc32 FROM {self.search_table_in_use + "_unique"} WHERE crc32=?',
                                    (crc32_result,))
                crc32_sql_result = self.cursor.fetchone()  # Reply if the CRC32 string already exists
                if not crc32_sql_result:
                    self.cursor.execute(f'INSERT INTO {self.search_table_in_use + "_unique"} VALUES(?, ?)',
                                        (key, crc32_result))
                    self.cursor.execute(f'INSERT INTO {self.search_table_in_use} VALUES(?, ?)', (key, value))
                    self.connection.commit()
                else:
                    raise ValueError("Value already exists")
            else:
                self.cursor.execute(f'INSERT INTO {self.search_table_in_use + "_unique"} VALUES(?, ?)', (key, None))
                self.connection.commit()
                self.cursor.execute(f'INSERT INTO {self.search_table_in_use} VALUES(?, ?)', (key, value))
                self.connection.commit()
        else:
            raise KeyError("Key already exists")

    def search_add_bulk(self, iterator: Iterable, table_name=None):
        """
        Search add bulk adds values in bulk, it's quicker than adding one at a time.
            It loads chunks of 10k items to RAM and then adds to database then merges write ahead log

        This function will check if values are unique, only add those.
            If duplicate value check is set to true then it will remove CRC32 based values
            it returns a list of tuples (key, value, crc32) that are deduped.

        It will then add all text values
        Then add the crc32 duplicates.

        """
        if table_name:
            self.search_table_in_use = table_name


        def de_duplicate_item(key, value) -> Tuple:
            """
            Removes duplicates from iterator and returns a list of (key, value, crc32)
            """
            duplicate_result_check = None
            duplicate_crc_result = None
            crc32_result = None

            if isinstance(value, str):  # Convert to bytes
                value = value.encode()
            self.cursor.execute(f'SELECT * FROM {self.search_table_in_use + "_unique"} where key=?', (key,))
            duplicate_result_check = self.cursor.fetchone()
            if not duplicate_result_check:
                "Key did not exist in the database, proceed to add"
                if self.search_prevent_duplicate_values:  # Only return unique values
                    crc32_result = crc32(value)
                    self.cursor.execute(f'SELECT crc32 FROM {self.search_table_in_use + "_unique"} where crc32=?',
                                        (crc32_result,))
                    duplicate_crc_result = self.cursor.fetchone()  # Get crc32 value if it exists
                    if not duplicate_crc_result:  # If it does not exist, return
                        return key, value, crc32_result
                    return None, None, None
                else:
                    return key, value, crc32_result
            else:
                return None, None, None

        def insert_data(tuple_list):
            self.cursor.executemany(f'INSERT INTO {self.search_table_in_use} VALUES(?, ?)',
                                    [(item[0], item[1]) for item in tuple_list])
            self.connection.commit()

            if self.search_prevent_duplicate_values:
                self.cursor.executemany(f'INSERT INTO {self.search_table_in_use + "_unique"} VALUES(?, ?)',
                                        [(item[0], item[2]) for item in tuple_list])
                self.connection.commit()

        ten_thousand_item_list = []
        for item in iterator:  # Loop through all values
            if len(item) != 2:
                raise ValueError("Bulk iterator must contain tuples of (key, values)")
            if not item[0] and not item[1]:
                raise ValueError("Tuple needs to contain key and value")
            key, value, crc32value = de_duplicate_item(item[0], item[1])  # Get de duplicated values
            if key:  # de_duplicate_item will return none for key if key already exists, then skip.
                ten_thousand_item_list.append((key, value, crc32value))
                if len(ten_thousand_item_list) == 100_000:
                    insert_data(ten_thousand_item_list)  # Insert items
                    ten_thousand_item_list = []  # Restore list
        insert_data(ten_thousand_item_list)  # Insert the last items

    def search(self, value, table_name=None, return_limit=30, order_by=True):
        """
        Returns the key for the strings or sentences that match
        """
        if table_name:
            self.search_table_in_use = table_name

        # No ordering
        search_string = f'SELECT key, value FROM {self.search_table_in_use} WHERE {self.search_table_in_use} MATCH ?'
        search_string = f'SELECT key, value FROM {self.search_table_in_use} WHERE {self.search_table_in_use} MATCH ? LIMIT={return_limit}'
        if order_by:
            search_string = f'SELECT key, value FROM {self.search_table_in_use} WHERE {self.search_table_in_use} MATCH ? ORDER BY rank LIMIT {return_limit}'
        else:
            search_string = f'SELECT key, value FROM {self.search_table_in_use} WHERE {self.search_table_in_use} MATCH ? LIMIT {return_limit}'

        self.cursor.execute(search_string,(value,))
        return self.cursor.fetchall()

    def search_key(self, key, table_name=None):
        """
        Returns the key and value for the string match
        Key is not indexed so this is slow, it is unadvisable to use this function.
        """
        if table_name:
            self.search_table_in_use = table_name

        self.cursor.execute(f'SELECT key, value FROM {self.search_table_in_use} WHERE key=?',
                            (key,))
        result = self.cursor.fetchone()
        if result:
            return result[1]

    def search_delete(self, key, table_name=None):
        """
        Deletes the key from the search index
        """
        if table_name:
            self.search_table_in_use = table_name

        if self.search_prevent_duplicate_values:
            " If CRC32 duplicate table exists, try and delete"
            self.cursor.execute(f'DELETE FROM {self.search_table_in_use + "_unique"} WHERE key=?', (key,))
            self.connection.commit()
        self.cursor.execute(f'DELETE FROM {self.search_table_in_use} WHERE key=?', (key,))
        self.connection.commit()

    def search_pop(self, key, table_name=None):
        """
        Return and delete key value
        """

        if table_name:
            self.search_table_in_use = table_name

        self.cursor.execute(f'SELECT key, value FROM {self.search_table_in_use} WHERE key=?', (key,))
        result = self.cursor.fetchone()
        if result:
            self.search_delete(key)
            return result[1]

    def search_iter_all_keys(self, table_name=None):
        """
        Returns an iterator with all the keys
        """
        if table_name:
            self.search_table_in_use = table_name
        self.cursor.execute(f'SELECT key, value FROM {self.search_table_in_use}')
        for item in self.cursor.fetchall():
            yield item[0]

    def search_validate_unique(self, table_name=None):
        """
        Re creates the crc32 unique table
        *Not implemented yet*
        """
        if table_name:
            self.search_table_in_use = table_name
        pass

    ####### Multi Functions ################################################################################################

    """

        Multi Functions
    
        This section contains all functions related to the "multi" part of SearchDB
        The Multi part acts more like a SQLite database instead of a python dictionary
        You can store a very large amount of columns, each with it's specific data type. 
    
    
    
    """


    def multi_add(self, items: Union[list, tuple, dict], table_name=None):
        """

        Add items, they can be in the format of:
        * Tuple: All values must match the table length and type
        * List: All values must match the table length and type
        * Dict: All keys and values must match, if value is empty, a Null will be inserted,

        If the multi table was created with other datatypes than TEXT, all items will get validated
        Duplicates are ignored.
        """
        if table_name:
            self.multi_table_in_use = table_name

        validated_items = self.__multi_validate_input(items)
        if validated_items:
            json_index = self.__multi_get_index_of_json()
            if json_index:
                #validated_items = list(validated_items)  # If they are a tuple the item can not be reassigned
                validated_items[json_index] = json.dumps(validated_items[json_index])
            self.cursor.execute(
                f"INSERT OR REPLACE INTO {self.multi_table_in_use} VALUES ({','.join(['?' for x in range(len(validated_items))])})",
                validated_items)
            self.connection.commit()
        else:
            raise ValueError("General insertion error")

    def multi_delete(self, delete_parameters: Union[tuple|list], return_deleted_count=False, table_name=None):
        """

        Delete items matching the inputs.
        The inputs are tuples of column name and keys.
        To remove all instances of "George" in the column name, use tuple: ("name": "George")

        To be more selective and only remove George's that are of the age 23, use:
            [("name": "George"), ("age": 23)]

        return_deleted_count returns an integer of all the items that were removed

        """
        if table_name:
            self.multi_table_in_use = table_name

        # First verify input data
        if isinstance(delete_parameters, tuple):
            " If input value was a single tuple, insert it into a list, can now use list code for tuple input."
            delete_parameters = [delete_parameters]  # tuple = list[tuple] :^)
        if isinstance(delete_parameters, list):
            for item in delete_parameters:
                if not isinstance(item, tuple):
                    raise ValueError("search parameter must be tuple")
                if len(item) != 2:
                    raise ValueError("search must be (key, value)")
                if item[0] not in self.table_info[self.multi_table_in_use]:
                    raise KeyError(f"does not exist, use .table_info to get tables")
        else:
            raise ValueError("multi_delete parameters must be tuple or list of tuples")

        column_string = ' AND '.join([f"{k[0]}=?" for k in delete_parameters])
        key_tuple = tuple([i[1] for i in delete_parameters])  # A tuple of all keys that will get removed

        delete_string = f"DELETE FROM {self.multi_table_in_use} WHERE {column_string} "
        self.cursor.execute(delete_string, key_tuple)
        deleted_count = self.cursor.rowcount
        self.connection.commit()
        if return_deleted_count:
            return deleted_count


    def multi_bulk_add(self, iterator: Iterable, table_name=None):
        """
        Bulk inserter of multiple values
        An iterable (list, generator) that yields tuples of values is required.

        First creates the insertion string and tests if insertion of first item works.
        Then insert 10k items at a time

        TODO: Add Dictionary insertion capability

        """
        if table_name:
            self.multi_table_in_use = table_name

        first_item = next(iterator)
        if self.__multi_validate_input(first_item):
            self.multi_add(first_item)
            self.connection.commit()

        insertion_string = f"INSERT OR REPLACE INTO {self.multi_table_in_use} VALUES ({','.join(['?' for x in range(len(first_item))])})"

        iterator = self.__multi_add_json_iterator_modifier(iterator)  # Modify iterator to handle JSON

        # Create 10k items and insert them
        ten_thousand_item_list = []
        for item in iterator:
            ten_thousand_item_list.append(item)
            if len(ten_thousand_item_list) == 10_000:
                self.cursor.executemany(insertion_string, ten_thousand_item_list)
                self.connection.commit()
                ten_thousand_item_list = []

        self.cursor.executemany(insertion_string, ten_thousand_item_list)
        self.connection.commit()

    def multi_search(self, search_parameters: Union[tuple|list], return_dict=False, table_name=None):
        """
        Search for an item based on one or many key values.

        Takes a tuple or list of tuples as input search parameters.
        The tuple must contain column and what to search for.
        All columns are validated before the search is being made.

        If you want to get a list directly, use list(searchdb.multi_search())
        """
        if table_name:
            self.multi_table_in_use = table_name
        # First verify input data
        if isinstance(search_parameters, tuple):
            " If input value was a single tuple, insert it into a list, can now use list code for tuple input."
            search_parameters = [search_parameters]  # tuple = list[tuple] :^)
        if isinstance(search_parameters, list):
            for item in search_parameters:
                if not isinstance(item, tuple):
                    raise ValueError("search parameter must be tuple")
                if len(item) != 2:
                    raise ValueError("search must be (key, value)")
                if item[0] not in self.table_info[self.multi_table_in_use]:
                    raise KeyError(f"does not exist, use .table_info to get tables")
        else:
            raise ValueError("multi search parameters must be tuple or list of tuples")


        column_list = self.__multi_get_columns()  # A list of all column names

        json_index = self.__multi_get_index_of_json()

        column_string = ' AND '.join([f"{k[0]}=?" for k in search_parameters])
        search_string = f"SELECT * FROM {self.multi_table_in_use} WHERE {column_string} "
        key_tuple = tuple([i[1] for i in search_parameters])


        self.cursor.execute(search_string, key_tuple)
        for item in self.cursor.fetchall():
            if json_index:
                item = list(item)
                item[json_index] = json.loads(item[json_index])
            if return_dict:
                item = dict(zip(column_list, item))
            yield item



    def multi_iter_all(self, table_name=None):
        " Returns an Sqlite iterator with all the values "
        if table_name:
            self.multi_table_in_use = table_name
        self.cursor.execute(f'SELECT * FROM {self.multi_table_in_use}')
        json_index = self.__multi_get_index_of_json()  # Check if JSON exists
        for item in self.cursor.fetchall():
            if json_index:
                item = list(item)
                item[json_index] = json.loads(item[json_index])
            yield item

    def multi_table_return_columns(self, table_name=None):
        """

        Prints the list of columns in the multi table/database

        """
        if table_name:
            self.multi_table_in_use = table_name
        return self.show_columns(table_name=self.multi_table_in_use)


    """
    
    Multi Helper functions
    
    """
    def __multi_get_index_of_json(self):
        " Return the index nr of the JSON item in the multi table"
        if 'json' in self.table_info[self.multi_table_in_use]:
            return list(self.table_info[self.multi_table_in_use].keys()).index("json")
        else:
            return None

    def __multi_get_json_iterator_modifier(self, iterator):
        """
        If a JSON item exists in the multi column then convert it to a python datatype
        """
        json_index = self.__multi_get_index_of_json()
        if json_index:
            for item in iterator:
                item = list(item)
                item[json_index] = json.loads(item[json_index])
                yield item
        else:
            for item in iterator:
                yield item

    def __multi_add_json_iterator_modifier(self, iterator):
        """

        If a JSON item exists in the multi column then convert it to a string

        """
        json_index = self.__multi_get_index_of_json()
        if json_index:
            for item in iterator:
                if self.__multi_validate_input(item):  # Validate item amount and datatypes
                    item = list(item)
                    item[json_index] = json.dumps(item[json_index])
                    yield item
        else:
            for item in iterator:
                if self.__multi_validate_input(item): # Validate item amount and datatypes
                    yield item
    def __multi_get_columns(self):
        """

        TODO: This is replaced by self.show_columns() # This is a function in the Init class
        Create an empty list with the size of the amount of columns in selected table
        For each column in table, insert the name in the index of the list.

        This is to make sure the column names are in correct order
            (Since Python 3.7 all dicts are ordered but it is better to be safe than sorry)

        """
        column_list = list([None]) * len(self.table_info[self.multi_table_in_use])
        for column in self.table_info[self.multi_table_in_use]:
            column_list[self.table_info[self.multi_table_in_use][column]["column_id"]] = column
        return column_list

    def __multi_get_columns_datatype(self):
        column_list = self.__multi_get_columns()
        datatype_list = [None]*len(column_list)
        for column in self.table_info[self.multi_table_in_use]:
            index = column_list.index(column)
            datatype = self.table_info[self.multi_table_in_use][column]["type"]
            datatype_list[index] = datatype
        return datatype_list

    def __multi_validate_input(self, items) -> list:
        """

        Validates the amount of items and datatype of items before trying to insert
            STRING/TEXT can contain anything
            INTEGER can only contain int
            REAL can contain float and int
            BLOB can only contain binary

        Returns the validated items ( This is because the
        """

        if not isinstance(items, tuple) and not isinstance(items, list) and not isinstance(items, dict):
            raise ValueError("tuple, list or dict is required")

        # Make sure the items are correct amount
        if len(items) != len(self.table_info[self.multi_table_in_use]):
            raise ValueError("Incorrect amount of items")

        """
        If input is dict, validate it and convert to a list
        """
        if isinstance(items, dict):
            columns = self.multi_table_return_columns()
            item_list = [None] * len(columns)
            for key in items:
                if key not in columns:
                    raise ValueError(f"key does not exist")
                item_list[columns.index(key)] = items[key] # Insert key in the correct name
            # Make sure there are no None values, they will break "UNIQUE" function in SQLite and allow duplicates.
            if None in item_list:
                raise ValueError(f"Missing {columns[item_list.index(None)]}") # This error should never happen
            items = item_list



        # Generate a list of SQLite datatypes
        datatype_list = self.__multi_get_columns_datatype()
        for i in range(len(items)):
            if items[i] is None:
                continue  # empty value None gets converted to Null in SQLite
            if datatype_list[i] == "TEXT" or datatype_list[i] == "STRING":
                continue  # Quick return since most items are TEXT
            elif datatype_list[i] == "INTEGER" and not isinstance(items[i], int):
                raise ValueError(f"Item {items[i]} is not int")
            elif datatype_list[i] == "REAL":
                if isinstance(items[i], float):
                    continue
                elif isinstance(items[i], int):
                    continue
                else:
                    raise ValueError(f"Item {items[i]} is neither float nor int")
            elif datatype_list[i] == "BLOB" and type(items[i]) != bytes:
                raise ValueError("Item is not bytes")

        return list(items)



    ### Utils ##############################################

    def __validate_db_and_key_int(self, key):
        """
        Checks if the table was created as INTEGER
        if so verify that the key is an integer
        """
        if self.table_info[self.table_in_use]["key"]["type"] == "INTEGER":
            " If the key was created as integer only, validate that key is an integer"
            if isinstance(key, int):
                pass
            elif isinstance(key, str) and key.isnumeric():
                pass
            else:
                raise KeyError(f"Table was created as integer only, {key} is not an integer")

    def __key_val_to_key_val_json(self, key, value) -> Tuple:
        " Converts the value to JSON if it is possible to do so"
        json_data = None
        if isinstance(value, str):
            return (key, value, json_data)
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, dict):
            json_data = json.dumps(value)
            value = None
        elif isinstance(value, list):
            json_data = json.dumps(value)
            value = None
        elif isinstance(value, tuple):
            json_data = json.dumps(value)
            value = None
        elif isinstance(value, set):
            json_data = json.dumps(list(value))
            value = None
        elif isinstance(value, bool):
            json_data = json.dumps(value)
            value = None
        return (key, value, json_data)

    def purge_table(self, table_name: str, confirm=False):
        "Remove all contents in table, if you want to remove the table use drop_table()" # Remove since drop table exists?
        if table_name in self.tables:
            if confirm:
                self.cursor.execute("PRAGMA writable_schema = 1")
                self.connection.commit()

                # Purge data
                self.cursor.execute(f"DELETE FROM {table_name}")
                self.connection.commit()

                # Purge key value unique table if it exists
                try:  # Ugly but ok it works
                    self.cursor.execute(f"DELETE FROM {table_name + '_unique'}")
                    self.connection.commit()
                except:
                    pass
                self.cursor.execute("PRAGMA writable_schema = 0")
                self.connection.commit()
                self.cursor.execute("VACUUM")
                self.connection.commit()
                self.cursor.execute("PRAGMA integrity_check")
                self.connection.commit()
                self.table_info_update()
            else:
                raise ValueError("Set confirm=True to wipe database")
        else:
            raise ValueError(f"{table_name} does not exist")

    def __missing__(self, key):
        pass
