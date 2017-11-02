# litemanager
A python program that doubles up as module which is designed to simplify the use of SQLite
# Program Instructions
Coming soon..

# Module Instructions
## Setup

```python
import litemanager
litemanager.connect(databasepath)
```

## Methods

### `connect(dbpath[String])` 

Sets up the database connection. This must be run before any other functions are run

```python
litemanager.connect("database.db")
```

### `input(tablename[String], input_data[List of strings])` 

Inputs an entry to a table. The input_data list must contain an amount of items identical to the amount of columns in the table. To leave an entry blank enter "".

```python
litemanager.input("foobar", ["Foo", "Bar"])
```

### `delete(tablename[String], column[String], conditional[String])` 

Deletes an entry from a table. 'conditional' refers to the term used to identify the entry to be deleted.

```python
litemanager.delete("foobar", "column1", "Foo")
```

### `drop(tablename[String])` 

Deletes a table

```python
litemanager.drop("foobar")
```
