# Rob Frye, 2017
# Update records or insert them if they don't exist.
# Note that this is a workaround to compensate for missing
# SQL features in SQLite.

import sqlite3

sqlite_file = 'twitter_r_data.sqlite'
# table_name1 = 'AUTHORS'	# name of the table to be created
# id_column = 'AUTHOR_ID'
# column_name = 'AUTHOR_NM'
table_name2 = 'TWEETS'	# name of the table to be created
id_column = 'AUTHOR_ID'
twt_col = 'TWEET_MSG'
pos_col = 'POS_MSG'
auth_id = '11234jasdf'
twt_msg = 'tweeting is fun'
pos_msg = '#POS V N C'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()


# # A) Inserts an ID with a specific value in a second column
# try:
#     c.execute("INSERT INTO {tn} ({idf}, {cn}) VALUES (123456, 'test')".\
#         format(tn=table_name, idf=id_column, cn=column_name))
# except sqlite3.IntegrityError:
#     print('ERROR: ID already exists in PRIMARY KEY column {}'.format(id_column))

# B) Tries to insert an ID (if it does not exist yet)
# with a specific value in a second column
# TESTING INSERTING AUTHOR
# c.execute("INSERT OR IGNORE INTO {tn} ({idf}, {cn}) VALUES ('11234jasdf', 'author_1')".\
#         format(tn=table_name1, idf=id_column, cn=column_name))

# TESTING INSERTING MESSAGE
sql_start = 'INSERT OR IGNORE INTO '
sql_end = ' VALUES (?,?,?)'
query = sql_start + table_name2 + sql_end
c.execute(query,(auth_id, twt_msg, pos_msg))

# # C) Updates the newly inserted or pre-existing entry
# c.execute("UPDATE {tn} SET {cn}=('Hi World') WHERE {idf}=(123456)".\
#         format(tn=table_name, cn=column_name, idf=id_column))

conn.commit()
conn.close()