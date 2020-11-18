#!/usr/bin/python3

########################################################################
# Copyright (c) 2020 Robert Bosch GmbH
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0
########################################################################




import argparse
import sys
import time

import obdconnector as obdC
import obd2vssmapper
import websocketconnector
import yaml

cfg={}
cfg['TIMEOUT']=60



def getConfig():
	global cfg
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--timeout",  default=1, help="Timeout between read cylces", type=int)
	parser.add_argument("-b", "--baudrate", default=2000000, help="Baudrate to ELM", type=int)
	parser.add_argument("-d", "--device",   default="/dev/ttyAMA0", help="Serial port for ELM connection", type=str)
	parser.add_argument("-s", "--server",   default="ws://localhost:8090", help="VSS server", type=str)
	parser.add_argument("-j", "--jwt",   default="jwt.token", help="JWT security token", type=str)
	parser.add_argument("--mapping",   default="mapping.yml", help="VSS mapping", type=str)
	
	args=parser.parse_args()
	cfg['TIMEOUT']=args.timeout
	cfg['baudrate']=args.baudrate
	cfg['device']=args.device
	cfg['mapping']=args.mapping
	cfg['jwtfile']=args.jwt
	cfg['server']=args.server

               


def publishData(vss):
	print("Publish data")
	for obdval,config in mapping.map():
		
		if config['value'] is None:
			continue
		print("Publish {}: to ".format(obdval), end='')
		for path in config['targets']:
			vss.push(path, config['value'].magnitude)
			print(path, end=' ')
		print("")
        


print("kuksa.val OBD example feeder")
getConfig()
print("Configuration")
print("Device       : {}".format(cfg['device']))
print("Baudrate     : {} baud".format(cfg['baudrate']))
print("Timeout      : {} s".format(cfg['TIMEOUT']))
print("Mapping file : {}".format(cfg['mapping']))
print("VSS server   : {}".format(cfg['server']))
print("JWT token    : {}".format(cfg['jwtfile']))





with open(cfg['jwtfile'],'r') as f:
	token=f.read()

mapping=obd2vssmapper.mapper("mapping.yml")
vss=websocketconnector.vssclient(cfg['server'],token)

connection = obdC.openOBD(cfg['device'],cfg['baudrate'])


while True:
	obdC.collectData(mapping,connection)
	publishData(vss)
#	response=connection.query(cmd)
#	if not response.is_null():
#		print("Speed is {}, or {} ".format(response.value,response.value.to("mph")))
#	else:
#		print("No data from car. Are you connected to OBD? Is your STN set to 2Mbit baudrate?")
#	print("Have you started porting VRTE to me?\n")
	time.sleep(cfg['TIMEOUT'])
