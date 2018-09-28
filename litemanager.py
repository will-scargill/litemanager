import os, sys
from tkinter.filedialog import *
from tkinter import *
import sqlite3

sqlvartypes_to_pythonvartypes = {
    "TEXT" : str,
    "INTEGER" : int,
    "REAL" : float,
    "BOOL" : bool
    }

if __name__ == "__main__":
    print("LiteManager")
    print("Type 'help' for a list of commands")

    root = Tk() # Initialise Tkinter frame
    root.withdraw() # Hide frame

    dbpath = askopenfilename() # Open database

    conn = sqlite3.connect(dbpath) # Set up DB connection
    c = conn.cursor() # Set up cursor

    while True:
        command = input(" >>> ")
        if command == "raw": # Input raw SQL
            command = input("    >>> ")
            try:
                c.execute("{}".format(command)) # Execute command
                conn.commit() # Commit command
                data = c.fetchall() # Fetch recieved data (if any)
                if data == []: # Is there any data?
                    pass # If not, move on
                else: # If there is
                    for item in data:
                        print("---------------")
                        for subitem in item:
                            print(subitem) # Print data
                    print("---------------")
            except sqlite3.OperationalError as e: # If SQL Syntax incorrect
                print("Operational Error")
                print(e) # Print error
        elif command == "view": # View all entries in a table
            try:
                tablename = input("    >>> ")
                c.execute("SELECT * FROM {}".format(tablename)) # Select all entries from selected table
                data = c.fetchall()
                if data == []: # Is there any data?
                    print("No table data")
                else: # If there is
                    for item in data:
                            print("---------------")
                            for subitem in item:
                                print(subitem) # Print data
                    print("---------------")
            except sqlite3.OperationalError as e: # If SQL Syntax incorrect
                print("Operational Error")
                print(e) # Print error
        elif command == "tables": # View all tables
            c.execute("SELECT * FROM sqlite_master WHERE type='table'") # Select all tables
            data = c.fetchall()
            if data == []: # Is there any data?
                print("No tables")
            else: # If there is
                for item in data:
                    c.execute("PRAGMA table_info({})".format(item[1]))
                    data = c.fetchall()
                    print("\n---------------")
                    print("Name: " + item[1])
                    print("====Columns====")
                    for column in data:
                        print("Column name: " + column[1] + " | Data Type: " + column[2])
                    print("---------------")
        elif command == "input": # Add an entry to a table
            try:
                tablename = input("    >>> ")
                c.execute("PRAGMA table_info({})".format(tablename)) # Get all table information
                data = c.fetchall()
                columns = []
                commandColumns = []
                values = []
                i=0
                for item in data:
                    columns.append(data[i]) # Add column data to columns                    
                    print("        "+str(columns[i][1] + " - " + columns[i][2])) # Print column name and data type
                    check = False
                    while check == False: # While inputted data is incorrect type
                        column_input = input("        >>> ")
                        try:
                            column_input = sqlvartypes_to_pythonvartypes[columns[i][2]](column_input) # Get equivalent data type
                            check = True # Set check to true
                        except: # Data type incorrect
                            print("        Error - Wrong data type")
                    values.append(str(column_input)) # Add inputted value to values as a string (To stop .join freaking out)
                    i += 1 # Add one to i
                i=0 # Reset i
                for col in columns:
                    commandColumns.append(columns[i][1]) # Add column name to commandColumns
                    i += 1
                c.execute("INSERT INTO " + tablename + " ('" + "', '".join(commandColumns) + "') values ({})".format("'" + ("', '".join(values)) + "'"))
                # "', '".join(commandColumns) --- Joins the columns names
                # ("', '".join(values)) --- Joins the values
                conn.commit() # Commit entry
                print("Input successful")
            except sqlite3.OperationalError as e:
                print("Operational Error")
                print(e)
        elif command == "delete":
            try:
                tablename = input("    >>> ")
                c.execute("SELECT * FROM {}".format(tablename))
                data = c.fetchall()
                entries = {}
                print("Please enter index of entry to delete/q to cancel")
                print("---------------")
                for i in range(len(data)):
                    entries[str(i)] = data[i]
                    print(str(i) + ": " + str(data[i]))
                    print("---------------")
                index = input("        >>> ")
                if index == "q":
                    pass
                else:
                    try:
                        entry = entries[index]
                        c.execute("DELETE FROM " + tablename + " WHERE rowid=?", [index])
                        conn.commit()
                        print("Deletion successful")
                    except KeyError:
                        print("Invalid Index")
            except sqlite3.OperationalError as e:
                print("Operational Error")
                print(e)
        elif command == "create":
            try:
                print("    Input Table Name")
                tablename = input("    >>> ")
                if tablename == "":
                    print("    Please enter a table name")
                else:
                    columns = []
                    check = False
                    print("""===Possible Data Types===
INTEGER - Whole Number
TEXT - String
REAL - Floating Point
BOOL - Boolean
=========================""")
                    while check == False:
                        col = []
                        print("    Input Column Name/q to finish")
                        col_name = input("    >>> ")
                        if col_name == "":
                            print("    Please enter a column name")
                        else:
                            if col_name == "q":
                                if len(columns) == 0:
                                    print("    Table must have at least 1 column")
                                else:
                                    col_names = []
                                    col_types = []
                                    for col in columns:
                                        col_names.append(col[0])
                                        col_types.append(col[1])
                                    formatted_text = ""
                                    for i in range(len(columns)):
                                        formatted_text += col_names[i]
                                        formatted_text += " "
                                        formatted_text += col_types[i]
                                        formatted_text += ", "
                                    formatted_text = formatted_text[:(len(formatted_text)-2)]
                                    c.execute("CREATE TABLE " + tablename + " (" + formatted_text + ")")
                                    conn.commit()
                                    check = True
                                    print("    Table created")
                            else:
                                print("    Input a column data type")
                                col_type = input("    >>> ")
                                if col_type == "":
                                    print("    Please enter a column data type")
                                else:
                                    if col_type == "INTEGER" or col_type == "TEXT" or col_type == "REAL":
                                        col.append(col_name)
                                        col.append(col_type)
                                        columns.append(col)
                                    else:
                                        print("    Invalid data type")
                        
                    
            except sqlite3.OperationalError as e:
                print("Operational Error")
                print(e)  
        elif command == "drop":
            try:
                c.execute("SELECT * FROM sqlite_master WHERE type='table'")
                data = c.fetchall()
                tables = {}
                print("Please enter index of table to delete/q to cancel")
                for i in range(len(data)):
                    tables[str(i)] = data[i]
                    print(str(i) + ": " + str(data[i][1]))
                index = input("        >>> ")
                if index == "q":
                    pass
                else:
                    try:
                        table = tables[index]
                        c.execute("DROP TABLE {}".format(table[1]))
                        conn.commit()
                    except KeyError:
                        print("Invalid Index")
            except sqlite3.OperationalError as e:
                print("Operational Error")
                print(e)           
        elif command == "wipe":
            choice = input("Warning! This will permanently remove all entries from the database. Continue? y/n >>> ")
            if choice == "y":
                print("Proceeding")
                c.execute("SELECT * FROM sqlite_master WHERE type='table'")
                data = c.fetchall()
                tables = []
                for item in data:
                    tables.append(item[1])
                for table in tables:
                    c.execute("SELECT * FROM {}".format(table))
                    entries = c.fetchall()
                    for i in range(len(entries)+1):
                        c.execute("DELETE FROM " + table + " WHERE rowid=?", [i])
                        conn.commit()
                conn.commit()
                print("Database wipe complete")
            elif choice == "n":
                pass            
        elif command =="help":
            print("""----=help=----
raw - input sql
view - view all entries for a table
tables - view all tables and their columns
input - input an entry to a table
delete - delete an entry from a table
create - create a table
drop - delete a table
wipe - wipes the database of all entries
help - view all commands""")
else:
    def connect(dbpath):
            global conn
            conn = sqlite3.connect(dbpath)
            global c
            c = conn.cursor()
    def raw(raw):
        c.execute(raw)
        data = c.fetchall()
        if data == []:
            pass
        else:
            return(data)
        conn.commit()
    def input(tablename, input_data):
            c.execute("PRAGMA table_info({})".format(tablename))
            data = c.fetchall()
            columns = []
            i=0
            for item in data:
                columns.append(data[i][1])
                i += 1
            c.execute("INSERT INTO " + tablename + " ('" + "', '".join(columns) + "') values ({})".format("'" + ("', '".join(input_data)) + "'"))
            conn.commit()
    def delete(tablename, column, conditional):
            c.execute("DELETE FROM " + tablename + " WHERE " + column + "=?",[conditional])
            conn.commit()      
    def create(tablename, columns):
        col_names = []
        col_types = []
        for col in columns:
            col_names.append(col[0])
            col_types.append(col[1])
        formatted_text = ""
        for i in range(len(columns)):
            formatted_text += col_names[i]
            formatted_text += " "
            formatted_text += col_types[i]
            formatted_text += ", "
        formatted_text = formatted_text[:(len(formatted_text)-2)]
        c.execute("CREATE TABLE " + tablename + " (" + formatted_text + ")")
        conn.commit()
    def drop(tablename):
            c.execute("DROP TABLE {}".format(tablename))
            conn.commit()     
