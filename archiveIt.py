import requests, json, secrets, time, urllib

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

# authenticate to ArchivesSpace
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
print 'This script is used to generate new digital objects within an ArchivesSpace collection for websites crawled in an Archive-It collection.'

# Find aspace resources that have subject of "Web sites"
# endpoint = '/search?page=1&filter_term[]={"subjects":"Web+sites"}'
# ASoutput = requests.get(baseURL + endpoint, headers=headers).json()

# populate resources with the ids of each resource that contains the subject "Web sites"
# resources = []
# for value in gen_dict_extract('id', ASoutput):
#     resources.append(value)

# GET each ao linked to in resources and add to aos
query = '/search?page=1&filter_term[]={"primary_type":"archival_object"}&filter_term[]={"level":"Web archive"}'
ASoutput = requests.get(baseURL + query, headers=headers).json()

#archiveit_coll = raw_input('Enter the Archive-It collection number: ')
archiveit_coll = '3181'

# search AS for url's included as the title field in an AS archival_object with level "Web archive"
urls = []
for value in gen_dict_extract('title', ASoutput):
    urls.append(value)

# search AS and store uri for AS archival_object with level "Web archive"
aos = []
for value in gen_dict_extract('uri', ASoutput):
    aos.append(value)

for url in urls:
    json.dumps(url)
    request = 'http://wayback.archive-it.org/' + archiveit_coll + '/timemap/json/' + url
    AIoutput = requests.get(request).json()

keys = AIoutput[0]
crawlList = []
for i in range (1, len (AIoutput)):
    AIlist = AIoutput[i]
    crawl = {}
    for j in range (0, len(AIlist)):
        crawl[keys[j]] = AIlist[j]
    crawlList.append(crawl)

for crawl in crawlList:
    ASpost = {}
    ASpost['digital_object_id'] = 'https://wayback.archive-it.org' + '/' + archiveit_coll + '/' + crawl['timestamp'] + '/' + crawl['original']
    ASpost['title'] = 'Web crawl of ' + crawl['original']
    ASpost['dates'] = [{'expression': crawl['timestamp'], 'date_type': 'single', 'label': 'creation'}]
    ASpost['file_versions'] = [{'file_uri': crawl['filename'], 'checksum': crawl['digest'], 'checksum_method': 'sha-1'}]
    ASpost['linked_instances'] = [{'ref': aos}]
    print ASpost
    post = requests.post(baseURL + '/repositories/2/digital_objects/', headers=headers, data=json.dumps(ASpost)).json()
    print post

# TO DO
# Parse dates for ArchivesSpace record, push to AOs above
# Add phystech stating "Archived website" to ASpace record
