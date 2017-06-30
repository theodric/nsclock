#!/usr/bin/env python

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

try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

# Running as root only needed for older Raspbians without /dev/gpiomem
if not (os.path.exists('/dev/gpiomem') and os.access('/dev/gpiomem', os.R_OK | os.W_OK)):
    user = os.getuid()
    if user != 0:
        print("Please run script as root")
        sys.exit()

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    execfile('/etc/default/epd-fuse')
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()


response = requests.get('http://webservices.ns.nl/ns-api-avt?station=asd',
        auth=requests.auth.HTTPBasicAuth(
                settings.username,
                settings.apikey), stream=True)

with open('trains.xml', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

# Command line usage
# papirus-write "Some text to write"  -x  -y -fsize

def main():
    p = argparse.ArgumentParser()
    p.add_argument('content', type=str, help="Text to display")
    p.add_argument('--posX', '-x', type=int, default=0, help="X position of the start of the text")
    p.add_argument('--posY', '-y', type=int, default=0, help="Y position of the start of the text")
    p.add_argument('--fsize', '-s',type=int , default=20, help="Font size to use for the text")
    p.add_argument('--rotation', '-r',type=int , default=0, help="Rotation one of 0, 90, 180, 270")
    p.add_argument('--invert', '-i', type=bool, default=False, help="Invert the display of the text")

    args = p.parse_args()

    with open('trains.xml') as fd:
         doc = xmltodict.parse(fd.read(), xml_attribs=True)

         iterCount = 0
         numDisplayed = 0

         if args.content:
            for iterCount in range(30):
                dest = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming']
                time = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd']
                plat = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text']
            
                if (dest == u"Den Helder" and numDisplayed <= 1) or (dest == u"Schagen" and numDisplayed <= 1):
                    numDisplayed += 1
##                  print dest, " || ", time[11:16], " || ", "Platform ", plat
                    disp = dest + " || " + time[11:16] + " || ", "Platform " + plat
#                print("Writing to Papirus.......")
#                text = PapirusText(rotation=args.rotation)
#                text.AddText(args.content, args.posX, args.posY, args.fsize, invert=args.invert)
#                print("Finished!")
                    dest = str(dest)
                    text = PapirusTextPos(rotation=args.rotation)
                    print("Writing to Papirus.......")
                    text.AddText(args.content, dest, args.posX, args.posY, args.fsize, invert=args.invert)
                    print("Finished!")

if __name__ == '__main__':
    main()
