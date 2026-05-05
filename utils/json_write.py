import os

def json_write(file_name, data):
    with open(os.path.abspath(os.path.join(__file__, "..", "..", "json", file_name))) as file:
        file.write(data)