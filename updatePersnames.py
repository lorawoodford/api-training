import secrets, requests, csv, json, urllib, time

startTime = time.time()

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

# authenticate to ArchivesSpace
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

viafURL = 'http://viaf.org/viaf/search?query=local.personalNames+%3D+%22'

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

# # print instructions
print 'This script queries existing person agent records in ArchivesSpace with the source of "viaf" and updates them with the proper/updated name form from VIAF (if one exists) and appends the VIAF URI to the existing records.  Please note: This is a PROOF OF CONCEPT script, and should not be used in production settings without thinking this through!'
raw_input('Press Enter to continue...')

# search AS for person agents with source "viaf"
query = '/search?page=1&filter={"query":{"jsonmodel_type":"boolean_query","op":"AND","subqueries":[{"jsonmodel_type":"field_query","field":"primary_type","value":"agent_person","literal":true},{"jsonmodel_type":"field_query","field":"source","value":"viaf","literal":true}]}}'
ASoutput = requests.get(baseURL + query, headers=headers).json()
print 'Found ' + str(len(ASoutput['results'])) + ' agents.'

# grab uri out of agent
for person in ASoutput['results']:
    uri = person['uri']
    personRecord = requests.get(baseURL + uri, headers=headers).json()
    lockVersion = str(personRecord['lock_version'])
    primary_name = personRecord['names'][0]['primary_name']
    try:
        secondary_name = personRecord['names'][0]['rest_of_name']
    except:
        secondary_name = ''
    try:
        dates = personRecord['names'][0]['dates']
    except:
        dates = ''
    searchName = primary_name + ', ' + secondary_name + ', ' + dates
    nameEdited = urllib.quote(searchName.strip())
    url = viafURL+nameEdited+'%22+and+local.sources+%3D+%22lc%22&sortKeys=holdingscount&maximumRecords=1&httpAccept=application/rdf+json'
    response = requests.get(url).content
    try:
        response = response[response.index('<recordData xsi:type="ns1:stringOrXmlFragment">')+47:response.index('</recordData>')].replace('&quot;','"')
        response = json.loads(response)
        properName = response['mainHeadings']['data'][0]['text']
        nameArray = properName.split(',')
        properPrimary = nameArray[0]
        try:
            properSecondary = nameArray[1]
        except:
            properSecondary = ''
        try:
            properDates = nameArray[2]
        except:
            properDates = ''
        viafid = response['viafID']
    except:
        label = ''
        viafid = ''
    if viafid != '':
        links = json.loads(requests.get('http://viaf.org/viaf/'+viafid+'/justlinks.json').text)
        viafid = 'http://viaf.org/viaf/'+viafid
    toPost = '{"lock_version": ' + lockVersion + ',"names": [{"primary_name":"' + properPrimary.strip() + '","rest_of_name":"' + properSecondary.strip() + '","dates":"' + properDates.strip() + '","sort_name":"' + properName + '","authorized":true, "is_display_name": true, "source": "viaf", "rules": "dacs", "name_order": "inverted", "jsonmodel_type": "name_person", "authority_id":"' + viafid + '"}]}'
    post = requests.post(baseURL + uri, headers=headers, data=toPost).json()
    print post

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
