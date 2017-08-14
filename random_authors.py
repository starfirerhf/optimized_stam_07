import random
import sqlite3


def count_authors(sqlite_db, tbl_nm):
    conn = sqlite3.connect(sqlite_db)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM {tn}'. \
              format(tn=tbl_nm, cn='rowid'))
    conn.commit()
    count = c.fetchone()
    num_auths = count[0]
    conn.close()
    return(num_auths)


def get_id_list(sqlite_db, tbl_nm, rnd_seed, num_ids):
    num_authors = count_authors(sqlite_db, tbl_nm)
    print('Number of authors: ')
    print(num_authors)
    random.seed(rnd_seed)
    rand_list = random.sample(range(1, num_authors), num_ids)
    # print('Author rowid list:')
    # for num in rand_list:
    #     print(num)
    return(rand_list)


# table_name = 'ELIGIBLE_AUTHORS'   # name of the table to be queried
# sqlite_file = 'twitter_r_data.sqlite'    # name of the sqlite database file
# random_seed = 500
# number_ids = 5
#
# get_id_list(sqlite_file, table_name, random_seed, number_ids)
