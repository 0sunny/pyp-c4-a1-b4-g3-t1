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
        self.column_types = column_types
        self.column_none_allowed = column_none_allowed
        self.duplicates_allowed = duplicates_allowed
        self.indexed = indexed
        self.path = self.name + ".table"
        self.file = None
        self._write_metadata()
    
    def _write_metadata(self):
        """Write the table metadata into the file."""
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
        row = tuple(str(i) for i in row)
        if self.file and not self.file.closed:
            self.file.close()
        with open(self.path, 'a') as self.file:
            self.file.write("\n")
            self.file.write(",".join(row))

    def insert_rows(self, rows):
        """Insert the rows into the table."""
        #Can modify later to chunk the rows for insertion
        val = "\n".join([",".join([str(i) for i in row]) for row in rows])
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
        Can change it to find the rows with given index."""
        #index_ stores the index as key and the value to be matched as value
        index_ = {}
        for key, value in kwargs.iteritems():
            try:
                index_[self.columns.index(key)] = str(value)
            except ValueError:
                raise e.ColumnNotFoundError()
        print(index_)
                
        if index_ is not None:
            #row = ",".join((str(i) for i in row))
            for i, curr_row in enumerate(self):
                curr = curr_row.strip().split(",")
                print(curr_row.strip().split(","))
                if all(curr[k] == v for k,v in index_.iteritems()):
                    print("Found")
                    return ",".join(curr)
        return None
    
    def delete(self, row = None, **kwargs):
        """Delete the given row or delete the rows with the information from the
        kwargs."""
        