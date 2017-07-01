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

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    execfile('/etc/default/epd-fuse')
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

train1 = "   . . . . o o o o o"
train2 = "          _____      o"
train3 = " ____====  ]OO|_n_n__][."
train4 = "[__404___]_|__|________)<"
train5 = " oo   oo  'oo OOOO-| oo\\\\_"

train6 = "           ____"
train7 = " ___====   |OO|__||_"
train8 = "| 4 0 4 |  |        )"
train9 = "( )---( ) ~ ( )--( )-\\"


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
                if (dest == "qeq" and numDisplayed <= 3) or (dest == "wew   " and numDisplayed <= 3):
                    if dest == "Wormerveer":
                        dest = "WRM"
                        print("!! HIT")
                    elif dest == "Rotterdam Centraal":
                        dest = "RDC"
                        print("!! HIT")
                    if numDisplayed == 0:
                        disp = dest + spc + time[11:16] + spc + "Spoor " + plat
                    elif numDisplayed == 1:
                        disp2 = dest + spc + time[11:16] + spc + "Spoor " + plat
                    elif numDisplayed == 2:
                        disp3 = dest + spc + time[11:16] + spc + "Spoor " + plat
                    elif numDisplayed == 3:
                        disp4 = dest + spc + time[11:16] + spc + "Spoor " + plat
                    numDisplayed += 1
#                    dest = str(dest)
                    text = PapirusTextPos(False, rotation=args.rotation)
                    text.AddText("Vertrek van de treinen\n\n", 12, 0, 13, Id="Header")
                    text.AddText(disp, 0, 19, 18, Id="opt1")
                    try:
                        disp2
                    except NameError:
                        disp2_exists = False
                    else:
                        disp2_exists = True
                    if disp2_exists == True:
                        text.AddText(disp2, 0, 39, 18, Id="opt2")
                    try:
                        disp3
                    except NameError:
                        disp3_exists = False
                    else:
                        disp3_exists = True
                    if disp3_exists == True:
                        text.AddText(disp3, 0, 59, 18, Id="opt3")
                        
                    try:
                        disp4
                    except NameError:
                        disp4_exists = False
                    else:
                        disp4_exists = True
                    if disp4_exists == True:
                        text.AddText(disp3, 0, 79, 18, Id="opt4")
                        
    if numDisplayed == 0:
        print("\nNo hits for configured stations. Assuming storing. Exception handler goes here.")
	text = PapirusTextPos(False, rotation=args.rotation)
        text.AddText("Vertrek van de treinen\n\n", 10, 0, 13, Id="Header")
        text.AddText(train6, 11, 10, 13, Id="train6")
        text.AddText(train7, 1, 25, 13, Id="train7")
        text.AddText(train8, 0, 40, 13, Id="train8")
        text.AddText(train9, 0, 55, 13, Id="train9")
#        text.AddText("Apparently there", 15, 35, 18, Id="errtxt1")
#        text.AddText("are no trains.", 25, 55, 18, Id="errtxt2")
        text.AddText("Apparently there are no trains", 15, 80, 12, Id="errtxt")
        
#assbag git
    text.WriteAll()

if __name__ == '__main__':
    main()


