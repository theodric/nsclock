#!/usr/bin/env python3

import sys
import xmltodict
from collections import OrderedDict


with open('trains.xml') as fd:
    doc = xmltodict.parse(fd.read(), xml_attribs=True)

iterCount = 0
numDisplayed = 0

##this doesn't work
#print(doc['ActueleVertrekTijden']['VertrekkendeTrein'][int(iterCount)]['RouteTekst'])

##this does.
doc['ActueleVertrekTijden']['VertrekkendeTrein'][0]['RouteTekst']

#root_elements = doc['VertrekkendeTrein'] if type(doc) == OrderedDict else [doc["VertrekkendeTrein"]]
#for element in root_elements:
#    print(element[0]["RitNummer"])

#num_displayed = 0
#index = 0
#while num_displayed <= 2:
#check trains.train.dest[index]
#if Nijmegen || Maastrict,
#   index++
#   rerun func
#if !Nijmegen || !Maastrict,
#   display_train()
#   index++
#   num_displayed++
#
#def display_train()
#   print(trains.train.[index].dest)
#   print(trains.train.[index].time)
#   print(trains.train.[index].platform)
#   print(trains.train.[index].delay)
#   print(trains.train.[index].delay_mins)