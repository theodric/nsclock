#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://github.com/theodric/nsclock
#theodric 20170717

import os
import sys
import time
import requests
import xmltodict
import argparse
from collections import OrderedDict

from demo_opts import get_device
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT

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
#destStation2 = destStation1

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

## Define the OLED device to write to using the setup routine 
device = get_device()
msg = "a"
show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))
time.sleep(1)

## The below block reads the just-written XML file
    with open('/tmp/trains.xml') as fd:
         doc = xmltodict.parse(fd.read(), xml_attribs=True)

    iterCount = 0
    numDisplayed = 0

## Figure out how many trains are departing from your start station                                                                                                              $
## the time the script is run.                                                                                                                                                   $
    departingTrainsCount = len(doc['ActueleVertrekTijden']['VertrekkendeTrein'])                                                                                                 $
## Then use that to feed the iterator so we don`t have an                                                                                                                        $
## underrun or miss any.                                                                                                                                                         $
    if args.content:
            for iterCount in range(departingTrainsCount):
                ## I'm only grabbing the end station, departure time, and
                ## departure platform at start station to display.
                ## There are more things you can retrieve-- paw through trains.xml
                ## +read xmltodict docs to understand how to retrieve them.
                ## I found this page useful:
                ## http://omz-software.com/pythonista/docs/ios/xmltodict.html
                dest = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['EindBestemming']
                time = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekTijd']
                plat = doc['ActueleVertrekTijden']['VertrekkendeTrein'][iterCount]['VertrekSpoor']['#text']
                spc = "    "
                print(dest + spc + time[11:16] + spc + plat) ## print each row on CLI

                ## CONFIGURABLE ITEM
                ## Currently the script outputs the next four trains matching your
                ## destination. Reduce the max value on both below checks of
                ## numDisplayed to get fewer results.
                if (dest == destStation1 and numDisplayed <= 3) or (dest == destStation2 and numDisplayed <= 3):
                    ## Shortening names to 3-letter codes to fit screen.
                    ## I *may* automate and elegantize this later.
                    if dest == "Schagen":
                        dest = "SGN"
                        print("!! HIT") ## flagging matches on CLI for debug
                    elif dest == "Den Helder":
                        dest = "HLD"
                        print("!! HIT") ## flagging matches on CLI for debug
                    ## save each extracted row to its own variable because
                    ## I can't quite grasp how to do this better.
                    if numDisplayed == 0:
                                       ## chars [11:16] is where the time lives.
                                       ## the raw var contains e.g.
                                       ## 2017-07-01T21:07:00+0200
                        disp = dest + spc + time[11:16] + spc + "Spoor " + plat
                    elif numDisplayed == 1:
                        disp2 = dest + spc + time[11:16] + spc + "Spoor " + plat
                    elif numDisplayed == 2:
                        disp3 = dest + spc + time[11:16] + spc + "Spoor " + plat
                    elif numDisplayed == 3:
                        disp4 = dest + spc + time[11:16] + spc + "Spoor " + plat
                    numDisplayed += 1
                    #initialize screen buffer var "text" without displaying anything
                    text = PapirusTextPos(False, rotation=args.rotation)
                    #Append the first bit of text to the screen buffer, top centered.
                    #X position 12, Y position 0, font size 13, Id="Header"
                    #text.AddText("Text", Xpos, Xpos, fontSize, Id="freeformElementID")
                    text.AddText("Vertrek van de treinen", 12, 0, 13, Id="Header")
                    text.AddText(disp, 0, 19, 18, Id="opt1")

                    ## The next three stanzas are merely an attempt to gracefully
                    ## handle fewer than the maximum allowed number of results.
                    ## The results, if they exist, are presented roughly centered
                    ## in a stack starting from the top, as you can see from the
                    ## increasing Y values in text.AddText.
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
                        text.AddText(disp4, 0, 79, 18, Id="opt4")


#if __name__ == "__main__":
#    try:
#        main()
#    except KeyboardInterrupt:
#        pass

