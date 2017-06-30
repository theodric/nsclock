#!/usr/bin/env python3

import sys
#import urllib.request
import requests
import untangle

try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

response = requests.get('http://webservices.ns.nl/ns-api-avt?station=sgn',
        auth=requests.auth.HTTPBasicAuth(
                settings.username,
                settings.apikey), stream=True)
                
with open('trains.xml', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

XML = 'trains.xml'

o = untangle.parse(XML)
for item in o.ActueleVertrekTijden.VertrekkendeTrein:
    dest = EindBestemming
    time = VertrekTijd
    plat = VertrekSpoor
    dely = VertrekVertraging
    dlym = VertrekVertragingTekst
    if dlym:
        print(time)
        print('   ', plat)
        print('   ', dely)
        print('   ', dlym)
