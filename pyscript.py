import json
import sys
import os
import requests
from time import sleep

headers = {
    'Accept': 'application/vnd.github.v3+json',
}

run_id = os.environ['GITHUB_RUN_ID']
repo = os.environ['GITHUB_REPOSITORY']

# Look at the workflow data

try:
    job_list = requests.get(f'https://api.github.com/repos/{repo}/actions/runs/{run_id}/jobs', headers=headers)
except requests.exceptions.ConnectionError:
    print("Connection refused. Sleeping.......")
    sleep(0.5)

job_data = job_list.json()

keys = list(job_data["jobs"][0].keys())

id_no = 0

# Loop through jobs data
for job in job_data["jobs"]:
    dict1 = {}
    for key in keys:
        if key != 'steps':
            dict1[f'job_{key}'] = job[key]
    
    for step in job['steps']:
        for info in list(step.keys()):
            dict1[f'{key}_{info}'] = step[info]
            id_no += 1
            dict1[f'steps_{info}'] = step[info]
        dict2 = {"index" : { "_index": "workflow_data", "_id" : id_no } }
        dicts = [dict2, dict1]
        # Write to file
        with open('meta_json.json', 'a') as fp:
            fp.write(
            '\n'.join(json.dumps(dict) for dict in dicts) + '\n')

# Push to data table on OpenSearch
headers = {
    'Content-Type': 'application/json',
}

with open('meta_json.json', 'rb') as f:
    data = f.read()

response = requests.post('https://search-gh-test-mn2dq77arhyercpvg3sgdihpnq.us-west-2.es.amazonaws.com/_bulk', 
                         headers=headers, data=data, auth=('ruthvik', 'Ruthvik-19'))


item_num = len(response.json()["items"])

print(f"Pushed {item_num} data items to Opensearch")

## Look at logs

GITHUB_TOKEN = os.environ['PAT_ACCESS']

headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': f"token {GITHUB_TOKEN}",
}   

id_no = 0 
for job in job_data["jobs"]:
    dict1 = {}
    job_id = job["id"]
    id_no += 1
    # print(job_id)
    try:
        job_log = requests.get(f'https://api.github.com/repos/{repo}/actions/jobs/{job_id}/logs', headers=headers)
    except requests.exceptions.ConnectionError:
        print("Connection refused. Sleeping.......")
        sleep(0.5)

    dict1 = {}
    dict1["job_id"] = job["id"]
    dict1["run_id"] = job["run_id"]
    dict1['job_run_attempt'] = job['run_attempt']
    dict1['job_status'] = job['status']
    dict1['job_conclusion'] = job['conclusion']
    dict1['logs'] = f"{job_log.text}"

    dict2 = {"index" : { "_index": "workflow_logs", "_id" : f"{id_no}" } }

    dicts = [dict2, dict1]

    with open('meta_json_logs.json', 'a') as fp:
        fp.write(
        '\n'.join(json.dumps(dict) for dict in dicts) + '\n')

headers = {
    'Content-Type': 'application/json',
}

with open('meta_json_logs.json', 'rb') as f:
    data = f.read()

response = requests.post('https://search-gh-test-mn2dq77arhyercpvg3sgdihpnq.us-west-2.es.amazonaws.com/_bulk', headers=headers, data=data, auth=('ruthvik', 'Ruthvik-19'))

print("OPensearch response \n ", response.json())

item_num = len(response.json()["items"])

print(f'\nUploaded {item_num} items to the logs table')
