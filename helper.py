import csv
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

def sort_by_views(list):
    list.sort(key=get_key_by_views)
    return list

