 # -*- coding: utf-8 -*-
"""
NS clock
Based partly on ns-notifications because I've never written Python before and have no idea what I'm doing
"""
import ns_api
import __main__ as main
import logging
import sys
import os

try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

# Only plan routes that are at maximum half an hour in the past or an hour in the future
MAX_TIME_PAST = 1800
MAX_TIME_FUTURE = 3600

VERSION_NSAPI = '2.7.3'

