#!/usr/bin/python3

#from emmi.scpi import MagicHuber
import sys
sys.path.append('/var/home/specuser/proj/diddy/src')


from caproto.asyncio.server import run as ca_run
from caproto.asyncio.server import start_server, Context

import logging, asyncio

import caproto as ca
from parse import parse

from functools import partial, partialmethod

from diddy.ioc import DDS120Ioc


class Application:
    
    def __init__(self, prefix, args = None):
        if args is None:
            args = []

        self.prefix = prefix
        
        self.ioc = DDS120Ioc(
            self.prefix,
            dev = "/dev/ttyUSB2",
            rman = "@py",
            #rman="tests/visa-sim-huber.yml@sim",
        )

    async def async_run(self):
        
        logging.info(f'Starting IOC, PV list following')
        
        for pv in self.ioc.pvdb:
            logging.info(f"  {pv}")

        await start_server(self.ioc.pvdb)
        
        
def main():

    logging.basicConfig(level=logging.INFO)
    
    app = Application(prefix="KMC3:XPP:DDS120:")
    
    asyncio.run(app.async_run())

    print("exhub: Done")


if __name__ == "__main__":
    main()
