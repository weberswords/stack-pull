from audioop import reverse
import csv
import datetime
import json
import os

def write_to_json_file(data, file_name):
    try:
        print("Removing existing file...")
        os.remove(file_name)
        print(f"{file_name} removed.")
        print("Writing new data...")
        with open(file_name, 'x+') as file:
            file.write(json.dumps(data))
    except FileNotFoundError:
        print("Writing new data...")
        with open(file_name, 'x+') as file:
            file.write(json.dumps(data))
   
def just_write(data, file_name):
    with open(file_name, "a") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)

def write_to_csv_file(headers, data, file_name):
    try:
        print("Removing existing file...")
        os.remove(file_name)
        print(f"{file_name} removed.")
        print("Writing new data...")
        with open(file_name, "x+") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvwriter.writerows(data)

    except FileNotFoundError:
        print("Writing new data...")
        with open(file_name, "x+") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvwriter.writerows(data)

def get_key_by_views(obj):
    return obj['view_count']

def get_key_by_answer_count(obj):
    return obj['answer_count']
def sort_by_views(list):
    list.sort(key=get_key_by_views)
    return list

def sort_by_answers(list):
    list.sort(key=get_key_by_answer_count, reverse=True)
    return list
def convert_from_epoch(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time)

def calculate_next_page(page):
    return int(page) + 1

def get_count_of_json(file):
    with open(file, "r") as file_to_count:
        answers = json.load(file_to_count)
        print(len(answers))

