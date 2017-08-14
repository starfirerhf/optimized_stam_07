import sqlite3

sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file
table_name = 'AUTHORS'   # name of the table to be queried
table_name2 = 'TWEETS'   # name of the table to be queried
id_column = 'AUTHOR_ID'
some_id = 123456
column_2 = 'MESSAGE_NUM'
column_3 = 'TWEET_MSG'
column_4 = 'POS_MSG'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# 1) Contents of all columns for row that match a certain value in 1 column
c.execute('SELECT * FROM {tn} WHERE {cn}="0cd5ca028593ffbf99e5b591513f1b0b9b538f2c"'.\
    format(tn=table_name2, cn=id_column))
all_rows = c.fetchall()
for row in all_rows:
    print(row)
#
# # 2) Value of a particular column for rows that match a certain value in column_1
# c.execute('SELECT ({coi}) FROM {tn} WHERE {cn}="Hi World"'.\
#         format(coi=column_2, tn=table_name, cn=column_2))
# all_rows = c.fetchall()
# print('2):', all_rows)
#
# # 3) Value of 2 particular columns for rows that match a certain value in 1 column
# c.execute('SELECT {coi1},{coi2} FROM {tn} WHERE {coi1}="Hi World"'.\
#         format(coi1=column_2, coi2=column_3, tn=table_name, cn=column_2))
# all_rows = c.fetchall()
# print('3):', all_rows)
#
# # 4) Selecting only up to 10 rows that match a certain value in 1 column
# c.execute('SELECT * FROM {tn} WHERE {cn}="Hi World" LIMIT 10'.\
#         format(tn=table_name, cn=column_2))
# ten_rows = c.fetchall()
# print('4):', ten_rows)
#
# # 5) Check if a certain ID exists and print its column contents
# c.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".\
#         format(tn=table_name, cn=column_2, idf=id_column, my_id=some_id))
# id_exists = c.fetchone()
# if id_exists:
#     print('5): {}'.format(id_exists))
# else:
#     print('5): {} does not exist'.format(some_id))

# Closing the connection to the database file
conn.close()
