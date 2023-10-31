#!/usr/bin/python3

#from emmi.scpi import MagicHuber
import sys

from caproto.asyncio.server import run as ca_run
from caproto.asyncio.server import start_server, Context

import logging, asyncio

import caproto as ca
import pyvisa
from parse import parse

from functools import partial, partialmethod

from emmi.scpi import MagicScpi

from kronos.ioc import SRSDG645Ioc

from os import environ

class Application:
    
    def __init__(self, prefix=None, host=None, port=None, dev=None, rman="@py", args = None):
        if args is None:
            args = []

        self.prefix = prefix or environ.get('DG645_EPICS_PREFIX', "KMC3:XPP:DG645:")
        
        if dev is not None and rman is not None:
            pydev = { 'dev': dev,
                      'rman': rman }
        else:

            # if port is specified, we connect to a raw socket
            if port is not None:
                pydev = { 'dev': dev or environ.get('DG645_VISA_DEV',
                                                    f'TCPIP::{ls_host}::{ls_port}::SOCKET'),
                          'rman': rman or environ.get('DG645_VISA_RMAN', '@py') }        
            else:
                # otherwise we take the INSTR
                ls_host = host or environ.get('DG645_HOST', '172.16.58.160')
                pydev = { 'dev': dev or environ.get('DG645_VISA_DEV',
                                                    f'TCPIP::{ls_host}::INSTR'),
                          'rman': rman or environ.get('DG645_VISA_RMAN',
                                                      '@py') }
        
        logging.debug(f"Connecting to DG645 {pydev['dev']} via '{pydev['rman']}'")
        self.ioc = SRSDG645Ioc(self.prefix, **pydev)
        

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
    }[environ.get('DG645_LOGGING', 'info').lower()] )
        
    app = Application()
    
    asyncio.run(app.async_run())

if __name__ == "__main__":
    main()
