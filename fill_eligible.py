import sqlite3


def get_tweets(sqlite_db, tbl_name, count):
    sql = 'SELECT * FROM {tn} WHERE TWEET_COUNT > (?)'.format(tn=tbl_name)
    conn = sqlite3.connect(sqlite_db)
    c = conn.cursor()
    c.execute(sql, (count,))
    all_rows = c.fetchall()
    conn.commit()
    conn.close()
    return(all_rows)


def fill_table(sqlite_db, tbl_name, all_rows):
    conn = sqlite3.connect(sqlite_db)
    c = conn.cursor()
    # Insert eligible author
    sql_start = 'INSERT OR IGNORE INTO '
    sql_end = ' VALUES (?,?,?)'
    query = sql_start + tbl_name + sql_end
    c.executemany(query, all_rows)
    conn.commit()
    conn.close()


source_table_name = 'AUTHORS'   # name of the table to be queried
target_table_name = 'ELIGIBLE_AUTHORS'   # name of the table to be queried
sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file
threshold = 120
t_plus_10 = (threshold * 0.1) + threshold
data = get_tweets(sqlite_file, source_table_name, t_plus_10)
fill_table(sqlite_file, target_table_name, data)
