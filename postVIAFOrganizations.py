import json, requests, secrets, csv, time

startTime = time.time()

# print instructions
print 'This script takes viafCorporateResults.csv and posts the organizations as corporate_entities to ArchivesSpace.'
raw_input('Press Enter to continue...')

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

#authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

targetFile = 'viafCorporateResults.csv'

csv = csv.DictReader(open(targetFile))

orgList = []
for row in csv:
    orgRecord = {}
    orgRecord['names'] = [{'primary_name': row['result'], 'sort_name': row['result'], 'source': 'viaf', 'authority_id': row['viaf']}]
    orgRecord = json.dumps(orgRecord)
    post = requests.post(baseURL + '/agents/corporate_entities', headers=headers, data=orgRecord).json()
    print post

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
