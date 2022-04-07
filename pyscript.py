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

        out_file = open("test_json_py.json", "a")
        index_dict = json.dumps(dict1, indent = 0)
        out_file.write(index_dict)
        out_file.write("\n")
        log_dict = json.dumps(dict2, indent = 0)
        out_file.write(log_dict)
        out_file.write("\n")
        out_file.close()

        if line_no > 7:
            break
        # p += 1

        # if p > 5:
        #     break
# print(type(dict1))
# print([dict1.keys()][:5])
# creating json file
# the JSON file is named as test1
# out_file = open("test_json.json", "a")
# out_file.write("\n")
# out_file.close()
# from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
# import boto3

# host = 'https://search-gh-actions-test-toozusakad3jibpfljps5rvmdm.us-west-2.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
# region = 'us-west-2' # e.g. us-west-1

# credentials = boto3.Session().get_credentials()
# auth = AWSV4SignerAuth(credentials, region)

# client = OpenSearch(
#     hosts = [{'host': host, 'port': 443}],
#     http_auth = auth,
#     use_ssl = True,
#     verify_certs = True,
#     connection_class = RequestsHttpConnection
# )
# id = '1'
# for key, log in dict1.items():
#     response = client.index(
#     index = key,
#     body = log,
#     )
#     id = str(int(id) + 1)

