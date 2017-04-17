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

# archiveit_coll = raw_input('Enter the Archive-It collection number: ')
# Note: will have to deal with the fact that this should be able to be run for multiple AI collections.
archiveit_coll = '3181'

# search AS for archival_object's with level "Web archive"
query = '/search?page=1&filter_term[]={"primary_type":"archival_object"}&filter_term[]={"level":"Web archive"}'
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
    for crawl in crawlList:
        doid = 'https://wayback.archive-it.org' + '/' + archiveit_coll + '/' + crawl['timestamp'] + '/' + crawl['original']
        query = '/search?page=1&filter_term[]={"primary_type":"digital_object"}&q=' + doid
        existingdoID = requests.get(baseURL + query, headers=headers).json()
        if len(existingdoID['results']) != 0:
            print 'Digital object already exists.'
        else:
            doPost = {}
            doPost['digital_object_id'] = doid
            doPost['title'] = 'Web crawl of ' + crawl['original']
            doPost['dates'] = [{'expression': crawl['timestamp'], 'date_type': 'single', 'label': 'creation'}]
            doPost['file_versions'] = [{'file_uri': crawl['filename'], 'checksum': crawl['digest'], 'checksum_method': 'sha-1'}]
            doJson = json.dumps(doPost)
        if doPost != []:
            post = requests.post(baseURL + '/repositories/2/digital_objects', headers=headers, data=doJson).json()
            print post
    #print 'Posted new digital objects to ArchivesSpace.'
            for do in doPost:
                if post != []:
                    doList = []
                    doItem = {}
                    doItem['digital_object'] = {'ref': post['uri']}
                    doItem['instance_type'] = 'digital_object'
                    doList.append(doItem)
                    doListJson = json.dumps(doList)
                print doListJson


    # get aos that need to be updated
    aostoLink = requests.get(baseURL + uri, headers=headers).json()
    print aostoLink



    #         for i in post:
    #             doItem = {}
    #             doItem['digital_object'] = {'ref': post['uri']}
    #             doItem['instance_type'] = 'digital_object'
    #             doList.append(doItem)
    #             doListJson = json.dumps(doList)
    #             print doListJson
                # if doListJson != []:

                #find a way to post just the last
            # doList keeps agregating and the final array has everything for a single ao in it...
                # if doList != []:
                #     aoGet = requests.get(baseURL + uri, headers=headers).json()
                #     existingInstances = aoGet['instances']
                #     existingInstances = existingInstances + doList
                #     aoGet['instances'] = existingInstances
                # print json.dumps(aoGet)
                # aoUpdate = requests.post(baseURL + uri, headers=headers, data=json.dumps(aoGet)).json()
                # print aoUpdate
                # aoGet = []
# #
# # TO DO
# # Parse dates for ArchivesSpace record, push to AOs above
# # Add phystech stating "Archived website" to ASpace resource record
#
# # show script runtime
# elapsedTime = time.time() - startTime
# m, s = divmod(elapsedTime, 60)
# h, m = divmod(m, 60)
# print 'Post complete. Total script run time: ', '%d:%02d:%02d' % (h, m, s)
