import json, requests, secrets, time, csv, os

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
print 'This script replaces existing fauxcodes with real barcodes (linked in a separate csv file) in ArchivesSpace.'
raw_input('Press Enter to continue...')

# open csv and generate dict
reader = csv.DictReader(open('barcodes.csv'))

# GET each top_container listed in top_containers and add to records
print 'The following barcodes have been updated in ArchivesSpace:'
for row in reader:
	uri = row['uri']
	output = requests.get(baseURL + uri, headers=headers).json()
	output['barcode'] = row['real']
	post = requests.post(baseURL + uri, headers=headers, data=json.dumps(output)).json()
	print post

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete.  Total script run time: ', '%d:%02d:%02d' % (h, m, s)
