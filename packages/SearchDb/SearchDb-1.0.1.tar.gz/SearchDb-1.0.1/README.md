# SearchDB #

*A SQLite powered dictionary*

**Features**
* **Indexed keys and values**
  * Can store dicts, lists, tuples as values (they are not indexed in that case)
* **Multi column indexes** 
  * Use SearchDB as a regular database, store several columns instead of just key-value
  * If column is called "JSON" then datatypes can get stored there (they get converted to JSON)
* **Fast Text Search**
  * Use Search functions to query large amounts of text.
  * Uses FastTextSearch5 functions in SQLite
* **Persists to file**
  * Makes sharing dicts easy
  * .merge function merges two different databases with the same structure.


## Usage ##
### Basic usage ###
```
In [1]: import SearchDb
In [2]: db = SearchDb.SearchDb(":memory:")   # Create an in memory database
In [3]: db["a"] = "alfa"
In [4]: db["a"]
Out[4]: 'alfa'
In [5]: del(db["a"])
In [6]: db["b"] = "beta"
In [7]: db.delete("b")
```


### Store and search text data ###
* Use search_add("unindexed_key", "lots of text") to add large datasets
* Examples:
  * Index a book, page is key, value is all text in page

### Use custom indexes ###
To set a custom name for your regular key,value index use:  
``.table_in_use("newname")``  
To set a custom name for your text search index (one per book for example) use:  
``.search_table_in_use("python_for_noobs")``  

### Create new table ###
To create a new table (database)  use the .create_tables() function.  
First set the name of the new table or tables you wish to create, for instance:
```
.table_in_use = "new_key_value"  
.multi_table_in_use = "new_multi_column"

.create_tables() # Will now create all the new tables 


.search_table_in_use = "new_indexed_texts" 
.sdb.create_search_index()
```
