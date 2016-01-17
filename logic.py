"""File with the required class definitions."""

from __future__ import print_function, division
import os
import exceptions as e

class Table(object):
    """The class structure for the table, this has methods to update entries, 
    delete entries, insert entries, display the table."""
    
    def __init__(self, name, columns = None, column_types = None, 
    column_none_allowed = None, duplicates_allowed = True, 
    indexed = False):
        """Initialize the table with the columns and name.
        The columns is a tuple with the column names,
        the column types is a tuple with types of data allowed for that coloumn, 
        having None/empty as type means any type allowed and
        columns_none_allowed or not is a tuple of booleans."""
        self.name = name
        self.columns = columns
        self._is_column_name_valid()
        self.column_types = column_types
        self.column_none_allowed = column_none_allowed
        self.duplicates_allowed = duplicates_allowed
        self.indexed = indexed
        self.path = self.name + ".table"
        self.num_rows = 0
        self.num_valid_rows = 0
        if not os.path.exists(self.path):
            #Create the file if it doesn't exist.
            self._write_metadata()
            with open(self.path, 'w') as f:
                pass
        else:
            self.load()
        self.file = None
    
    def _write_metadata(self):
        """Write the table metadata into the file."""
        #This part would be to make the database persistent
        """
        #Metadata format:
        Name
        Database Name
        columns
        column types
        columns_none_allowed
        indexed - boolean
        duplicates_allowed - boolean
        number of rows of data
        number of valid rows of data
        """
        with open(self.path + ".metadata", 'w') as f:
            f.write(self.name + "\n")
            f.write("\n")
            f.write(",".join(self.columns) + "\n")
            if self.column_types is not None:
                f.write(",".join(self.column_types) + "\n")
            else:
                f.write(str(None) + "\n")
            if self.column_none_allowed is not None:
                f.write(",".join(self.columns_none_allowed) + "\n")
            else:
                f.write(str(None) + "\n")
            f.write(str(self.indexed) + "\n")
            f.write(str(self.duplicates_allowed) + "\n")
            f.write(str(self.num_rows) + "\n")
            f.write(str(self.num_valid_rows) + "\n")

    def load(self):
        """Load the table from the file, useful to make this persistent."""
        #load the metadata and update the attribute variables.
        with open(self.path + ".metadata", 'r') as f:
            self.name = f.readline()[:-1]
            f.readline()
            self.columns = tuple(f.readline()[:-1].split(","))
            self.column_types = tuple(f.readline()[:-1].split(","))
            self.column_none_allowed = tuple(f.readline()[:-1].split(","))
            if f.readline()[:-1] == 'True':
                self.indexed = True
            else:
                self.indexed = False
            if f.readline()[:-1] == 'True':
                self.duplicates_allowed = True
            else:
                self.duplicates_allowed = False
            self.num_rows = int(f.readline()[:-1])
            self.num_valid_rows = int(f.readline()[:-1])
                
    
    def _is_column_name_valid(self):
        """Make sure that the column do not end with __, as is it used for better
        queries."""
        if any(col[-2:] == '__' for col in self.columns):
            raise NameError('Columns cannot have double underscore towards end.')
        
    def _is_valid_data(self, row = None, **kwargs):
        """Checks if the row or kwargs have valid data types."""
        #Incomplete
        if row is not None:
            if len(row) == len(self.columns):
                pass
    
    def __iter__(self, mode = 'r'):
        self.file = open(self.path, mode)
        return self.file
    
    def __next__(self):
        try:
            res = next(self)
            res = ",".join(res.strip().split(",")[2:])
        except StopIteration:
            self.file.close()
            raise StopIteration
        return res
    
    def __str__(self):
        """Return the table in a pretty format."""
        res = ""
        for row in self:
            res += row
        return res
    
    def insert(self, row):
        """Insert the row which is a tuple of strings into the table."""
        if self.file and not self.file.closed:
            self.file.close()
        with open(self.path, 'a') as self.file:
            row = (str(self.num_rows + 1), '1') + tuple(str(i) for i in row)
            self.file.write(",".join(row))
            self.file.write("\n")
            self.num_rows += 1
            self.num_valid_rows += 1

    def insert_rows(self, rows):
        """Insert the rows into the table."""
        #Can modify later to chunk the rows for insertion
        val = "\n".join([",".join([str(self.num_rows + i + 1), '1'] + 
        [str(it) for it in row]) for i,row in enumerate(rows)])
        if self.file and not self.file.closed:
            self.file.close()
        with open(self.path, 'a') as self.file:
            self.file.write("\n")
            self.file.write(val)

    def update(self, row, **kwargs):
        """Update the rows based on the information in the kwargs.
        The rows get updated with the row."""
    
    def query(self, **kwargs):
        """Find the row with the given information as in the kwargs.
        Can change it to find the rows with given index. 
        Returns a list of tuples, each tuple being the line number and data"""
        #index_ stores the index as key and the value to be matched as value
        index_ = {}
        for key, value in kwargs.iteritems():
            try:
                index_[self.columns.index(key)] = str(value)
            except ValueError:
                #raise e.ColumnNotFoundError()
                print("Column {} not found".format(key))
                pass
        #print(index_)
        
        res = []    
        if index_ is not None:
            #row = ",".join((str(i) for i in row))
            for i, curr_row in enumerate(self):
                temp = curr_row.strip().split(",")
                valid = temp[1]
                curr = temp[2:]
                #print(curr, "Current row")
                if valid != '0' and all(curr[k] == v for k,v in index_.iteritems()):
                    print("Found")
                    res.append(",".join(curr))
        if res == []:
            return None
        else:
            return res
    
    def delete(self, row = None, **kwargs):
        """Delete the given row or delete the rows with the information from the
        kwargs."""
        


class Database(object):
    """Class Structure for the database."""
    
    def __init__(self, name):
        self.name = name
        self.path = self.name + ".db"
        self.table_names = []
        if not os.path.exists(self.path):
            #Create the file if it doesn't exist.
            #self._write_metadata()
            with open(self.path, 'w') as f:
                pass  
    
    def create_table(self, table_name, columns = None, column_types = None, 
    column_none_allowed = None, duplicates_allowed = True, 
    indexed = False):
        """Creates the table and returns the table object. If table already 
        exists, then prints the information and returns None."""
        if table_name in self.table_names:#hasattr(self, table_name):
            #raise TableAlreadyExistsError()
            print("Table already exists, please choose a different name.")
            return None
        tb = Table(table_name, columns, column_types, column_none_allowed, 
        duplicates_allowed, indexed)
        setattr(self, table_name, tb)
        self.table_names.append(table_name)
        return getattr(self, table_name)
    
    def delete_table(self, table_name):
        """Deletes the file if exists or prints a message."""
        if hasattr(self, table_name):
            #Delete the table
            #print("Deleted the table succesfully.")
            os.remove(getattr(self, table_name).path)
            self.table_names.remvove(table_name)
            delattr(self, table_name)
            return True
            pass
        else:
            print("The table doesn't exist.")
            return False
    
    def _write_metadata(self):
        """Write the table metadata into the file."""
        #This part would be to make the database persistent
        """
        #Metadata format:
        Name
        """
        with open(self.path + ".metadata", 'w') as f:
            f.write(self.name + "\n")
    
    def load(self):
        """Load the database from the file. Useful for persistence."""
        #Nothing to update