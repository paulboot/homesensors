#!/usr/bin/python
# -*- coding: utf-8 -*-
#

#List of sensors
URLS = [ "http://se01.bocuse.nl", "http://se02.bocuse.nl" ]

#List of MAC addresses (not used now)
#se01 30:AE:A4:2C:A8:40
#se02 30:AE:A4:05:F2:34

#Influx Settings
influxDbHost = "localhost"
influxDbPort = 8086
influxDbUser = ""
influxDbPassword = ""
influxDbName = "homesensors"
