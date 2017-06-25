#!/usr/local/bin/python3.6

import sys
#import urllib.request
import requests
#import xmltodict
import untangle

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

response = requests.get('http://webservices.ns.nl/ns-api-stations-v2',
        auth=requests.auth.HTTPBasicAuth(
                settings.username,
                settings.apikey), stream=True)
                
with open('stations.xml', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

obj = untangle.parse('stations.xml')

print(obj.Stations.Station.Code)

#data = xmltodict.parse(response)
    


#for i in range(500):
#    print(response.text[i], end="")

#import requests

#r = requests.get('https://my.website.com/rest/path', auth=('myusername', 'mybasicpass'))
#print(r.text)
    
#print(settings.username, settings.apikey)