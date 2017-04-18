import json, requests, secrets, time

startTime = time.time()

# function to find key in nested dicts: see http://stackoverflow.com/questions/9807634/find-all-occurences-of-a-key-in-nested-python-dictionaries-and-lists
def gen_dict_extract(key, var):
    if hasattr(var,'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

# authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

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

# provide instructions
print 'This script is used to link all top_containers in a single collection (identified by the ArchivesSpace resource id number) to a single container_profile (identified by the ArchivesSpace container_profile id number).'
raw_input('Press Enter to continue...')

# have user enter resource id
resource_id = raw_input('Enter resource id: ')

# search for top_containers linked to entered resource id
endpoint = '/repositories/2/top_containers/search?page=1&aq={"filter_term":{"field":"collection_uri_u_sstr", "value":"/repositories/2/resources/' + resource_id + '", "jsonmodel_type":"field_query"}}'
output = requests.get(baseURL + endpoint, headers=headers).json()

# populate top_containers with the ids of each top_container in search results
top_containers = []
for value in gen_dict_extract('id', output):
    top_containers.append(value)

# GET each top_container listed in top_containers and add to records
records = []
for top_container in top_containers:
    output = requests.get(baseURL + top_container, headers=headers).json()
    records.append(output)

# have user enter container profile id
profile_id = raw_input('Enter container profile id: ')

# Add container profile to records and post
print 'The following records have been updated in ArchivesSpace:'
for record in records:
    record['container_profile'] = {'ref': '/container_profiles/' + profile_id + ''}
    jsonLine = json.dumps(record)
    uri = record['uri']
    post = requests.post(baseURL + uri, headers=headers, data=jsonLine).json()
    print post

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete. Total script run time: ', '%d:%02d:%02d' % (h, m, s)
