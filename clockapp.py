#!/usr/bin/env python

import os
import sys
import time
import requests
import xmltodict
import argparse
from collections import OrderedDict
## The below library is not available via pip.
## Retrieve and install as instructed from
## https://github.com/PiSupply/PaPiRus
from papirus import PapirusText
from papirus import PapirusTextPos
from papirus import Papirus

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

# Check EPD_SIZE is defined
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    execfile('/etc/default/epd-fuse')
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

## CLI 404 train
train1 = "   . . . . o o o o o"
train2 = "          _____      o"
train3 = " ____====  ]OO|_n_n__][."
train4 = "[__404___]_|__|________)<"
train5 = " oo   oo  'oo OOOO-| oo\\\\_"

## PaPiRus 404 train
train6 = "           ____"
train7 = " ___=== |OO|__||_"
train8 = " |4 0 4|~|________)"
train9 = "( )--( ) (o)--( )-\\"


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
    args.content = " "

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
        text.AddText(train6, 87, 15, 13, Id="train6")
        text.AddText(train7, 28, 27, 13, Id="train7")
        text.AddText(train8, 20, 40, 13, Id="train8")
        text.AddText(train9, 15, 53, 13, Id="train9")
#        text.AddText("Apparently there", 15, 35, 18, Id="errtxt1")
#        text.AddText("are no trains.", 25, 55, 18, Id="errtxt2")
        text.AddText("Apparently there are no trains", 8, 80, 10, Id="errtxt")
	print(train1)
	print(train2)
	print(train3)
	print(train4)
	print(train5 + "\n")
    text.WriteAll()

if __name__ == '__main__':
    main()


