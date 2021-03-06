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


#iterCount = 1
#numDisplayed = 0

for iterCount in range(0, 8):
    print(doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming'])
    print(doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd'])
    print(doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text'])
#    print(doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['RitNummer'])
