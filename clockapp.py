#!/usr/bin/env python
##merged with papirus-write from https://github.com/PiSupply/PaPiRus to implement arg parsing and epaper output

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

with open('/tmp/trains.xml', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--posX', '-x', type=int, default=0, help="X position of the start of the text")
    p.add_argument('--posY', '-y', type=int, default=0, help="Y position of the start of the text")
    p.add_argument('--fsize', '-s',type=int , default=12, help="Font size to use for the text")
    p.add_argument('--rotation', '-r',type=int , default=0, help="Rotation one of 0, 90, 180, 270")
    p.add_argument('--invert', '-i', type=bool, default=False, help="Invert the display of the text")
    args = p.parse_args()
    args.content = "at some point I will figure out why this is a required variable but until then I'll just nail it up like this"

    with open('/tmp/trains.xml') as fd:
        doc = xmltodict.parse(fd.read(), xml_attribs=True)

        iterCount = 0
        numDisplayed = 0

        if args.content:
            for iterCount in range(30):
                dest = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming']
                time = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd']
                plat = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text']
                spc = "    "

                print(dest + spc + time[11:16] + spc + plat)

                if (dest == "Den Helder" and numDisplayed <= 1) or (dest == "Schagen" and numDisplayed <= 1):

                    if dest == "Den Helder":
                        dest = "HDR"
                        print("!! HIT")
                    elif dest == "Schagen":
                        dest = "SGN"
                        print("!! HIT")

                        if numDisplayed == 0:
                            disp = dest + spc + time[11:16] + spc + "Spoor " + plat

                        elif numDisplayed == 1:
                            disp2 = dest + spc + time[11:16] + spc + "Spoor " + plat

                        elif numDisplayed == 2:
                            disp3 = dest + spc + time[11:16] + spc + "Spoor " + plat

                            numDisplayed += 1
                        
#                   dest = str(dest)
                    text = PapirusTextPos(False, rotation=args.rotation)
                    text.AddText("Vertrek van de treinen\n\n", 10, 0, 13, Id="Header")
                    text.AddText(disp, 0, 20, 18, Id="opt1")

                    try:
                        disp2
                    except NameError:
                        disp2_exists = False
                    else:
                        disp2_exists = True
                        if disp2_exists == True:
                            text.AddText(disp2, 0, 40, 18, Id="opt2")

                    try:
                        disp3
                    except NameError:
                        disp3_exists = False
                    else:
                        disp3_exists = True
                        if disp3_exists == True:
                            text.AddText(disp3, 0, 40, 18, Id="opt3")

                    if numDisplayed == 0:
                        print("\nNo hits for configured stations. Assuming storing. Exception handler goes here.")
                        text = PapirusTextPos(False, rotation=args.rotation)
                        text.AddText("Vertrek van de treinen\n\n", 10, 0, 13, Id="Header")
                        text.AddText("Apparently there are no trains.", 0, 35, 18, Id="errtxt")
            text.WriteAll()

if __name__ == '__main__':
    main()

