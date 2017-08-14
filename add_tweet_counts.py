import sqlite3


def return_authors(tab_name):
    """ Returns list of all author ids and author names from the author table """
    auths = {}
    c.execute('SELECT AUTHOR_ID,AUTHOR_NM FROM {tn}'. \
              format(tn=tab_name))
    auths = c.fetchall()
    return auths


def count_tweets(tab_name, id_col, auth_id):
    """ Counts the number of tweets for a given author in the tweet table """
    c.execute('SELECT * FROM {tn} WHERE {cn}="{a_id}"'. \
              format(tn=tab_name, cn=id_col, a_id=auth_id))
    tweets = c.fetchall()
    return(len(tweets))


def update_authors(author_table, tweet_table, auth_id):
    all_authors = return_authors(author_table)
    query = 'UPDATE AUTHORS SET TWEET_COUNT = (?) WHERE AUTHOR_ID = (?)'
    for key, author in all_authors:
        num_tweets = count_tweets(tweet_table, auth_id, key)
        c.execute(query, (num_tweets, key))
        # print(author + ": " + str(num_tweets))


table_name = 'AUTHORS'   # name of the table to be queried
table_name2 = 'TWEETS'   # name of the table to be queried
id_column = 'AUTHOR_ID'  # author id column name in both tables
sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
update_authors(table_name, table_name2, id_column)

conn.commit()
conn.close()
