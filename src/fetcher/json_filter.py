import sys
import json


def recursive_print(item, attrib):
    if len(attrib) > 1:
        return recursive_print(item[attrib[0]],attrib[1:])
    else:
        return item[attrib[0]]

if len(sys.argv) < 3:
    print 'Please give me a JSON file and a list of variables to filter from its items.'
else:
    file_name = sys.argv[1]
    attrib_names = sys.argv[2:]

    with open(file_name) as data_file:    
        data = json.load(data_file)
        for item in data[attrib_names[0]]:
            print(recursive_print(item,attrib_names[1].split('/')))