import random
import sqlite3


def get_num_tweets(sqlite_db, tab_name, auth_id):
    conn = sqlite3.connect(sqlite_db)
    c = conn.cursor()
    sql = 'SELECT TWEET_COUNT FROM {tn} WHERE AUTHOR_ID="{a_id}"'.\
          format(tn=tab_name, a_id=auth_id)
    print(sql)
    count = c.execute(sql)
    result = c.fetchone()[0]
    print(result)
    return(result)


def get_random_tweets(sqlite_db, twt_tbl, auth_tbl, auth_id, num_req, rnd_seed):
    """ Queries tweet table for all tweets from one author based on author id and table name
        sqlite_db: sqlite3 database
        twt_tbl: table with tweets
        auth_tbl: table with eligible authors (enough tweets for training threshold)
        auth_id: author id
        num_req: number of tweets required for author profile training
        Returns tweets as list of tuples with one element """
    conn = sqlite3.connect(sqlite_db)
    c = conn.cursor()
    # get the number of tweets available for a given author and select threshold + 1 for experiments
    # get number of tweets
    num_twts = get_num_tweets(sqlite_db, auth_tbl, auth_id)
    # print(num_twts)
    # random seed for reproducing experimental results
    random.seed(rnd_seed)
    # list of message id's to use in testing
    message_list = random.sample(range(1, num_twts), num_req)
    print(message_list)
    # build the sql statement
    param = '?'
    params = ','.join(param*len(message_list))
    sql = "SELECT TWEET_MSG FROM {tn} WHERE AUTHOR_ID='{a_id}' AND MESSAGE_NUM IN ({prms})".\
           format(tn=twt_tbl, a_id=auth_id, prms=params)
    print(sql)
    # c.execute('SELECT TWEET_MSG FROM {tn} WHERE AUTHOR_ID="{a_id}" AND MESSAGE_NUM IN "{m_lst}"'. \
    #           format(tn=twt_tbl, a_id=auth_id), m_lst=','.join(['?']*len(message_list)))
    c.execute(sql,message_list)
    conn.commit()
    twts = c.fetchall()
    # printing the tweets to validate selection
    # for tweet_tup in twts:
    #     for tweet in tweet_tup:
    #         print(tweet.rstrip())
    conn.close()
    return(twts)

# sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file
# author_id = "000454c774d4c43d40b92ff720c72446217a66b2"
# author_table = "ELIGIBLE_AUTHORS"
# tweet_table = "TWEETS"
# get_random_tweets(sqlite_file, tweet_table, author_table, author_id, 60)