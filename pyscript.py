import json
import sys
import os
import requests
from time import sleep

print(os.environ, "\n")

headers = {
    'Accept': 'application/vnd.github.v3+json',
}

run_id = os.environ['GITHUB_RUN_ID']
repo = os.environ['GITHUB_REPOSITORY']


try:
    job_list = requests.get(f'https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs', headers=headers)
except requests.exceptions.ConnectionError:
    print("Connection refused. Sleeping.......")
    sleep(0.5)

# job_list = requests.get(f'https://HOSTNAME/api/v3/repos/ruthvik17/aws-otel-collector/actions/runs/{run_id}/jobs', headers=headers)

# print(job_list.json())

job_data = job_list.json()

#Get Job Id
job_id = job_data['jobs'][0]['id']

headers = {
    'Accept': 'application/vnd.github.v3+json',
}

try:
    job_logs= requests.get(f'https://api.github.com/repos/{repo}/actions/jobs/{job_id}/logs', headers=headers)
except requests.exceptions.ConnectionError:
    print("Connection refused. Sleeping.......")
    sleep(0.5)
    
    
print('Job logs \n', job_logs.json())

with open('test_json_py.json', 'a') as fp:
     fp.write(json.dumps(job_data) + '\n')

## Write to OpenSearch

headers = {
    'Content-Type': 'application/json',
}

with open('test_json_py.json', 'rb') as f:
    data = f.read().replace(b'\n', b'')

print("\nOpenSearch data\n", data)

try:
    response = requests.post('https://search-gh-test-mn2dq77arhyercpvg3sgdihpnq.us-west-2.es.amazonaws.com/_bulk', headers=headers, data=data, auth=('ruthvik', 'Ruthvik-19'))
except requests.exceptions.ConnectionError:
    print('\nConnection error')
    
print("\nOpenSearch response\n", response.json())



# # the file to be converted to 
# # json format
# args = sys.argv
# filename = str(args[1])

# dictionary where the lines from
# text will be stored



# dictionary where the lines from
# text will be stored


# fields in the sample file 
# fields =['job_name', 'curent_job', 'log']

# # p = 0
# # creating dictionary
# with open(filename) as fh:
#     line_no = 1
#     for line in fh:
#         dict1 = {}

#         id_dict = { "_index": "logs", "_id" : str(line_no + 1) }
#         dict1["index"] = id_dict
        
#         # reads each line and trims of  the extra spaces 
#         # and gives only the valid words
#         description = list( line.strip().split('\t', 3))
#         # print(description)
#         # loop variable

#         if len(description) < len(fields):
#             # dict2[line_no] = description
#             # line_no += 1
#             continue
        
#         i = 0
#         # intermediate dictionary
#         dict2 = {}
#         while i<len(fields):
              
#                 # creating dictionary for each employee
#                 dict2[fields[i]]= description[i]
#                 i = i + 1
                  
#         # appending the record of each employee to
#         # the main dictionary
        
#         # print(dict1)
#         line_no += 1


#         data = [ dict1, dict2]


#         with open('test_json_py.json', 'a') as fp:
#             fp.write(
#             '\n'.join(json.dumps(i) for i in data) + '\n')


# print('Uploaded the data')
