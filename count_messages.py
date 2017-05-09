import file_operations
import os
import json

def count_tweets(src):
    # Counts tweets from author file
    files = file_operations.get_file_names(src)
    for file in files:
        count = 0
        print("File: " + os.path.join(src, file))
        #   file_operations.print_file(os.path.join(src_folder,file))
        with open(os.path.join(src, file), mode='r', encoding='utf-8') as file_object:
            lines = file_object.readlines()
            for line in lines:
                # check each line of the file and only increment counter if the end of the message is detected
                if line.rstrip() == "{" or line.rstrip() == "}" or line[:4] == "#POS":
                    # report message start count
                    # if line.rstrip() == "{":
                    #     print("Message start: " + str(count))
                    # report message end count and increment counter
                    if line.rstrip() == "}":
                        count += 1
                        # print("Message end: " + str(count))
                    # report POS start count
                    # if line.rstrip() == "#POS":
                    #     print("POS LINE: " + str(count))
            print("Number of tweets: " + str(count))


def parse_tweets(src):
    messages = []
    tweet_dict = {}
    outstem = "messsage"
    outsuffix = ".txt"
    # assembles tweets to a list of tweets and returns the list of tweets for a given author
    files = file_operations.get_file_names(src)
    for file in files:
        count = 0
        print("Tweets in file " + os.path.join(src, file))
        os.makedirs(os.path.join(src,file[:-4]))
        with open(os.path.join(src,file), mode='r', encoding='utf-8') as file_object:
            lines = file_object.readlines()
            for line in lines:
                if line.rstrip() == "{":
                    message = ''
                    pass
                elif line[:4] == "#POS":
                    pass
                elif line.rstrip() == "}":
                    print('Tweet: ' + message)
                    messages.append(message)
                    count += 1
                    with open(os.path.join(os.path.join(src,file[:-4]),outstem + str(count) + outsuffix),'a',encoding='utf-8') as outfile:
                        outfile.write(message)
                    print("Tweet count: " + str(count))
                else:
                    message += line.rstrip()
    return tweet_dict


def write_json(dictionary,output_file):
    with open(testfile, 'a', encoding="utf-8") as outfile:
        json.dump(dict, outfile, indent=4)


src_folder = 'D:\\RochaPartial'
# file_operations.print_file_names(files)

# count_tweets(src_folder)
parse_tweets(src_folder)
testfile = "out-test.json"
