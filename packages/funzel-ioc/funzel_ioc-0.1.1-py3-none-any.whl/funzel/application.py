#!/usr/bin/python3

import logging, asyncio
import pyvisa

import funzel.flags as fflg
from funzel.ioc import PharosIoc

from caproto.asyncio.server import start_server

class Application:
    
    def __init__(self, prefix, args=None):
        if args is None:
            args = []

        self.prefix = prefix
        
        self.ioc = PharosIoc(
            self.prefix,
            #dev="TCPIP::192.168.136.217::1234::SOCKET",
            #dev="TCPIP::10.0.0.178::1234::SOCKET",
            dev="ASRL/dev/funzel::INSTR",
            rman="@py",
            #dev="ASRL1::INSTR",
            #rman="tests/visa-sim-huber.yml@sim",
        )

    async def async_run(self):
        
        logging.info(f'Starting IOC, PV list following')
        
        for pv in self.ioc.pvdb:
            logging.info(f"  {pv}")

        await start_server(self.ioc.pvdb)
        
        
def main():

    logging.basicConfig(level=logging.INFO)
    
    app = Application(prefix="KMC3:XPP:PHAROS:")
    
    asyncio.run(app.async_run())

    print("exhub: Done")


if __name__ == "__main__":
    main()
