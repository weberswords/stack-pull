import json

def write_to_json_file(data, file_name):
    with open(file_name, 'x+') as file:
        file.write(json.dumps(data))