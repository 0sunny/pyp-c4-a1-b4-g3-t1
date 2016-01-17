"""The file to test the package pyp_database."""

import logic as l
import pyp_database as pdb


print pdb.show_databases()

#db = pdb.use('testdb.db')

#print pdb.show_tables()
tb = l.Table('test', ('a','b','c'))

#db = l.Database('testdb')
#db.create_table('new', ('a','b','c'))

#db.new.insert((1,2,3))

#print db.new.query(a = 10)

#db.create_table('new', ('a'))

for row in tb:
    print row

#tb.insert((10,20,30))


#tb.insert((100,200,300))

#tb.insert_rows(((2,3,4),(5,6,7),(8,9,10)))

print tb.query(a = 10)

print tb.query(a = 10, b = 20, d = 4)

print tb.query(a = 100, b = 200)

for row in tb:
    print row