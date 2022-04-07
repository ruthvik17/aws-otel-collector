import json
import sys

# the file to be converted to 
# json format
args = sys.argv
filename = str(args[1])

# dictionary where the lines from
# text will be stored


# fields in the sample file 
fields =['job_name', 'curent_job', 'log']

# p = 0
# creating dictionary
with open(filename) as fh:
    line_no = 1
    for line in fh:
        dict1 = {}

        id_dict = { "_index": "logs", "_id" : str(line_no + 1) }
        dict1["index"] = id_dict
        
        # reads each line and trims of  the extra spaces 
        # and gives only the valid words
        description = list( line.strip().split('\t', 3))
        # print(description)
        # loop variable

        if len(description) < len(fields):
            # dict2[line_no] = description
            # line_no += 1
            continue
        
        i = 0
        # intermediate dictionary
        dict2 = {}
        while i<len(fields):
              
                # creating dictionary for each employee
                dict2[fields[i]]= description[i]
                i = i + 1
                  
        # appending the record of each employee to
        # the main dictionary
        
        # print(dict1)
        line_no += 1


        data = [ dict1, dict2]


        with open('test_json_py.json', 'a') as fp:
            fp.write(
            '\n'.join(json.dumps(i) for i in data) + '\n')

