#!/usr/bin/env python3

import sys
#import urllib.request
import requests
import xmltodict
#import untangle

try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

#def homepage(request):
#    file = urllib.request.urlopen('http://webservices.ns.nl/ns-api-stations-v2')
#    data = file.read()
#    file.close()
#
#    data = xmltodict.parse(data)
#    return render_to_response('my_template.html', {'data': data})

#def dictate(response)

#f = open('workfile.xml', 'w')

#https://stackoverflow.com/questions/40154727/how-to-use-xmltodict-to-get-items-out-of-an-xml-file
#https://pythonadventures.wordpress.com/tag/xmltodict/
#http://www.ns.nl/en/travel-information/ns-api/documentation-up-to-date-departure-times.html
#http://webservices.ns.nl/ns-api-avt?station=sgn
#http://webservices.ns.nl/ns-api-avt?station=asd
#http://webservices.ns.nl/ns-api-stations-v2
response = requests.get('http://webservices.ns.nl/ns-api-avt?station=sgn',
        auth=requests.auth.HTTPBasicAuth(
                settings.username,
                settings.apikey), stream=True)
                
with open('stations.xml', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)
        
with open('stations.xml', 'rb') as fd:
    doc = xmltodict.parse(fd.read())
    
#codes = []
#for station in doc['Stations']['Station']:
#    codes.append(station['Code'])
    
trains = []

for time in doc['ActueleVertrekTijden']['VertrekkendeTrein']:
    trains.append(time['EindBestemming'])
 
for time in doc['ActueleVertrekTijden']['VertrekkendeTrein']:   
     trains.append(time['VertrekTijd'])
     
     
for time in doc['ActueleVertrekTijden']['VertrekkendeTrein']:
    
    
    
#for time in doc['ActueleVertrekTijden']['VertrekkendeTrein']:
#    trains.append(time['VertrekSpoor'])
    
print(trains)

#obj = untangle.parse('stations.xml')

#print(obj.Stations.Station.Code)

#data = xmltodict.parse(response)
    


#for i in range(500):
#    print(response.text[i], end="")

#import requests

#r = requests.get('https://my.website.com/rest/path', auth=('myusername', 'mybasicpass'))
#print(r.text)
    
#print(settings.username, settings.apikey)