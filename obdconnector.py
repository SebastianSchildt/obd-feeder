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

import obd 
import sys


def openOBD(port, baudrate):
	print("Opening OBD port and testing connection")
	con = obd.OBD(port,baudrate=baudrate)
	#response=con.query(obd.commands.SPEED)
	response=con.query(obd.commands['SPEED'])

	if  response.is_null():
		print("Error commnunicating with OBD, check baudrate and device settings")
		sys.exit(-1)
	print("OBD connection established")
	return con


def collectData(mapping, obdcon):
    print("Collection data")
    for obdval,config in mapping.map():
        print("Querying /{}/".format(obdval))
        response=obdcon.query(obd.commands[obdval])
        if not response.is_null():
            config['value']=response.value
            print("Got {}".format(response.value))
        else:
            config['value']=None
            print("Not available")
