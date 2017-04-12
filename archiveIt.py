import requests, json, secrets, time

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
#url = raw_input('Enter the url you wish to search: ')
urls = []
for value in gen_dict_extract('title', ASoutput):
    urls.append(value)

for url in urls:
    json.dumps(url)
    request = 'http://wayback.archive-it.org/' + archiveit_coll + '/timemap/json/' + url
    AIoutput = requests.get(request).json()

for i in range (1, len (AIoutput)):
    keys = AIoutput[0]
    values = AIoutput[i]
    merged = zip(keys, values)
    print json.dumps(merged)

# Parse dates for ArchivesSpace record
# Add phystech stating "Archived website" to ASpace record
# Checksum in the dao?
# In dev subjects/202 is for "Web sites"

# [[u'urlkey', u'timestamp', u'original', u'mimetype', u'statuscode', u'digest', u'redirect', u'robotflags', u'length', u'offset', u'filename'], [u'edu,jhu,library)/', u'20150625180455', u'http://www.library.jhu.edu/', u'text/html', u'200', u'AZ2TUETPDGYB4IJDOF2KRX7JCIYUYL3U', u'-', u'-', u'10225', u'28636', u'ARCHIVEIT-3181-CRAWL_SELECTED_SEEDS-JOB161970-20150625180453753-00000.warc.gz'],
