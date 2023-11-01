#!/usr/bin/python3

from miniquant.harp import Monster
from miniquant.app import HarpManager

from emmi import app

from softioc import softioc, builder, asyncio_dispatcher
import asyncio

import sys, time
import numpy as np
import logging

from schema import SchemaError, Schema

from emmi.api.exports import ExportObjectFromDict

from math import floor

import os
import argparse


useless_harp_config = {
    'epics': {
        'harpBase': { 'exports': {}},
        'harpChannels': {
        'exports': {},
            'interfix': 'ch{}_'
        }
    },
    'harp': {
        'settings': {
            'histogramLength': 6,
        },
        'init': {
            'measurementMode': 'Histogramming',
            'referenceClock': 'Internal'
        }
    }
}    
        
        
class HarpConnector(object):
    '''
    Will connect a Harp object (HarpManager, actually) to the EPICS CA protocol.

    Exports:
      - Waveform variables for the channels (with axis scaling)
      - a variable to switch preset proviles
      - a variable for setting histogram integration time
      - a variable for controlling data acquisition
    '''
    
    def __init__(self, iocDispatch, harpMan, epxHarp, epxChns, recTypeDefaults=None):
        '''
        Parameters:
          - `iocDispatch`: the pythonSoftIOC dispatcher to use
          - `harpMan`: the Harp manager
          - `epxHarp`: EPICS export configuration for the harp object
          - `epxChns`: EPICS export configuration for the channel objects.
          - `recTypeDefaults`: Dictionary that may contain sections with
            default parameters for each record type (e.g. `{"signal": "pollPeriod": ...}`)
        
        Both `epxHarp` and `epxChns` each have a section called "exports"
        which contains emmi "Connector Records" describing which
        fiels of the respective object get exported to EPICS under which
        suffix.

        The difference is that the `epxChns` dictionary also has supplementary
        information about intermediate naming schemes (as there are several
        channels, but only one Harp).
        '''
        
        self.iocDispatch = iocDispatch
        self.harpMan = harpMan
        self.recTypeDefaults = recTypeDefaults

        # Need to store a reference to some of the objects (e.g. the channels)
        # or they'll disappear.
        self.harp = harpMan.harp
        self.harp_channels = self.harp.channels

        logging.info("Exporting Harp base properties")
        if (epxHarp.get('exports') or None):
            self.exportEpics(self.harp, epxHarp['exports'])

        for i,ch in enumerate(self.harp_channels):
            if ch.enabled and (epxChns.get('exports') or None):
                logging.info("Exporting Harp properties for channel %d" % i)                
                self.exportEpics(ch, epxChns['exports'], interfix=epxChns['interfix'].format(i))
            else:
                logging.info("Ignoring disabled Harp channel %d" % i)


    def exportEpics(self, obj, spec, interfix=''):
        #print ("Defaults:", self.recTypeDefaults)
        for rec in spec:
            logging.info("EPICS export of '%r' according to: %r" % (obj, rec))
            ExportObjectFromDict(self.iocDispatch, obj, rec,
                                 suffixMangle=lambda x: (interfix+x).upper(),
                                 recordTypeDefaults=self.recTypeDefaults)
            
            #logging.info("EPICS PV for %r.%s, type %s/%s" % \
            #             (obj, rec['name'], rec['kind'], rec['type']))


class Application(app.IocApplication):
    '''
    Application model for a Miniquant IOC. Responsiblities:
      - managing a harp (indirectly)
      - shuffling configuration profiles (indirectly)
      - shuffling EPICS PVs
      - publishing the IOC.
    '''
    
    def __init__(self, cfg=None, **params):
        '''
        Parameters:
          - `cfg`: a configuration dictionary

        Any other named parameters passed to the constructor will be updated
        into the configuration dictionary.
        '''
        super().__init__(cfg=cfg)
        self.addFlatConfig(params, prefix='default')


    def setupHarp(self, devId=None):
        '''
        Initializes / creates a Harp device
        '''
        
        self.conf.setdefault('harp', {})
        if devId is not None:
            self.conf.setdefault['harp']['device'] = devId

        self.harpMan = HarpManager(self.conf['harp']['device'])

        if self.conf['harp']['settings'].get('fromPreset'):
            harp_settings = self.harpPreset()
            logging.info("Using Harp preset '%s'" % self.conf['harp']['settings']['fromPreset'])
        else:
            harp_settings = self.conf['harp']['settings']
            logging.info("Using explicit Harp settings")

        self.harpMan.initialize(self.conf['harp']['init'])
        self.harpMan.configure(harp_settings)
        self.harpMan.logStatus()


    def harpPreset(self, preset=None):
        '''
        Returns the Harp configuration preset named `preset`. If `None` is
        specified, returns the one that is set as default in the config file
        (configuration key `harp.settings`).

        Note that `harp.settings` may either have a `.fromPreset` field which
        must contain a preset name as string, or must contain Harp settings
        directly. Either way, if called with default parameter (`preset=None`),
        this function will return the set of settings referenced by or contained
        within `harp.settings`.
        '''
        if preset is None:
            if self.conf['harp']['settings'].get('fromPreset'):
                preset = self.conf['harp']['settings']['fromPreset']
            else:
                return self.conf['harp']['settings']
        return list(filter(lambda x: x['name'] == preset, self.conf['harp']['presets']))[0]['settings']


    def setupPvRecords(self):
        '''
        Sets up EPICS PV records
        '''
        self.harpCon = HarpConnector(self.iocDispatch, self.harpMan,
                                     self.conf['epics']['harpBase'],
                                     self.conf['epics']['harpChannels'],
                                     recTypeDefaults=self.conf['epics']['defaults'])
        
    
def loadFromYaml(path):
    from yaml import load, dump
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    return load(open(path, 'r').read(), Loader=Loader)

    
def main():    
    parser = argparse.ArgumentParser(prog='miniquant-ioc', description='EPICS-IOC for the HydraHarp 400')
    
    parser.add_argument('-d', '--harp-device', action='store', default='first',
                        help='HydraHarp device ID to use')
    
    parser.add_argument('-c', '--harp-config', action='store',
                        help='Load configuraion from YAML file')
    
    parser.add_argument('-s', '--harp-settings-fromPreset', action='store',
                        help='HARP settings preset to use')
    
    parser.add_argument('-l', '--logging', action='store',
                        help='Logging level')
    
    parser.add_argument('-e', '--epics-prefix', action='store',
                        help='EPICS prefix to export to')
    
    args = parser.parse_args()
    
    loglevel = getattr(logging, (args.logging or 'INFO').upper(), None)
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=loglevel)

    if args.harp_config:
        logging.info("Config from file: %s" % args.harp_config)
        ycfg = loadFromYaml(args.harp_config)
    else:
        ycfg = useless_harp_config

    miniApp = Application(default_epics_prefix='KMC3XPP:HARP',
                          default_harp_device='first')
    miniApp.addFlatConfig({k:v for k,v in vars(args).items() if v}, prefix="epics", subsection="epics")
    miniApp.addFlatConfig({k:v for k,v in vars(args).items() if v}, prefix="harp", subsection="harp")
    miniApp.addNestedConfig(ycfg)
    miniApp.addFlatConfig(os.environ, prefix='MINIQUANT', subsection="harp")
        
    #pprint (miniApp.conf)    
    
    miniApp.setupIoc()
    miniApp.setupHarp()
    miniApp.setupPvRecords()

    from functools import partial

    miniApp.runIoc()


if __name__ == "__main__":
    main()
