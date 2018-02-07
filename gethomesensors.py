#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# COPYRIGHT

# Dependancies
# sudo apt-get update
# sudo apt-get install build-essential
# sudo apt-get install python3-dev
# sudo pip3 install scrapy

import sys
sys.path.append('/etc/homesensors')
from secret_homesensors import *
import logging
import requests
import time
import re

import os
import argparse
from influxdb import InfluxDBClient

version = "1.0 (27-01-2018) by Paul Boot"
prog = os.path.basename(__file__)
debug = False    # Do not set to true,  will be reassigned by command line argument --debug

log = logging.getLogger(prog)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
log.info('Start logging')

def timenownano():
    return "%18.f" % (time.time() * 10 ** 9)


def setupdb(influxDbHost, influxDbPort, influxDbUser, influxDbPassword, influxDbName):

    log.info("Connect to DB: %s %i" % (influxDbHost, influxDbPort))
    client = InfluxDBClient(influxDbHost, influxDbPort, influxDbUser, influxDbPassword, influxDbName)

    #print(client.get_list_database())

    log.info("Create database: " + influxDbName)
    client.create_database(influxDbName)

    log.info("Create a retention policy")
    client.create_retention_policy('365d_policy', '365d', 365, default=True)

    log.info("Switch user: " + influxDbName)
    client.switch_user(influxDbName, influxDbPassword)

    return client


def insertindb(client, line):

    #if line insert or error
    log.info("Write points: {0}".format(line))
    try:
        client.write_points(line, time_precision='ms', protocol='line')
    except Exception as e:
        #print("InfluxDBClientError: ", e)
        log.error("InfluxDBClientError: ", e)
        return False

    return True

def getdata(URL):

    try:
        page = requests.get(URL + "/influxdb.txt")
        #print(page.json) if the page comes in JSON encoding
    except Exception as e:
        #print("Page request exeption: ", e)
        log.error("Page request exeption: ", e)
        return None

    # simple format check and ignore trailing \r
    searchObj = re.search(r'(\S+\s{1}\S+)', page.text)
    if searchObj:
        return searchObj.group(1)
    else:
        log.error("Format in getdata not valid return None")
        return None

def main():
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(prog=prog, description='Read sensors and output InfluxDB line protocol')
    parser.add_argument('--version', '-V', action='version', version='%(prog)s ' + version,
                        help='print version')
    args = parser.parse_args()

    influxDbClient = setupdb(influxDbHost, influxDbPort, influxDbUser, influxDbPassword, influxDbName)

    for URL in URLS:
        insertindb(influxDbClient, getdata(URL))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
   main()
