#!/usr/bin/python3

#from emmi.scpi import MagicHuber
import sys
sys.path.append('/var/home/specuser/proj/fridge/src')


from caproto.asyncio.server import run as ca_run
from caproto.asyncio.server import start_server, Context

import logging, asyncio

import caproto as ca
import pyvisa
from parse import parse

from functools import partial, partialmethod

from emmi.scpi import MagicScpi

import fridge.flags as fflg

from fridge.ioc import LakeShoreIoc

from os import environ

class Application:
    
    def __init__(self, prefix=None, host=None, port=7777, dev=None, rman="@py", args = None):
        if args is None:
            args = []

        self.prefix = prefix or environ.get('LS336_EPICS_PREFIX', "KMC3:XPP:LS336:")
        
        if dev is not None and rman is not None:
            pydev = { 'dev': dev,
                      'rman': rman }
        else:
            ls_host = host or environ.get('LS336_HOST', '172.16.58.161')
            ls_port = port or environ.get('LS336_PORT', '7777')
            pydev = { 'dev': dev or environ.get('LS336_VISA_DEV',
                                                f'TCPIP::{ls_host}::{ls_port}::SOCKET'),
                      'rman': rman or environ.get('LS336_VISA_RMAN',
                                                  '@py'),
                      #rman="tests/visa-sim-huber.yml@sim",  ## for simulations
                     }

        logging.debug(f"Connecting to LS336 {pydev['dev']} via '{pydev['rman']}'")
        self.ioc = LakeShoreIoc(self.prefix, **pydev)

    async def async_run(self):
        
        logging.info(f'Starting IOC, PV list following')
        
        for pv in self.ioc.pvdb:
            logging.info(f"  {pv}")

        await start_server(self.ioc.pvdb)
        
        
def main():

    logging.basicConfig(level={
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }[environ.get('LS336_LOGGING', 'info').lower()] )
    
    app = Application()
    
    asyncio.run(app.async_run())


if __name__ == "__main__":
    main()
