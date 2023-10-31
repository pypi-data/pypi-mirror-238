#!/usr/bin/python3

from caproto.server import pvproperty, PVGroup
import logging, asyncio, time

import pyvisa
from parse import parse

from functools import partial, partialmethod

from emmi.scpi import MagicScpi

import kronos.flags as tflg

from caproto import ChannelType

logger = logging.getLogger(__name__)

from os import environ

class SRSDG645Ioc(PVGroup):
    main_state =    pvproperty(value=False)

    trig_adv =      pvproperty(value = "ON",
                               dtype = ChannelType.ENUM,
                               enum_strings = ["OFF", "ON"],
                               record = "bi",
                               doc = "Disable/enable advanced triggering mode")
    trig_adv_RBV =  pvproperty(value = "1",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of advanced triggering mode status")
    
    trig_lvl =      pvproperty(value = "1.1",
                               dtype = ChannelType.STRING,
                               doc = "Trigger level threshold in (V)")
    trig_lvl_RBV =  pvproperty(value = "1.1",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of trigger level threshold in (V)")
    
    trig_edge =     pvproperty(value = "INTERNAL",
                               dtype = ChannelType.ENUM,
                               enum_strings = ["INTERNAL", "RISING", "FALLING"],
                               record = "mbbi",
                               doc = "Trigger edge")
    trig_edge_RBV = pvproperty(value = "2",
                               dtype = ChannelType.STRING,
                               doc = "Trigger edge: 0 -- internal trigger, 1 -- rising edge, 2 -- falling edge")
                             

    div1 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel AB")
    div2 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel CD")
    div3 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel EF")
    div4 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel GH")
    div1_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel AB")
    div2_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel CD")
    div3_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel EF")
    div4_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Trigger divider for channel GH")
    
    
    dly1 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Delay of output AB (s)",)
    dly2 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Delay of output CD (s)",)
    dly3 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Delay of output EF (s)",)
    dly4 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Delay of output GH (s)",)
    dly1_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of delay of output AB (s)",)
    dly2_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of delay of output CD (s)",)
    dly3_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of delay of output EF (s)",)
    dly4_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of delay of output GH (s)",)
    
    dur1 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Duration of output AB (s)",)
    dur2 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Duration of output CD (s)",)
    dur3 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Duration of output EF (s)",)
    dur4 =          pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Duration of output GH (s)",)
    dur1_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of duration of channel AB in (s)",)
    dur2_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of duration of channel CD in (s)",)
    dur3_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of duration of channel EF in (s)",)
    dur4_RBV =      pvproperty(value = "0.0",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of duration of channel GH in (s)",)

    olvl1 =         pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output AB (V)",)
    olvl2 =         pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output CD (V)",)
    olvl3 =         pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output EF (V)",)
    olvl4 =         pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output GH (V)",)
    olvl1_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output AB (V)",)
    olvl2_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output CD (V)",)
    olvl3_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output EF (V)",)
    olvl4_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Level of output GH (V)",)
    
    opol1 =         pvproperty(value = "POS",
                               dtype = ChannelType.ENUM,
                               enum_strings = ["NEG", "POS"],
                               record = "bi",
                               doc = "Polarity of output AB",)
    opol2 =         pvproperty(value = "POS",
                               dtype = ChannelType.ENUM,
                               enum_strings = ["NEG", "POS"],
                               record = "bi",
                               doc = "Polarity of output CD",)
    opol3 =         pvproperty(value = "POS",
                               dtype = ChannelType.ENUM,
                               enum_strings = ["NEG", "POS"],
                               record = "bi",
                               doc = "Polarity of output EF",)
    opol4 =         pvproperty(value = "POS",
                               dtype = ChannelType.ENUM,
                               enum_strings = ["NEG", "POS"],
                             record = "bi",
                               doc = "Polarity of output GH",)
    opol1_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of output polarity for AB",)
    opol2_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of output polarity for CD",)
    opol3_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of output polarity for EF",)
    opol4_RBV =     pvproperty(value = "0.42",
                               dtype = ChannelType.STRING,
                               doc = "Readback value of output polarity for GH",)
    
    CLS =           pvproperty(value = "0",
                               dtype = ChannelType.STRING,
                               doc = "Clear instrument errors",)
    # CAL = pvproperty(val = "0",
    #                  dtype = ChannelType.STRING,
    #                  doc = "Runs auto calibration routine",)
    SETTINGS_SAVE = pvproperty(dtype = ChannelType.STRING,
                               doc = "Save instrument settings to location X")
    SETTINGS_LOAD = pvproperty(dtype = ChannelType.STRING,
                               doc = "Restore instrument settings from location X")
                          

    def __init__(self, prefix, dev=None, rman=None, motors=None):

        self.dg645 = self._init_device(dev, rman)
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
        
        dg645 = MagicScpi(device = dev, resource_manager = rman, device_conf = {"read_termination": "\r\n", "write_termination": "\r\n"})
        helo = dg645.kdev.query("*IDN?")

        try:
            assert "Stanford Research Systems,DG645,s/n001776,ver" in helo
            self.dg645_version = helo[45:]
        except:
            raise RuntimeError(f'Cannot parse version from "{helo}"')
        
        logger.info(f'Stanford Research Systems,DG645,s/n001776,ver{self.dg645_version}')
        
        return dg645
    

    async def dg645_write(self, cmd):

        # FIXME! Need to make this async!
        
        nr = self.dg645.kdev.write(cmd)
        tmp = len(cmd) + len(self.dg645.kdev.write_termination)
        
        if nr != tmp:
            raise RuntimeError(f'Error writing {cmd}: should have '+
                               f'been {tmp} bytes, were {nr}')

    async def dg645_query(self, cmd):

        # FIXME! Need to make this async!
        
        nr = self.dg645.kdev.write(cmd)
        tmp = len(cmd) + len(self.dg645.kdev.write_termination)
        
        if nr != tmp:
            raise RuntimeError(f'Error writing {cmd}: should have '+
                               f'been {tmp} bytes, were {nr}')
        
        return self.dg645.kdev.read()
    
    async def status_query(self, dev):
        # Queries current status of the device
        # Returns a dictionary with flags/registers as defined in funzel.flags,
        # and their corresponding value.

        status = {}
        
        # Put the command in here (for commands which return orthogonal flags)
        trigger_queries = (
            "ADVT", # advanced triggerin: 0 -- off, 1 -- on
            "TLVL", # trigger level
            "TRAT", # trigger rate (for internal trigger)
            "TSRC", # trigger source: 0 -- internal, 1 -- external rising, 2 -- external falling edge
            )

        bnc_queries = (
            "PRES", # prescale for advanced triggering
            "LAMP", # level amplitude (V)
            "LOFF", # level offset (V)
            "LPOL", # level polarity: 0 -- neg, 1 -- pos
            )
            
        channel_queries = (
            "DLAY", # delay
            )

        for cmd in trigger_queries:
            ret = self.dg645.kdev.query(f"{cmd}?")
            status[f"{cmd}"] = ret
            
        for cmd in bnc_queries:
            for b in range(5):
                ret = self.dg645.kdev.query(f"{cmd}? {b}")
                status[f"{cmd}{b}"] = ret

        for cmd in channel_queries:
            for c in range(10):
                ret = self.dg645.kdev.query(f"{cmd}? {c}")
                status[f"{cmd}{c}"] = ret

        # query standard event register and get errors back
        status["ERROR"] = self.dg645.kdev.query("*ESR?")
        status["STATUS_REGISTER"] = self.dg645.kdev.query("INSR?")

        self.log_dg645_status(status)

        return status

    def log_dg645_status(self, status):
        if environ.get('DG645_LOG_STATUS', 'no').lower() not in ['yes', 'true', '1']:
            return

        logger.info(f' --- Status at {time.time()}:')
        
        for k,v in status.items():
            if isinstance(v, dict):
                for k2,v2 in v.items():
                    logger.info(f'  {k}.{k2}: {v2}')
            else:
                logger.info(f'{k}: {v}')

    @trig_adv.putter
    async def trig_adv(self, inst, val):
        if val == "ON":
            await self.dg645_write(f'ADVT 1')
            await self.dg645_write(f'DISP 4,0')
        elif val == "OFF":
            await self.dg645_write(f'ADVT 0')
            await self.dg645_write(f'DISP 4,0')

    @trig_lvl.putter
    async def trig_lvl(self, inst, val):
        await self.dg645_write(f'TLVL {val}')
        await self.dg645_write(f'DISP 1,0')

    @trig_edge.putter
    async def trig_edge(self, inst, val):
        if val == "INTERNAL":
            await self.dg645_write('TSRC 0')
        elif val == "RISING":
            await self.dg645_write('TSRC 1')
        elif val == "FALLING":
            await self.dg645_write('TSRC 2')

    @dly1.putter
    async def dly1(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 2,0,{val}')
        await self.dg645_write(f'DISP 11,2')
    @dly2.putter
    async def dly2(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 4,0,{val}')
        await self.dg645_write(f'DISP 11,4')
    @dly3.putter
    async def dly3(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 6,0,{val}')
        await self.dg645_write(f'DISP 11,6')
    @dly4.putter
    async def dly4(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 8,0,{val}')
        await self.dg645_write(f'DISP 11,8')

    @dur1.putter
    async def dur1(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 3,0,{val}')
        await self.dg645_write(f'DISP 11,3')
    @dur2.putter
    async def dur2(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 5,0,{val}')
        await self.dg645_write(f'DISP 11,5')
    @dur3.putter
    async def dur3(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 7,0,{val}')
        await self.dg645_write(f'DISP 11,7')
    @dur4.putter
    async def dur4(self, inst, val):
        val = float(val) * 1e-9
        await self.dg645_write(f'DLAY 9,0,{val}')
        await self.dg645_write(f'DISP 11,9')

    @olvl1.putter
    async def olvl1(self, inst, val):
        await self.dg645_write(f'LAMP 1,{val}')
        await self.dg645_write(f'DISP 12,3')
    @olvl2.putter
    async def olvl2(self, inst, val):
        await self.dg645_write(f'LAMP 2,{val}')
        await self.dg645_write(f'DISP 12,5')
    @olvl3.putter
    async def olvl3(self, inst, val):
        await self.dg645_write(f'LAMP 3,{val}')
        await self.dg645_write(f'DISP 12,7')
    @olvl4.putter
    async def olvl4(self, inst, val):
        await self.dg645_write(f'LAMP 4,{val}')
        await self.dg645_write(f'DISP 12,9')

    @opol1.putter
    async def opol1(self, inst, val):
        if val == "POS":
            await self.dg645_write(f'LPOL 1,1')
            await self.dg645_write(f'DISP 13,3')
        elif val == "NEG":
            await self.dg645_write(f'LPOL 1,0')
            await self.dg645_write(f'DISP 13,3')            
    @opol2.putter
    async def opol2(self, inst, val):
        if val == "POS":
            await self.dg645_write(f'LPOL 2,1')
            await self.dg645_write(f'DISP 13,5')
        elif val == "NEG":
            await self.dg645_write(f'LPOL 2,0')
            await self.dg645_write(f'DISP 13,5')
    @opol3.putter
    async def opol3(self, inst, val):
        if val == "POS":
            await self.dg645_write(f'LPOL 3,1')
            await self.dg645_write(f'DISP 13,7')
        elif val == "NEG":
            await self.dg645_write(f'LPOL 3,0')
            await self.dg645_write(f'DISP 13,7')            
    @opol4.putter
    async def opol4(self, inst, val):
        if val == "POS":
            await self.dg645_write(f'LPOL 4,1')
            await self.dg645_write(f'DISP 13,9')
        elif val == "NEG":
            await self.dg645_write(f'LPOL 4,0')
            await self.dg645_write(f'DISP 13,9')            

    @div1.putter
    async def div1(self, inst, val):
        await self.dg645_write(f'PRES 1,{val}')
        await self.dg645_write(f'DISP 6,2')
    @div2.putter
    async def div2(self, inst, val):
        await self.dg645_write(f'PRES 2,{val}')
        await self.dg645_write(f'DISP 6,4')
    @div3.putter
    async def div3(self, inst, val):
        await self.dg645_write(f'PRES 3,{val}')
        await self.dg645_write(f'DISP 6,6')
    @div4.putter
    async def div4(self, inst, val):
        await self.dg645_write(f'PRES 4,{val}')
        await self.dg645_write(f'DISP 6,8')

    @CLS.putter
    async def CLS(self, inst, val):
        print("Clearing error state from instrument:")
        await self.dg645_write('*CLS')
    # @CAL.putter
    # async def CAL(self, inst, val):
    #     print("Clearing error state from instrument:")
    #     await self.dg645_write('*CAL?')
    @SETTINGS_SAVE.putter
    async def SETTINGS_SAVE(self, inst, val):
        pring(f"Saving instrument settings to {val}")
        await self.dg645_write(f'*SAV {val}')
    @SETTINGS_LOAD.putter
    async def SETTINGS_LOAD(self, inst, val):
        print(f"Restoring instrument settings {val}")
        await self.dg645_write(f'*RCL {val}')
        

    @main_state.scan(period = 1.0)
    async def _update(self, inst, async_lib):

        status = await self.status_query(self.dg645)

        await self.trig_adv_RBV.write(status["ADVT"])
        await self.trig_lvl_RBV.write(status["TLVL"])
        await self.trig_edge_RBV.write(status["TSRC"])
        await self.dly1_RBV.write(float(status["DLAY2"].split(',')[1]) * 1e9)
        await self.dly2_RBV.write(float(status["DLAY4"].split(',')[1]) * 1e9)
        await self.dly3_RBV.write(float(status["DLAY6"].split(',')[1]) * 1e9)
        await self.dly4_RBV.write(float(status["DLAY8"].split(',')[1]) * 1e9)

        await self.dur1_RBV.write(float(status["DLAY3"].split(',')[1]) * 1e9)
        await self.dur2_RBV.write(float(status["DLAY5"].split(',')[1]) * 1e9)
        await self.dur3_RBV.write(float(status["DLAY7"].split(',')[1]) * 1e9)
        await self.dur4_RBV.write(float(status["DLAY9"].split(',')[1]) * 1e9)
        
        await self.div1_RBV.write(status["PRES1"])
        await self.div2_RBV.write(status["PRES2"])
        await self.div3_RBV.write(status["PRES3"])
        await self.div4_RBV.write(status["PRES4"])

        await self.olvl1_RBV.write(status['LAMP1'])
        await self.olvl2_RBV.write(status['LAMP2'])
        await self.olvl3_RBV.write(status['LAMP3'])
        await self.olvl4_RBV.write(status['LAMP4'])

        await self.opol1_RBV.write(status['LPOL1'])
        await self.opol2_RBV.write(status['LPOL2'])
        await self.opol3_RBV.write(status['LPOL3'])
        await self.opol4_RBV.write(status['LPOL4'])
