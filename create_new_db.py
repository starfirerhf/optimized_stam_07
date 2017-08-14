# Creating a new SQLite database for Rocha Twitter Data
import sqlite3

sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file
table_name1 = 'AUTHORS'	# name of the table to be created
table_name2 = 'TWEETS'	# name of the table to be created
new_field = 'AUTHOR_ID' # name of the column
field_type = 'TEXT'  # column data type

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn=table_name1, nf=new_field, ft=field_type))

# Creating a second table with 1 column and set it as PRIMARY KEY
# note that PRIMARY KEY column must consist of unique values!
c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name2, nf=new_field, ft=field_type))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()