import json, requests, secrets, time

startTime = time.time()

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

#authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

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

# print instructions
print 'This script will add the container_profiles included in a separate json file to ArchivesSpace.'
raw_input('Press Enter to continue...')

# post container_profiles
print 'The following container profiles have been added to ArchivesSpace:'
jsonfile = open('containerProfiles.json')
jsonfile = json.load(jsonfile)
for line in jsonfile:
	toPost = json.dumps(line)
	post = requests.post(baseURL + '/container_profiles', headers=headers, data=toPost).json()
	print post

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
