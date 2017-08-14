# Adding a new column to an existing SQLite database

import sqlite3

sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file
table_name = 'AUTHORS'	# name of the table to be created
table_name1 = 'TWEETS'	# name of the table to be created
id_column = 'AUTHOR_ID' # name of the PRIMARY KEY column
nm_column = 'AUTHOR_NM' # name of the PRIMARY KEY column
numb_column = 'TWEET_COUNT' # number of tweets for this author
new_column1 = 'MESSAGE_NUM'  # name of the new column
new_column2 = 'TWEET_MSG'  # name of the new column
new_column3 = 'POS_MSG'  # name of the new column
column_type = 'TEXT' # E.g., INTEGER, TEXT, NULL, REAL, BLOB
int_column_type = 'INTEGER'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# A) Adding a new column without a row value
c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=numb_column, ct=int_column_type))
# c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
#         .format(tn=table_name1, cn=new_column1, ct=column_type))
# c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
#         .format(tn=table_name1, cn=new_column2, ct=column_type))
# c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
#         .format(tn=table_name1, cn=new_column3, ct=column_type))

# B) Adding a new column with a default row value
# c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
#         .format(tn=table_name, cn=new_column2, ct=column_type, df=default_val))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()