#!/usr/bin/env python2.7

import os
import sys
import time
import requests
import xmltodict
import argparse
from collections import OrderedDict
from papirus import PapirusText
from papirus import PapirusTextPos
from papirus import Papirus

rot = 0

# The epaper screen object.
# Optional rotation argument: rot = 0, 90, 180 or 270
screen = Papirus()

# Write a bitmap to the epaper screen
#screen.display('./path/to/bmp/image')

# Perform a full update to the screen (slower)
screen.update()

# Update only the changed pixels (faster)
#screen.partial_update()

# Disable automatic use of LM75B temperature sensor
screen.use_lm75b = False

# Change screen size
# SCREEN SIZES 1_44INCH | 1_9INCH | 2_0INCH | 2_6INCH | 2_7INCH
#screen.set_size(papirus.2_0INCH)

try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

p = argparse.ArgumentParser()
p.add_argument('content', type=str, help="Text to display")
p.add_argument('--posX', '-x', type=int, default=0, help="X position of the start of the text")
p.add_argument('--posY', '-y', type=int, default=0, help="Y position of the start of the text")
p.add_argument('--fsize', '-s',type=int , default=20, help="Font size to use for the text")
p.add_argument('--rotation', '-r',type=int , default=0, help="Rotation one of 0, 90, 180, 270")
p.add_argument('--invert', '-i', type=bool, default=False, help="Invert the display of the text")

args = p.parse_args()

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

#for iterCount in range(0, len(doc), not_fucked_up=True, dont_always_return_1=True):
for iterCount in range(30):
    dest = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming']
    time = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd']
    plat = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text']

    if (dest == u"Den Helder" and numDisplayed <= 1) or (dest == u"Schagen" and numDisplayed <= 1):
        numDisplayed += 1
#        print dest, " || ", time[11:16], " || ", "Platform ", plat
        disp = dest + " || " + time[11:16] + " || ", "Platform " + plat
        papi = PapirusText(rotation=args.rotation)
        papi.AddText(disp, args.posX, args.posY, args.fsize, invert=args.invert)
