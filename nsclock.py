 # -*- coding: utf-8 -*-
"""
NS clock
Copied partly on ns-notifications because I've never written Python before and have no idea what I'm doing
"""
import ns_api
import click
from pymemcache.client import Client as MemcacheClient
import datetime
import json
import __main__ as main
import logging
import sys
import os
from ns_api import *

try:
    import settings
except ImportError:
    print('Copy settings_example.py to settings.py and set the configuration to your own preferences')
    sys.exit(1)

# Only plan routes that are at maximum half an hour in the past or an hour in the future
MAX_TIME_PAST = 1800
MAX_TIME_FUTURE = 3600

# Set max time to live for a key to an hour
MEMCACHE_TTL = 3600
MEMCACHE_VERSIONCHECK_TTL = 3600 * 12
MEMCACHE_DISABLING_TTL = 3600 * 6

VERSION_NSAPI = '2.7.3'

nsapi = ns_api.NSAPI(settings.username, settings.apikey)


## Helper functions for memcache serialisation
def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    #if issubclass(value, ns_api.BaseObject):
    #    print ("instance of NS-API object")
    #    return value.to_json(), 3
    return json.dumps(value), 2

def json_deserializer(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return json.loads(value)
    raise Exception("Unknown serialization format")

mc = MemcacheClient(('127.0.0.1', 11211), serializer=json_serializer, deserializer=json_deserializer)
    
def get_stations(mc, nsapi):
    """
    Get the list of all stations, put in cache if not already there
    """
    try:
        stations = mc.get('stations')
    except KeyError:
        stations = []
        try:
            stations = nsapi.get_stations()
        except requests.exceptions.ConnectionError:
            print('Something went wrong connecting to the API')
            
        stations_json = ns_api.list_to_json(stations)
        # Cache the stations
        mc.set('stations', stations_json)
    return stations
    
stations = get_stations(mc, nsapi)
stations2 = mc.get('stations')

stations3 = Station()
bo = BaseObject()

@click.command()
#@click.option('--st2', default=UT, help='Station 2')
#@click.option('--st1', default=SGN, prompt='Station 1')
def hello():
    """Try to use ns_api in Python"""
#    for x in range(count):
#    click.echo('Welp %s!' % stations)
#    click.echo(stations2)
    click.echo('%s' % bo)
    

if __name__ == '__main__':
    hello()