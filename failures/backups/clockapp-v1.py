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

## CONFIGURABLE ITEM
## The following checks to see if EPD_SIZE is defined
## This is related to the size of your PaPiRus screen.
## This script is built for the 2.0-inch Pi Zero screen.
## Not tested on any others! GLHF.
EPD_SIZE=0.0
if os.path.exists('/etc/default/epd-fuse'):
    execfile('/etc/default/epd-fuse')
if EPD_SIZE == 0.0:
    print("Please select your screen size by running 'papirus-config'.")
    sys.exit()

## CLI 404 train :)
train1 = "   . . . . o o o o o"
train2 = "          _____      o"
train3 = " ____====  ]OO|_n_n__][."
train4 = "[__404___]_|__|________)<"
train5 = " oo   oo  'oo OOOO-| oo\\\\_"

## PaPiRus 404 train :)
train6 = "           ____"
train7 = " ___=== |OO|__||_"
train8 = " |4 0 4|~|________)"
train9 = "( )--( ) (o)--( )-\\"

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

## The below argparse code is shamelessly stolen from one of the demo
## scripts included with the PaPiRus software.
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
         
## CONFIGURABLE ITEM
## Depending on the time of day, and the size of your station, there will
## be a varying number of results returned in the 'trains.xml' file. If
## range(VALUE) exceeds the number of results contained in the file, the
## script will die. I realize that this sucks, and I will work on fixing
## it. For now, set the range(VALUE) to something that works for you.
## 30 seems to be safe for Amsterdam Centraal most of the time.
#for iterCount in range(0, len(doc), not_fucked_up=True, dont_always_return_1=True):
         if args.content:
            for iterCount in range(30):
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
#                    dest = str(dest)
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
                        text.AddText(disp3, 0, 79, 18, Id="opt4")
                        
    ## Exception handling. If we got all the way here and there was
    ## nothing to display, print something on the screen and the CLI
    ## to alert the user.
    if numDisplayed == 0:
        print("\nNo hits for configured stations. Assuming disruption. Exception handler goes here.")
	text = PapirusTextPos(False, rotation=args.rotation)
        text.AddText("Vertrek van de treinen\n\n", 10, 0, 13, Id="Header")
        ## this is the small Choo-Choo #404 from above, appearing
        ## shortly on your PaPiRus :)
        text.AddText(train6, 87, 15, 13, Id="train6")
        text.AddText(train7, 28, 27, 13, Id="train7")
        text.AddText(train8, 20, 40, 13, Id="train8")
        text.AddText(train9, 15, 53, 13, Id="train9")
#        text.AddText("Apparently there", 15, 35, 18, Id="errtxt1")
#        text.AddText("are no trains.", 25, 55, 18, Id="errtxt2")
        text.AddText("Apparently there are no trains", 8, 80, 10, Id="errtxt")
    ## And here's another Choo-Choo #404 to keep your terminal company
	print(train1)
	print(train2)
	print(train3)
	print(train4)
	print(train5 + "\n")
    
    ## Finally, the grand finale! Up until now, every text.AddText()
    ## operation was merely adding data to the buffer for the screen,
    ## not actually displaying it. text.WriteAll() dumps everything
    ## to the screen all at once, as befits an ePaper display. We
    ## only have to call this once per run of the entire script,
    # which is why it's at the end. d3rp.
    text.WriteAll()

if __name__ == '__main__':
    main()


