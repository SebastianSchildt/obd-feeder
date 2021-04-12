#!/usr/bin/env python

########################################################################
# Copyright (c) 2020 Robert Bosch GmbH
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0
########################################################################

import configparser
import sys, os
import time

import obdconnector as obdC
import obd2vssmapper
from kuksa_viss_client import KuksaClientThread

scriptDir= os.path.dirname(os.path.realpath(__file__))

class OBD_Client():
    def __init__(self, config):
        print("Init gpsd client...")
        if "obd" not in config:
            print("obd section missing from configuration, exiting")
            sys.exit(-1)
        
        self.vssClient = KuksaClientThread(config['kuksa_val'])
        self.vssClient.start()
        self.vssClient.authorize()
        self.cfg = {}
        provider_config=config['obd']
        self.cfg['timeout'] = provider_config.get('timeout', 1)
        self.cfg['baudrate'] = provider_config.get('baudrate', 2000000) 
        self.cfg['device'] = provider_config.get('device','/dev/ttyAMA0')
        self.cfg['mapping'] = provider_config.getint('mapping', os.path.join(scriptDir, 'mapping.yml'))
        print("Configuration")
        print("Device       : {}".format(self.cfg['device']))
        print("Baudrate     : {} baud".format(self.cfg['baudrate']))
        print("Timeout      : {} s".format(self.cfg['timeout']))
        print("Mapping file : {}".format(self.cfg['mapping']))

        self.mapping=obd2vssmapper.mapper(self.cfg['mapping'])

        self.thread = threading.Thread(target=self.loop, args=())
        self.connection = obdC.openOBD(self.cfg['device'], self.cfg['baudrate'])
        self.thread.start()

    def publishData():
        print("Publish data")
        for obdval,config in mapping.map():
            
                if config['value'] is None:
                    continue
                print("Publish {}: to ".format(obdval), end='')
                for path in config['targets']:
                    self.vssclient.setValue(path, config['value'].magnitude)
                    print(path, end=' ')
                print("")

    def loop(self):
        print("obd loop started")
        while True:
            obdC.collectData(mapping, self.connection)
            self.publishData()
        #    response=connection.query(cmd)
        #    if not response.is_null():
        #        print("Speed is {}, or {} ".format(response.value,response.value.to("mph")))
        #    else:
        #        print("No data from car. Are you connected to OBD? Is your STN set to 2Mbit baudrate?")
        #    print("Have you started porting VRTE to me?\n")
            time.sleep(self.cfg['timeout'])


    def shutdown(self):
        self.running=False
        self.thread.join()
        self.vssClient.stop()


if __name__ == "__main__":
    print("kuksa.val OBD example feeder")
    config_candidates=['/config/gpsd_feeder.ini', '/etc/gpsd_feeder.ini', os.path.join(scriptDir, 'config/gpsd_feeder.ini')]
    for candidate in config_candidates:
        if os.path.isfile(candidate):
            configfile=candidate
            break
    if configfile is None:
        print("No configuration file found. Exiting")
        sys.exit(-1)
    print("read config file" + configfile)
    config = configparser.ConfigParser()
    config.read(configfile)
    
    client = OBD_Client(config)

    def terminationSignalreceived(signalNumber, frame):
        print("Received termination signal. Shutting down")
        client.shutdown()
    signal.signal(signal.SIGINT, terminationSignalreceived)
    signal.signal(signal.SIGQUIT, terminationSignalreceived)
    signal.signal(signal.SIGTERM, terminationSignalreceived)

