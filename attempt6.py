#!/usr/bin/env python3

import sys
import untangle

XML = 'trains.xml'

o = untangle.parse(XML)
for item in o.ActueleVertrekTijden.VertrekkendeTrein[1]:
    print(item)

