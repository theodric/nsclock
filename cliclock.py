#!/usr/bin/env python2.7

import sys
import requests
import xmltodict
from collections import OrderedDict

## This script makes use of the NS API, documented extensively here:
## http://www.ns.nl/en/travel-information/ns-api

## Look up what 

## Hardcode your default stations here.
station1 = "Den Helder"
station2 = "Schagen"

## There are two destinations that get me
## to my target station, so I'm checking for two, but you can just uncomment
## the next line if you only need one.
# station2 = station1


try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

response = requests.get('http://webservices.ns.nl/ns-api-avt?station=asd',
        auth=requests.auth.HTTPBasicAuth(
                settings.username,
                settings.apikey), stream=True)

with open('/tmp/trains.xml', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

with open('/tmp/trains.xml') as fd:
    doc = xmltodict.parse(fd.read(), xml_attribs=True)

iterCount = 0
numDisplayed = 0

#for iterCount in range(0, len(doc), not_fucked_up=True, dont_always_return_1=True):
for iterCount in range(30):
    dest = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming']
    time = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd']
    plat = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text']

    if (dest == str(station1) and numDisplayed <= 1) or (dest == (station2) and numDisplayed <= 1):
        numDisplayed += 1
        print(dest, " || ", time[11:16], " || ", "Platform ", plat)
