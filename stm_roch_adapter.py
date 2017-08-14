import sqlite3
import os
import shutil
import json
import random_authors
import build_meta
import random_tweets


def return_random_authors(sqlite_db, tbl_nm, seed, num_auths):
    """ Returns list of random author ids and author names from the author table """
    id_list = random_authors.get_id_list(sqlite_db, tbl_nm, seed, num_auths)
    # print(id_list)
    id_list_str = repr(id_list).replace('[', '(').replace(']', ')')
    auths = {}
    # c.execute('SELECT AUTHOR_ID,AUTHOR_NM FROM {tn} WHERE rowid in {lst}'. \
    #            format(tn=tbl_nm, lst=id_list_str))
    c.execute('SELECT AUTHOR_ID,AUTHOR_NM FROM {tn} WHERE rowid in {lst}'. \
               format(tn=tbl_nm, lst=id_list_str))
    auths = c.fetchall()
    # print(auths)
    return(auths)


def count_tweets(tab_name, id_col, auth_id):
    """ Counts the number of tweets for a given author in the tweet table """
    c.execute('SELECT * FROM {tn} WHERE {cn}="{a_id}"'. \
              format(tn=tab_name, cn=id_col, a_id=auth_id))
    tweets = c.fetchall()
    return(len(tweets))


def get_authors_over_threshold(auths, twt_table, limit, num):
    """ Returns a list of authors with number of tweets above selected threshold """
    over_threshold = []
    count = 0
    # iterate through authors to find those with more than threshold number of tweets
    for key, auth in auths:
        num_tweets = count_tweets(twt_table, id_column, key)
        # commenting following line to improve speed
        # print(key + ':' + author)
        # print("Number of tweets for " + author + ": " + str(tweets))
        if num_tweets >= limit:
            over_threshold.append(key)
            count += 1
        # Status update - break when enough authors have been found for testing
        if count == num:
            print('Number of candidates: ' + str(len(over_threshold)))
            break
    return(over_threshold)


def get_tweet(tab_name, auth_id, tweet_num):
    """ Queries tweet table for one tweet based on author id and tweet number
        Returns a tweet as a string """
    twt_str = ''
    c.execute('SELECT TWEET_MSG FROM {tn} WHERE AUTHOR_ID="{a_id}" AND MESSAGE_NUM="{twn}"'. \
              format(tn=tab_name, a_id=auth_id, twn=tweet_num))
    twt = c.fetchone()
    for t in twt:
        twt_str += t
    return(twt_str)


def get_all_tweets(tab_name, auth_id):
    """ Queries tweet table for all tweets from one author based on author id and table name
        Returns tweets as list of tuples with one element """
    c.execute('SELECT TWEET_MSG FROM {tn} WHERE AUTHOR_ID="{a_id}"'. \
              format(tn=tab_name, a_id=auth_id))
    twts = c.fetchall()
    return(twts)


def write_training(t_str, msg_num, auth, out_dir):
    """ Takes a tweet string, message number, author, and target output directory and writes the tweet to a file """
    trn_stem = "known"
    num_str = str(msg_num).rjust(5, '0')
    trn_suffix = ".txt"
    trn_file = trn_stem + num_str + trn_suffix
    target_dir = os.path.join(out_dir, auth)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    with open(os.path.join(target_dir, trn_file), 'w', encoding="utf-8") as outfile:
        outfile.write(t_str)


def write_testing(t_str, msg_num, auth, out_dir):
    """ Takes a tweet string, message number, author, and target output directory and writes the tweet to a file """
    trn_stem = "unknown"
    num_str = str(msg_num).rjust(5, '0')
    trn_suffix = ".txt"
    trn_file = trn_stem + num_str + trn_suffix
    # target_dir = os.path.join(out_dir, auth)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, trn_file), 'w', encoding="utf-8") as outfile:
        outfile.write(t_str)


def delete_files(out_dir):
    """ Takes a tweet string, message number, author, and target output directory and writes the tweet to a file """
    for root, dirs, files in os.walk(out_dir):
        for file in files:
            os.unlink(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))


# declare variables ##################################################################################################
# source database variables
metafile = "meta-file.json"
gtfile = "ground-truth.json"
outdir = "D:\\RochaTwitterData\\VariantD"   # output directory for extracted data files
sqlite_file = 'twitter_r_data.sqlite'       # name of the sqlite database file
author_table = 'AUTHORS'                      # name of the table to be queried
tweet_table = 'TWEETS'                      # name of the table to be queried
eligible_auth_table = 'ELIGIBLE_AUTHORS'            # name of the table to be queried
id_column = 'AUTHOR_ID'                     # author id column name in both tables
column_2 = 'MESSAGE_NUM'                    # message number for a candidate
column_3 = 'TWEET_MSG'                      # tweet message content
column_4 = 'POS_MSG'                        # part of speech tags for tweets

# data structures ####################################################################################################
truth =[]
g_truth = {}
author_list = []
unknown_list = []

# Experimental Variables #############################################################################################
# minimum number of tweets - at 132, this sets a minimum of 120 training tweets and allows 10% hold out for testing
threshold = 120            # training set size
threshold_check = 0       # counter to compare to threshold
random_seed = 10
# number of candidates considered - for scaling out - can remove if determined computationally feasible
num_candidates = 10        # number of candidate authors
tst_cnt = 0               # counts number of unknown messages

# empty target directory
delete_files(outdir)
# Connect to the database
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
# get random eligible authors from eligible_author table
authors = return_random_authors(sqlite_file, eligible_auth_table, random_seed, num_candidates)
valid_candidates = get_authors_over_threshold(authors, tweet_table, threshold, num_candidates)
# print(authors)
# print(valid_candidates)
# get tweets for training profile
for candidate in valid_candidates:
    # print(candidate)
    tweet_tups = random_tweets.get_random_tweets(sqlite_file, tweet_table, author_table,\
                                                 candidate, threshold + 1, random_seed)
    # dictionary for the candidate author - primarily for json format
    c_list = {}
    c_list["author-name"] = candidate
    author_list.append(c_list)
    print('\n' + str(threshold) + ' Tweets from:' + candidate)
    # print(tweet_tups)
    for tweet_tup in tweet_tups:
        for tweet in tweet_tup:
            truth_line_dict = {}
            # write 60 messages to author folder for training
            if threshold_check < threshold:
                print("Tweet:" + str(threshold_check))
                print(tweet.rstrip())
                write_training(tweet.rstrip(), threshold_check, candidate, outdir)
                threshold_check += 1
            # write 1 message per candidate to unknown folder for testing and ground-truth
            elif threshold_check == threshold:
                u_list = {}
                u_list["unknown-text"] = "unknown" + str(tst_cnt).rjust(5, '0') + ".txt"
                unknown_list.append(u_list)
                truth_line_dict["true-author"] = candidate
                truth_line_dict["unknown-text"] = "unknown" + str(tst_cnt).rjust(5, '0') + ".txt"
                truth.append(truth_line_dict)
                print("Tweet:" + str(threshold_check))
                print(tweet.rstrip())
                write_testing(tweet.rstrip(), tst_cnt, candidate, os.path.join(outdir,"unknown"))
                threshold_check += 1
                tst_cnt += 1
            else:
                break
    threshold_check = 0

meta = build_meta.build_meta_dict(author_list, unknown_list)
with open(os.path.join(outdir, metafile),'a',encoding="utf-8") as m_outfile:
    json.dump(meta, m_outfile, indent=0)

g_truth = build_meta.build_ground_truth(truth)
with open(os.path.join(outdir, gtfile), 'a', encoding="utf-8") as gt_outfile:
    json.dump(g_truth, gt_outfile, indent=0)

# Closing the connection to the database file
conn.close()
