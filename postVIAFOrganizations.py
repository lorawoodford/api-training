# This script takes viafCorporateResults.csv and posts the organizations as corporate_entities to ArchivesSpace.

import json, requests, secrets, csv

targetFile = 'viafCorporateResults.csv'

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

#authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

csv = csv.DictReader(open(targetFile))

orgList = []
for row in csv:
    orgRecord = {}
    orgRecord['names'] = [{'primary_name': row['result'], 'sort_name': row['result'], 'source': 'viaf', 'authority_id': row['viaf']}]
    orgRecord = json.dumps(orgRecord)
    post = requests.post(baseURL + '/agents/corporate_entities', headers=headers, data=orgRecord).json()
    print post
