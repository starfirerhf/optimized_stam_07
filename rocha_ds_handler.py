import sqlite3
import file_operations
import os

def author_query(tbl_nm):
    """
    Builds a query to write to the author table
    """
    sql_start = 'INSERT OR IGNORE INTO '
    sql_end = ' VALUES (?,?)'
    return(sql_start + tbl_nm + sql_end)


def message_query(tbl_nm):
    """
    Builds a query to write to the messages table
    """
    sql_start = 'INSERT INTO '
    sql_end = ' VALUES (?,?,?,?)'
    return(sql_start + tbl_nm + sql_end)


def parse_tweets():
    src_folder = 'D:\\datasetPOS_anonymized_tagged'
    sqlite_file = 'twitter_r_data.sqlite'
    author_table = 'AUTHORS'  # name of the table to be created
    msg_table = 'TWEETS'  # name of the table to be created
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    auth_num = 0
    files = file_operations.get_file_names(src_folder)
    for file in files:
        c.execute(author_query(author_table), (file[:-4], ("author_"+str(auth_num))))
        count = 0
        print("Tweets in file " + os.path.join(src_folder, file))
        with open(os.path.join(src_folder, file), mode='r', encoding='utf-8') as file_object:
            lines = file_object.readlines()
            is_tweet = False
            is_pos = False
            for line in lines:
                # print(line.rstrip())
                # if it's the beginning of a message, reset tweet and pos_cd, identify as a tweet
                if line.rstrip() == "{":
                    print("message start")
                    is_tweet = True
                    tweet = ''
                    pos_cd = ''
                elif line.strip()[-4:] == "#POS":
                    print("pos_end")
                    is_pos = False
                    is_tweet = False
                    pos_cd += line
                elif line[:4] == "#POS":
                    print("pos")
                    is_pos = True
                    is_tweet = False
                    pos_cd += line
                elif is_tweet:
                    print("tweet")
                    tweet += line
                elif is_pos:
                    print("pos")
                    pos_cd += line
                elif line.rstrip() == "}":
                    is_pos = False
                    is_tweet = False
                    print('writing')
                    count += 1
                    c.execute(message_query(msg_table), (file[:-4], str(count), tweet, pos_cd))
                else:
                    print("You missed a condition!")
            print("Tweet count: " + str(count))
        auth_num += 1
    conn.commit()
    conn.close()


parse_tweets()
