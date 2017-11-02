import os, sys
from tkinter.filedialog import *
from tkinter import *
import sqlite3

if __name__ == "__main__":
    print("LiteManager")
    print("Type 'help' for a list of commands")

    root = Tk()
    root.withdraw()

    dbpath = askopenfilename()

    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    while True:
        command = input(" >>> ")
        if command == "raw":
            command = input("    >>> ")
            try:
                c.execute("{}".format(command))
                conn.commit()
                data = c.fetchall()
                if data == []:
                    pass
                else:
                    for item in data:
                        print("---------------")
                        for subitem in item:
                            print(subitem)
                    print("---------------")
            except sqlite3.OperationalError as e:
                print("Operational Error")
                print(e)
        elif command == "view":
            try:
                tablename = input("    >>> ")
                c.execute("SELECT * FROM {}".format(tablename))
                data = c.fetchall()
                if data == []:
                    print("No table data")
                else:
                    for item in data:
                            print("---------------")
                            for subitem in item:
                                print(subitem)
                    print("---------------")
            except sqlite3.OperationalError as e:
                print("Operational Error")
                print(e)
        elif command == "tables":
            c.execute("SELECT * FROM sqlite_master WHERE type='table'")
            data = c.fetchall()
            for item in data:
                c.execute("PRAGMA table_info({})".format(item[1]))
                data = c.fetchall()
                print("\n---------------")
                print("Name: " + item[1])
                print("====Columns====")
                for column in data:
                    print("Column name: " + column[1] + " | Data Type: " + column[2])
                print("---------------")
        elif command == "input":
            try:
                tablename = input("    >>> ")
                c.execute("PRAGMA table_info({})".format(tablename))
                data = c.fetchall()
                columns = []
                values = []
                i=0
                for item in data:
                    columns.append(data[i][1])
                    column_input = input("        >>> ")
                    values.append(column_input)
                    i += 1
                c.execute("INSERT INTO " + tablename + " ('" + "', '".join(columns) + "') values ({})".format("'" + ("', '".join(values)) + "'"))
                conn.commit()
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
            pass
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
            choice = input("Warning. This will permanently remove all entries from the database. Continue? y/n >>> ")
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
        try:
            global conn
            conn = sqlite3.connect(dbpath)
            global c
            c = conn.cursor()
        except sqlite3.OperationalError as e:
            print("Operational Error")
            print(e) 
    def input(tablename, input_data):
        try:
            if type(input_data) != list:
                print("Incorrect arg type")
            else:
                c.execute("PRAGMA table_info({})".format(tablename))
                data = c.fetchall()
                columns = []
                i=0
                for item in data:
                    columns.append(data[i][1])
                    i += 1
                c.execute("INSERT INTO " + tablename + " ('" + "', '".join(columns) + "') values ({})".format("'" + ("', '".join(input_data)) + "'"))
                conn.commit()
        except sqlite3.OperationalError as e:
            print("Operational Error")
            print(e) 
    def delete(tablename, column, spec):
        try:
            c.execute("DELETE FROM " + tablename + " WHERE " + column + "=?",[spec])
            conn.commit()
        except sqlite3.OperationalError as e:
            print("Operational Error")
            print(e)        
    def create(placeholder):
        pass
    def drop(tablename):
        try:
            c.execute("DROP TABLE {}".format(tablename))
            conn.commit()    
        except sqlite3.OperationalError as e:
            print("Operational Error")
            print(e) 

