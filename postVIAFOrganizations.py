# This script takes people.csv and posts the individuals as agents to ArchivesSpace.

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
    orgRecord['primary_name'] = row['result']
    orgRecord['authority_id'] = row['viaf']
    orgRecord = json.dumps(orgRecord)
    print orgRecord
    # post = requests.post(baseURL + '/repositories/3/top_orgs', headers=headers, data=orgRecord).json()
    # print post
    # orgList.append(post['uri'].encode('utf-8'))

# asRecord = requests.get(baseURL+'/repositories/3/'+targetRecord, headers=headers).json()
# instanceArray = asRecord['instances']
#
# for i in range (0, len (orgList)):
#     top_org = {}
#     top_org['ref'] = orgList[i]
#     sub_org = {}
#     sub_org['top_org'] = top_org
#     instance = {}
#     instance['sub_org'] = sub_org
#     instance['instance_type'] = 'mixed_materials'
#     instanceArray.append(instance)
#
# asRecord['instances'] = instanceArray
# asRecord = json.dumps(asRecord)
# post = requests.post(baseURL+'/repositories/2/'+targetRecord, headers=headers, data=asRecord).json()
# print post
