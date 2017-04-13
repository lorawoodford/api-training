import json, requests

endpoint = 'http://projects.propublica.org/nonprofits/api/v2/search.json?q=animal'

output = requests.get(endpoint).json()
f=open('proPublicaRecord.json', 'w')
results=(json.dump(output, f))
f.close()
