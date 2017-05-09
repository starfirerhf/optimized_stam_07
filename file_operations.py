import os


def get_file_names(src_folder):
    file_names = os.listdir(src_folder)
    return(file_names)


def print_file_names(list):
    for item in list:
        print(item)


def print_file(file):
    with open(file,mode='r',encoding='utf-8') as file_object:
        lines = file_object.readlines()
        for line in lines:
            try:
                print(line.rstrip())
            except UnicodeDecodeError:
                print("UnicodeDecodeError handled!")
                pass


def count_lines(file):
    count = 0
    with open(file,mode='r',encoding='utf-8') as file_object:
        lines = file_object.readlines()
        for line in lines:
            count += 1
    return count

