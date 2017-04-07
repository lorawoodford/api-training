import requests
import csv
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import json
import urllib

baseURL = 'http://viaf.org/viaf/search/viaf?query=local.personalNames+%3D+%22'
f=csv.writer(open('viafPeopleResults.csv', 'wb'))
f.writerow(['search']+['result']+['ratio']+['partialRatio']+['tokenSort']+['tokenSet']+['avg']+['viaf']+['lc']+['isni'])
with open('people.txt') as txt:
    for row in txt:
        rowEdited = urllib.quote(row.decode('utf-8-sig').encode('utf-8').strip())
        url = baseURL+rowEdited+'%22+and+local.sources+%3D+%22lc%22&sortKeys=holdingscount&httpAccept=application/rdf+xml'
        response = requests.get(url).content
        record = BeautifulSoup(response, "lxml").find('html').find('body').find('searchretrieveresponse')
        try:
            label = record.find('records').find('record').find( 'recorddata').find('ns2:viafcluster').find('ns2:mainheadings').find('ns2:data').find('ns2:text').text.encode('utf-8')
            viafid = record.find('records').find('record').find( 'recorddata').find('ns2:viafcluster').find('ns2:viafid').text.encode('utf-8')
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
        f=csv.writer(open('viafPeopleResults.csv', 'a'))
        f.writerow([row.strip()]+[label]+[ratio]+[partialRatio]+[tokenSort]+[tokenSet]+[avg]+[viafid]+[lc]+[isni])
