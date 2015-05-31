import sys
import json


def recursive_print(item, attrib):
    if len(attrib) > 1:
        return recursive_print(item[attrib[0]],attrib[1:])
    else:
        return item[attrib[0]]

if len(sys.argv) < 3:
    print 'Please give me a JSON file; and a variable name you want me to return the value.'
else:
    file_name = sys.argv[1]

    with open(file_name) as data_file:    
        data = json.load(data_file)
        for item in data:
            print(recursive_print(item,sys.argv[2].split('/')))
