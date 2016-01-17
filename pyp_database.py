"""The top level module."""

import os
import logic as l
import exceptions as e

def show_databases():
    """Show the databases present in the current workspace."""
    items = os.listdir(workspace)
    dbs = []
    for names in items:
        if names.endswith(".db"):
            dbs.append(names[:-3])
    #print [str(db) for db in dbs]
    return dbs

def show_tables():
    """Show the tables present in the current database."""
    return "\n".join([str(tab) for tab in default_db.table_names])
    
def create_database(name):
    """Create a database with the given name."""
    if name in db_names:
        print "Database with {} name exists already.".format(name)
        return None
    else:
        db = l.Database(name)
        db_names.append(name)
        return db

def delete_database(name):
    """Delete the database with the given name, else mesage printed/error raised."""
    
def use(name):
    """Use the database with the given name."""
    if name not in db_names:
        print "Database not found, would you like to create?"
        return None
    else:
        db = l.Database(name)
        default_db = db
        return default_db

#Setting default values
workspace = os.getcwd()
default_db = None
db_names = show_databases()
