#!/usr/bin/python3

from caproto.server import pvproperty, PVGroup
import logging, asyncio

from parse import parse

from functools import partial, partialmethod

from caproto import ChannelType

import diddy.dds as dds

from time import sleep

logger = logging.getLogger(__name__)

class DDS120Ioc(PVGroup):
    main_state = pvproperty(value=False)

    PHASE =      pvproperty(value = "0.0",
                            dtype = ChannelType.STRING,
                            doc = "Phase in (deg)",)
    PHASE_RBV =  pvproperty(value = "0.0",
                            dtype = ChannelType.STRING,
                            doc = "Readback value of phase in (deg)",)

    FREQ =       pvproperty(value = "20000000.0",
                            dtype = ChannelType.STRING,
                            doc = "Frequency in (Hz)",)
    FREQ_RBV =   pvproperty(value = "0.0",
                            dtype = ChannelType.STRING,
                            doc = "Readback value of frequency in (Hz)",)

    OUTPUT =     pvproperty(value = "OFF",
                            dtype = ChannelType.ENUM,
                            enum_strings = ["OFF", "ON"],
                            record = "bi",
                            doc = "Disables/enables the output of the DDS120",)
    
    def __init__(self, prefix, dev=None, rman=None, motors=None):

        self.dds120 = self._init_device(dev, rman)
        self.prefix = prefix
        
        super().__init__(prefix)


    def _init_device(self, dev=None, rman=None):

        # useful for reconnecting on errors
        if dev is None:
            dev = self.param_dev
        else:
            self.param_dev = dev
        
        if rman is None:
            rman = self.param_rman
        else:
            self.param_rman = rman
        
        dds120 = dds.DdsIo("/dev/ttyUSB2")
        serialnumber = dds120.serialNumber
        firmware = dds120.firmwareVersion
        
        try:
            assert "002971017HW2V64" in serialnumber
        except:
            raise RuntimeError(f'Cannot parse version from "{helo}"')

        config = dds120.config
        print(config)

        logger.info(f"Found device with serialnumber {serialnumber} and firmware version {firmware}")
        logger.info(f"Current DDS120 configuration: {config}.")

        return dds120
    
    
    async def status_query(self, dev):
        # Queries current status of the device
        # Returns a dictionary with flags/registers as defined in funzel.flags,
        # and their corresponding value.

        status = {}
        
        status["REF_FREQ_HZ"]  = self.dds120.frequencyHz
        status["PHASE_DEG"]    = self.dds120.phaseDeg
        status["AMPL"]         = self.dds120.amplitude
        status["OUTPUT"]       = self.dds120.outputChannel

        self.log_dds120_status(status)

        print()
        
        return status

    
    def log_dds120_status(self, status):
        for k,v in status.items():
            if isinstance(v, dict):
                for k2,v2 in v.items():
                    logger.info(f'  {k}.{k2}: {v2}')
            else:
                logger.info(f'{k}: {v}')

                
    @FREQ.putter
    async def FREQ(self, inst, val):
        print("type: ", type(val))
        self.dds120.frequencyHz = float(val)
        
    @PHASE.putter
    async def PHASE(self, inst, val):
#        val = round(float(val) / 0.025) * 0.025  # only 0.025 steps in phase_deg are possible
        val = round(float(val) * 40) / 40  # only 0.025 steps in phase_deg are possible
        #print(val)
        self.dds120.phaseDeg = float(val)
        
    @OUTPUT.putter
    async def OUTPUT(self, inst, val):
        if val == "ON":
            self.dds120.outputChannel = 1
        elif val == "OFF":
            self.dds120.outputChannel = 0

            
    @main_state.scan(period = 1.0)
    async def _update(self, inst, async_lib):

        status = await self.status_query(self.dds120)
        
        await self.PHASE_RBV.write(status["PHASE_DEG"])
        await self.FREQ_RBV.write(status["REF_FREQ_HZ"])
