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

# Look at the work

headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': access_token
}

try:
    job_logs= requests.get(f'https://api.github.com/repos/{repo}/actions/jobs/{job_id}/logs', headers=headers)
except requests.exceptions.ConnectionError:
    print("Connection refused. Sleeping.......")
    sleep(0.5)
    
 try:
    job_list = requests.get('https://api.github.com/repos/ruthvik17/aws-otel-collector/actions/runs/2168746686/jobs', headers=headers)
except requests.exceptions.ConnectionError:
    print("Connection refused. Sleeping.......")
    sleep(0.5)

job_data = job_list.json()

print("\nTotal count of jobs", len(job_data["jobs"]))

job_id = job_data["jobs"][0]["id"]

keys = list(job_data["jobs"][0].keys())
id_no = 0
for job in job_data["jobs"]:
    id_no += 1
    dict1 = {}
    for key in keys:
        if key != 'steps':
            dict1[f'job_{key}'] = job[key]
        else:
            for step in job[key]:
                for info in list(step.keys()):
                    dict1[f'{key}_{info}'] = step[info]

    dict1["job_id"] = f"{id_no}"

    dict2 = {"index" : { "_index": "workflow_data", "_id" : f"{id_no}" } }

    dicts = [dict2, dict1]
    with open('meta_json.json', 'a') as fp:
        fp.write(
        '\n'.join(json.dumps(dict) for dict in dicts) + '\n')

headers = {
    'Content-Type': 'application/json',
}

with open('meta_json.json', 'rb') as f:
    data = f.read()

response = requests.post('https://search-gh-test-mn2dq77arhyercpvg3sgdihpnq.us-west-2.es.amazonaws.com/_bulk', headers=headers, data=data, auth=('ruthvik', 'Ruthvik-19'))

print("OPensearch response \n ", response.json())

print('\nUploaded to the data table')

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
        job_log = requests.get(f'https://api.github.com/repos/ruthvik17/aws-otel-collector/actions/jobs/{job_id}/logs', headers=headers)
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

print('\nUploaded to the logs table')
