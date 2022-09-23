"""Creating tables: https://docs.python.org/3/library/sqlite3.html"""

import sqlite3, csv
con = sqlite3.connect("ramen.db")
cursor = con.cursor()

# Clears old table if one exists: https://www.tutorialspoint.com/python_data_access/python_sqlite_drop_table.htm
res = cursor.execute("SELECT name FROM sqlite_master")
if res.fetchall() is not []:
    cursor.execute("DROP TABLE ramen_ratings")
    con.commit()

# Creates a table called ramen_ratings
cursor.execute("CREATE TABLE ramen_ratings(number, brand, variety, style, country, stars)")

# Imports csv file to table:
# https://www.geeksforgeeks.org/how-to-import-a-csv-file-into-a-sqlite-database-table-using-python/
file = open("ramen-ratings.csv")
contents = csv.reader(file)
cursor.executemany("""INSERT INTO ramen_ratings (number, brand, variety, style, country, stars) 
                    VALUES(?, ?, ?, ?, ?, ?)""", contents)
con.commit()
con.close()
