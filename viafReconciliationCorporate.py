import requests
import csv
from fuzzywuzzy import fuzz
import json
import urllib

baseURL = 'http://viaf.org/viaf/search/viaf?query=local.corporateNames+%3D+%22'
f=csv.writer(open('viafCorporateResults.csv', 'wb'))
f.writerow(['search']+['result']+['viaf']+['lc']+['isni']+['ratio']+['partialRatio']+['tokenSort']+['tokenSet']+['avg'])
with open('organizations.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = str(row['name'])
        rowEdited = urllib.quote(name.strip())
        url = baseURL+rowEdited+'%22+and+local.sources+%3D+%22lc%22&sortKeys=holdingscount&maximumRecords=1&httpAccept=application/rdf+json'
        response = requests.get(url).content
        try:
            response = response[response.index('<recordData xsi:type="ns1:stringOrXmlFragment">')+47:response.index('</recordData>')].replace('&quot;','"')
            response = json.loads(response)
            label = response['mainHeadings']['data'][0]['text']
            viafid = response['viafID']
        except:
            label = ''
            viafid = ''
        ratio = fuzz.ratio(row, label)
        partialRatio = fuzz.partial_ratio(row, label)
        tokenSort = fuzz.token_sort_ratio(row, label)
        tokenSet = fuzz.token_set_ratio(row, label)
        avg = (ratio+partialRatio+tokenSort+tokenSet)/4

        if viafid != '':
            links = json.loads(requests.get('http://viaf.org/viaf/'+viafid+'/justlinks.json').text)
            viafid = 'http://viaf.org/viaf/'+viafid
            try:
                lc = 'http://id.loc.gov/authorities/names/'+json.dumps(links['LC'][0]).replace('"','')
            except:
                lc = ''
            try:
                isni = 'http://isni.org/isni/'+json.dumps(links['ISNI'][0]).replace('"','')
            except:
                isni = ''
        else:
            lc = ''
            isni = ''
        f.writerow([name.strip()]+[label]+[viafid]+[lc]+[isni]+[ratio]+[partialRatio]+[tokenSort]+[tokenSet]+[avg])
