#!/usr/bin/env python3

import sys
import requests
import xmltodict
from collections import OrderedDict

try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

response = requests.get('http://webservices.ns.nl/ns-api-avt?station=asd',
        auth=requests.auth.HTTPBasicAuth(
                settings.username,
                settings.apikey), stream=True)

with open('trains.xml', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

with open('trains.xml') as fd:
    doc = xmltodict.parse(fd.read(), xml_attribs=True)


iterCount = 0
numDisplayed = 0

for iterCount in range(15):
    dest = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming']
    time = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd']
    plat = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text']
    if (dest == u"Den Helder" and numDisplayed <= 1) or (dest == u"Schagen" and numDisplayed <= 1):
#        print("So far I have displayed ", numDisplayed)
        numDisplayed += 1
#        print("I just incremented my counter to ", numDisplayed)
        print(dest, " || ", time, " || ", "Platform ", plat)
        
        

#    print(doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['RitNummer'])

##so.....
#if doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming'] == Den Helder
#do a thing
#else
#i have no ide awhat U'm doing

