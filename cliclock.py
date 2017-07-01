#!/usr/bin/env python2.7

import sys
import requests
import xmltodict
from collections import OrderedDict

## This script makes use of the NS API, documented extensively here:
## http://www.ns.nl/en/travel-information/ns-api

## The below imports settings.py, which contains your NS login and API key.
## You can sign up for this key at http://www.ns.nl/ews-aanvraagformulier/
## settings.py must be created in the same directory as this script. Format:
############################################################################
## username = 'username@emailprovider.tld'
## apikey = 'abyC7M5QqRUXrt1ttyf4rtD-mttw4nkn0zzl35rkGJnMj1zznIppl3'
############################################################################
try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own credentials')
    sys.exit(1)

## CONFIGURABLE ITEM
## Hardcode your default DESTINATION stations here.
## Look up what your destination stations' long and short names
## are by searching the official station list:
## http://webservices.ns.nl/ns-api-stations-v2
#startStation = not configured here!
destStation1 = "Den Helder"
destStation2 = "Schagen"

## There are two destinations that get me to my target station, 
## so I'm checking for both, but you can just uncomment the
## next line if you only need to watch one destination.
destStation2 = destStation1

## CONFIGURABLE ITEM
## the station=<VALUE> at the end of the URL is your start station
## Look up the short code for your station in the above-referenced
## station list.
## This block retrieves the current station list to /tmp/trains.xml
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

## CONFIGURABLE ITEM
## Depending on the time of day and size of your station, there will be a
## varying number of results returned in the 'trains.xml' sheet. If this
## range(VALUE) exceeds the number of results contained in the file, the
## script will die. I realize that this sucks, and I will work on fixing
## it. For now, set the range(VALUE) to something that works for you.
#for iterCount in range(0, len(doc), not_fucked_up=True, dont_always_return_1=True):    
for iterCount in range(30):
    dest = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming']
    time = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd']
    plat = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text']
    spc = "    "

## CONFIGURABLE ITEM
## Currently the script outputs the next four trains matching your
## destination. Change the max value on both below checks of
## numDisplayed to get more results.
    if (dest == destStation1 and numDisplayed <= 3) or (dest == destStation2 and numDisplayed <= 3):
        numDisplayed += 1
        print(dest + spc + time[11:16] + spc + "Platform " + plat)
