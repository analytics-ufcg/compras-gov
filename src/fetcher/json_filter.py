import sys
import json


def recursive_look(item, attrib):
    if len(attrib) > 1:
        return recursive_look(item[attrib[0]],attrib[1:])
    else:
        return item[attrib[0]]

if len(sys.argv) < 6:
    print '''Please give me: 
             [1] a JSON file; 
             [2] the name of the JSON element to look inside; 
             [3] the variable name to filter with; 
             [4] the value to look;
             [5] output file name'''
else:
    file_name = sys.argv[1]
    attrib_names = sys.argv[2:]
    output_data = []

    with open(file_name) as data_file:    
        data = json.load(data_file)
        for item in data[attrib_names[0]]:
            value = recursive_look(item,attrib_names[1].split('/'))
            if value == attrib_names[2]:
                output_data.append(item)
    output_file = open(attrib_names[3],'w')
    json.dump(output_data,output_file)

