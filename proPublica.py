import json, requests, time

startTime = time.time()

# print instructions
print 'This script creates and saves a separate file called "proPublicaRecord.json" containing the results of a proPublica search for "animal.""'
raw_input('Press Enter to continue...')

endpoint = 'http://projects.propublica.org/nonprofits/api/v2/search.json?q=animal'

output = requests.get(endpoint).json()
f=open('proPublicaRecord.json', 'w')
results=(json.dump(output, f))
f.close()

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
