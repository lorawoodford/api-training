import json, requests, csv, time, secrets

startTime = time.time()

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

# test for successful connection
def test_connection():
	try:
		requests.get(baseURL)
		print 'Connected!'
		return True

	except requests.exceptions.ConnectionError:
		print 'Connection error. Please confirm ArchivesSpace is running.  Trying again in 10 seconds.'

is_connected = test_connection()

while not is_connected:
	time.sleep(10)
	is_connected = test_connection()

#authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

# User supplied variables
do_csv = raw_input('Enter csv filename: ')

# Open csv, create new csv
csv_dict = csv.DictReader(open(do_csv))
f=csv.writer(open('new_' + do_csv, 'wb'))
f.writerow(['title']+['digital_object_id']+['digital_object_uri']+['archival_object_uri'])

# Parse csv
for row in csv_dict:
	file_uri = row['fileuri']
	title = row['title']
	digital_object_id = row['objectid']
	ref_ID = row['refID']
	# Construct new digital object from csv
	doRecord = {'title': title, 'digital_object_id': digital_object_id, 'publish': False}
	doRecord['file_versions'] = [{'file_uri': file_uri, 'publish': False, 'file_format_name': 'jpeg'}]
	doRecord = json.dumps(doRecord)
	doPost = requests.post(baseURL + '/repositories/2/digital_objects', headers=headers, data=doRecord).json()
	print doPost
	# Store uri of newly posted digital objects because we'll need it
	uri = doPost['uri']
	# Find AOs based on refIDs supplied in csv
	AOquery = '/search?page=1&filter={"query":{"jsonmodel_type":"boolean_query","op":"AND","subqueries":[{"jsonmodel_type":"field_query","field":"primary_type","value":"archival_object","literal":true},{"jsonmodel_type":"field_query","field":"ref_id","value":"' + ref_ID + '","literal":true},{"jsonmodel_type":"field_query","field":"types","value":"pui","literal":true}]}}'
	aoSearch = requests.get(baseURL + AOquery, headers=headers).json()
	linked_ao_uri = aoSearch['results'][0]['uri']
	# Get and store archival objects from above search
	aoRecord = requests.get(baseURL + linked_ao_uri, headers=headers).json()
	# Find existing instances and create new ones from new digital objects
	exising_instance = aoRecord['instances'][0]
	new_instance = '{"instance_type": "digital_object", "digital_object": {"ref": "' + uri + '"}}'
	new_instance = json.loads(new_instance)
	# Merge old and new instances
	instances_new = []
	instances_new.append(exising_instance)
	instances_new.append(new_instance)
	aoRecord['instances'] = instances_new
	# Post updated archival objects
	aoPost = requests.post(baseURL + linked_ao_uri, headers=headers, data=json.dumps(aoRecord)).json()
	print aoPost
	# Save select information to new csv file
	f.writerow([title]+[digital_object_id]+[uri]+[linked_ao_uri])

# Feedback to user
print 'New .csv saved to working directory.  Go have a look!'

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
