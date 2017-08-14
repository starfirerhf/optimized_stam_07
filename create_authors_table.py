# Creating a new SQLite database for Rocha Twitter Data
import sqlite3


class Sqlite_Table():
    """Generic class for creating sqlite table from dictionary"""

    def __init__(self, sqlite_db, table_name, table_def):
        """
        Initialize table with column:col_type dictionary definition
        :param sqlite_db: An existing sqlite database
        :param table_name: A name for the new table
        :param table_def: Column definitions - ex. [{'user_id': 'text primary key'},{'user': 'text'}]
        :return: returns nothing
        """
        status = False
        self.sqlite_db = sqlite_db
        self.table_name = table_name
        self.build_table(sqlite_db, table_name, table_def)


    def build_table(self, sqlite_db, table_name, table_def):
        """
        The primary constructor for an sqlite table
        :param table_name: A name for the new table
        :param table_def: Column definitions - ex. [{'user_id': 'text primary key'},{'user': 'text'}]
        :return: returns nothing, but creates a table in the sqlite database specified in __init__
        """
        # creates the sql statement for creating the table
        create_sql = 'CREATE TABLE ' + table_name + ' ('
        # loop through all but the last item and add column name and type to the sql statement as well as ','
        for column in table_def[:-1]:
            for col in column:
                create_sql += col + ' ' + column[col] + ','
        # add final column name and type with closing ')'
        for column in table_def[-1:]:
            for col in column:
                create_sql += col + ' ' + column[col] + ')'
        print('SQL Statement:')
        print(create_sql)
        try:
            # connect to the sqlite database
            conn = sqlite3.connect(sqlite_db)
            c = conn.cursor()
            # create the table using the sql statement
            c.execute(create_sql)
            # commit changes and close the connection
            conn.commit()
            conn.close()
            print('Table creation succeeded')
        except:
            print('Table creation failed')



sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file
# sqlite_file = 'my_first_db.sqlite'    # name of the sqlite database file

table_def = [{"AUTHOR_ID": "TEXT PRIMARY KEY"},\
             {"AUTHOR_NM": "TEXT"},\
             {"TWEET_COUNT": "INTEGER"}]

print(table_def)
table_name = 'ELIGIBLE_AUTHORS'	# name of the table to be created
new_table = Sqlite_Table(sqlite_file, table_name, table_def)
