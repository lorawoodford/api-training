import requests, json, secrets, time, urllib

startTime = time.time()

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
print 'This script is used to generate new digital objects within an ArchivesSpace collection for websites crawled in an Archive-It collection.  Please note: This is a "proof of concept" script, NOT completed work.  Do not use in production scenarios.'

raw_input('Press Enter to continue...')

# archiveit_coll = raw_input('Enter the Archive-It collection number: ')
archiveit_coll = '3181'

# search AS for archival_object's with level "Web archive"
query = '/search?page=1&filter={"query":{"jsonmodel_type":"boolean_query","op":"AND","subqueries":[{"jsonmodel_type":"field_query","field":"primary_type","value":"archival_object","literal":true},{"jsonmodel_type":"field_query","field":"level","value":"Web%20archive","literal":true}]}}'
ASoutput = requests.get(baseURL + query, headers=headers).json()
print 'Found ' + str(len(ASoutput['results'])) + ' archival objects with the instance type "Web archive."'

# grab needed fields out of ao
for ao in ASoutput['results']:
    url = ao['title']
    uri = ao['uri']

    # search AI and get json of crawls for url listed in AS ao's title field
    request = 'http://wayback.archive-it.org/' + archiveit_coll + '/timemap/json/' + url
    AIoutput = requests.get(request).json()
    print 'Found ' + str(len(AIoutput)-1) + ' Archive-It crawls of ' + url + '.'

    # take AI json lists and convert to python dicts
    keys = AIoutput[0]
    crawlList = []
    for i in range (1, len (AIoutput)):
        AIlist = AIoutput[i]
        crawl = {}
        for j in range (0, len(AIlist)):
            crawl[keys[j]] = AIlist[j]
        crawlList.append(crawl)

    # construct digital object json from Archive-It output and post to AS
    print 'The following digital objects have been created in ArchivesSpace:'
    newInstances = []
    for crawl in crawlList:
        doid = 'https://wayback.archive-it.org' + '/' + archiveit_coll + '/' + crawl['timestamp'] + '/' + crawl['original']
        query = '/search?page=1&filter={"query":{"jsonmodel_type":"boolean_query","op":"AND","subqueries":[{"jsonmodel_type":"field_query","field":"primary_type","value":"digital_object","literal":true},{"jsonmodel_type":"field_query","field":"digital_object_id","value":"' + doid + '","literal":true}]}}'
        existingdoID = requests.get(baseURL + query, headers=headers).json()
        doPost = {}
        if len(existingdoID['results']) != 0:
            print 'Digital object already exists.'
        else:
            doPost['digital_object_id'] = doid
            doPost['title'] = 'Web crawl of ' + crawl['original']
            doPost['dates'] = [{'expression': crawl['timestamp'], 'date_type': 'single', 'label': 'creation'}]
            doPost['file_versions'] = [{'file_uri': crawl['filename'], 'checksum': crawl['digest'], 'checksum_method': 'sha-1'}]
            doJson = json.dumps(doPost)
        if doPost != {}:
            post = requests.post(baseURL + '/repositories/2/digital_objects', headers=headers, data=doJson).json()
            print post
            doItem = {}
            doItem['digital_object'] = {'ref': post['uri']}
            doItem['instance_type'] = 'digital_object'
            newInstances.append(doItem)
    aoGet = requests.get(baseURL + uri, headers=headers).json()
    existingInstances = aoGet['instances']
    existingInstances = existingInstances + newInstances
    aoGet['instances'] = existingInstances
    aoUpdate = requests.post(baseURL + uri, headers=headers, data=json.dumps(aoGet)).json()
    print 'The following archival objects have been updated in ArchivesSpace:'
    print aoUpdate

# TO DO LATER
# Parse dates for ArchivesSpace record, push to AOs above
# Add phystech stating "Archived website" to ASpace resource record
# Add "Web sites" subject tracing to ASpace resource record
# Deal with the fact that this should be able to be run for multiple AI collections (at present limited to one declared in script)
# Improve logic for determining whether something is a duplicate

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Post complete. Total script run time: ', '%d:%02d:%02d' % (h, m, s)
