#!/usr/bin/python3

from caproto.server import pvproperty, PVGroup
import logging, asyncio, time

import pyvisa
from parse import parse

from functools import partial, partialmethod

from emmi.scpi import MagicScpi

import fridge.flags as fflg

from caproto import ChannelType

logger = logging.getLogger(__name__)

from os import environ

class LakeShoreIoc(PVGroup):
    main_state =        pvproperty(value=False)
    
    krdg1_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Reading of temperature sensor 1 (sample) (K)",
                                   )
    krdg2_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Reading of temperature sensor 2 (goniometer) (K)",
                                   )
    krdg3_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Reading of temperature sensor 3 (2nd stage) (K)",
                                   )
    krdg4_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Reading of temperature sensor 4 (radiation shield) (K)",
                                   )
    
    krdg1 =             pvproperty(value = "290.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature setpoint for sensor 1 (sample) (K)",
                                   )
    krdg2 =             pvproperty(value = "290.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature setpoint for sensor 2 (goniometer) (K)",
                                   )
    krdg3 =             pvproperty(value = "280.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature setpoint for sensor 3 (2nd stage) (K)",
                                   )
    krdg4 =             pvproperty(value = "275.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature setpoint for sensor 4 (radiation shield) (K)",
                                   )
    
    # krdg1_RBV =        pvproperty(value = "0.0",
    #                            dtype = ChannelType.STRING,
    #                            doc = "Temperature setpoint for sensor 1 (sample) (K)",
    #                            )
    # krdg2_RBV =        pvproperty(value = "0.0",
    #                            dtype = ChannelType.STRING,
    #                            doc = "Temperature setpoint for sensor 2 (goniometer) (K)",
    #                            )
    # krdg3_RBV =        pvproperty(value = "0.0",
    #                            dtype = ChannelType.STRING,
    #                            doc = "Temperature setpoint for sensor 3 (2nd stage) (K)",
    #                            )
    # krdg4_RBV =        pvproperty(value = "0.0",
    #                            dtype = ChannelType.STRING,
    #                            doc = "Temperature setpoint for sensor 4 (radiation shield) (K)",
    #                            )

    TLIM1 =             pvproperty(value = "450",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit set value for sensor 1 (sample) (K)",
                                   )
    TLIM2 =             pvproperty(value = "310",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit set value for sensor 2 (goniometer) (K)",
                                   )
    TLIM3 =             pvproperty(value = "290",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit set value for sensor 3 (2nd stage) (K)",
                                   )
    TLIM4 =             pvproperty(value = "280",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit set value for sensor 4 (radiation shield) (K)",
                                   )
    TLIM1_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit readback value for sensor 1 (sample) (K)",
                                   )
    TLIM2_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit readback value for sensor 2 (goniometer) (K)",
                                   )
    TLIM3_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit readback value for sensor 3 (2nd stage) (K)",
                                   )
    TLIM4_RBV =         pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Temperature limit readback value for sensor 4 (radiation shield) (K)",
                                   )
    
    OUTMODE1 =          pvproperty(value = "1,1,0",
                                   dtype = ChannelType.STRING,
                                   doc = "Output 1 settings (sample heater) (mode, input, powerup)",
                                   )    
    OUTMODE2 =          pvproperty(value = "1,2,0",
                                   dtype = ChannelType.STRING,
                                   doc = "Output 2 settings (goniometer heater) (mode, input, powerup)",
                                   )    
    OUTMODE3 =          pvproperty(value = "5,3,0",
                                   dtype = ChannelType.STRING,
                                   doc = "Output 3 settings (warmup) (mode, input, powerup)",
                                   )    
    OUTMODE4 =          pvproperty(value = "5,4,0",
                                   dtype = ChannelType.STRING,
                                   doc = "Output 4 settings (warmup shield) (mode, input, powerup)",
                                   )
    OUTMODE1_RBV =      pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback values for output 1 (sample heater) (mode, input, powerup)",
                                   )    
    OUTMODE2_RBV =      pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback values for output 2 (goniometer heater) (mode, input, powerup)",
                                   )    
    OUTMODE3_RBV =      pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback values for output 3 (warmup) (mode, input, powerup)",
                                   )    
    OUTMODE4_RBV =      pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback values for output 4 (warmup shield) (mode, input, powerup)",
                                   )
    
    PID_SAMPLE =        pvproperty(value = "30.0,25.0,0",
                                   dtype = ChannelType.STRING,
                                   doc = "PID settings for sample heater 1")
    PID_SAMPLE_RBV =    pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback PID settings for sample heater 1")
    
    # PID_STAGE =         pvproperty(value = "50.0,20.0,0.0",
    #                             dtype = ChannelType.STRING,
    #                             doc = "PID settings for stage heater 2")
    # PID_STAGE_RBV =     pvproperty(value = "n/a",
    #                             dtype = ChannelType.STRING,
    #                             doc = "Readback PID settings for stage heater 2")
    
    CRYO_ENABLE =       pvproperty(value = "OFF",
                                   enum_strings = ["OFF", "ON"],
                                   dtype = ChannelType.ENUM,
                                   record = "bi",
                                   doc = "Disables/enables compressor of closed-cycle cryostat")    
    CRYO_STAT_RBV =     pvproperty(value = "n/a",
                                   dtype = ChannelType.STRING,
                                   doc = "Check if relay for compressor operation is turned on")
    
    HEATER_OFF =        pvproperty(value = "n/a",
                                   dtype = ChannelType.STRING,
                                   doc = "Turn off all heaters")
    HEATER_ENABLE =     pvproperty(value = "OFF",
                                   enum_strings = ["OFF", "ON"],
                                   dtype = ChannelType.ENUM,
                                   record = "bi",
                                   doc = "Turn off/on sample heaters")
    HEATER1_STAT  =     pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Status of sample heater")
    HEATER1_OUT_RBV  =  pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback value of heater 1 output.")
    HEATER2_OUT_RBV  =  pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback value of heater 1 output.")
    
    WARMUP =            pvproperty(value = "OFF",
                                   enum_strings = ["OFF", "ON"],
                                   dtype = ChannelType.ENUM,
                                   record = "bi",
                                   doc = "Turn on heaters for cryo-warmup")
    WARMUP1_OUT_RBV  =  pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback value of warm-up power supply 1 output.")
    # WARMUP2_OUT_RBV  =  pvproperty(value = "0.0",
    #                                dtype = ChannelType.STRING,
    #                                doc = "Readback value of warm-up power supply 2 output.")
    
    RAMP =              pvproperty(value = "0.0",
                                   dtype = ChannelType.STRING,
                                   doc = "Ramp for sample temperature (K/min)")
    RAMP_RBV =          pvproperty(value = "42.24",
                                   dtype = ChannelType.STRING,
                                   doc = "Readback of ramp for sample temperature (K/min)")
                      

    def __init__(self, prefix, dev=None, rman=None, motors=None):

        self.ls336 = self._init_device(dev, rman)
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
        
        ls336 = MagicScpi(device = dev, resource_manager = rman, device_conf = {"read_termination": "\r\n", "write_termination": "\r\n"})
        helo = ls336.kdev.query("*IDN?")
        

        try:
            assert "LSCI,MODEL336,LSA133P/#######," in helo
            self.ls336_version = helo[30:]
        except:
            raise RuntimeError(f'Cannot parse version from "{helo}"')
        
        logger.info(f'Lake Shore Model 336 version: {self.ls336_version}')
        
        return ls336
    

    async def ls336_write(self, cmd):

        # FIXME! Need to make this async!
        
        nr = self.ls336.kdev.write(cmd)
        tmp = len(cmd) + len(self.ls336.kdev.write_termination)
        
        if nr != tmp:
            raise RuntimeError(f'Error writing {cmd}: should have '+
                               f'been {tmp} bytes, were {nr}')

    async def ls336_query(self, cmd):

        # FIXME! Need to make this async!
        
        nr = self.ls336.kdev.write(cmd)
        tmp = len(cmd) + len(self.ls336.kdev.write_termination)
        
        if nr != tmp:
            raise RuntimeError(f'Error writing {cmd}: should have '+
                               f'been {tmp} bytes, were {nr}')
        
        return self.ls336.kdev.read()
    
    async def status_query(self, dev):
        # Queries current status of the device
        # Returns a dictionary with flags/registers as defined in funzel.flags,
        # and their corresponding value.

        status = {}
        
        # Put the command in here (for commands which return orthogonal flags)
        input_queries = (
            #"ALARM", #<off/on>,<high value>,<low value>,<deadband>,<latch enable>,<audible>,<visible>
            ## "DIOCUR", #<excitation>
            ## "FILTER", #<off/on >,<points>,<window>     
            "KRDG", #<value>
            ## "SRDG", #<value>
            "TLIMIT", #<limit>
            "HTRST", #1,2<error code> Heater error code: 0 = no error, 1 = heater open load, 2 = heater short
            "ALARMST", #A-D<input> A - D <high state>,<low state>[term]; n,n <high state> 0 = Off, 1 = On <low state> 0 = Off, 1 = On
            "RDGST", #A-D bit flag
            )

        heater_queries = (
            "HTR", #<heater value>Heater output in percent (%).
            "HTRSET", #<htr resistance>,<max current>,<max user current>,<current/power>
            "HTRST",
            "OUTMODE", #<mode>,<input>,<powerup enable>
            "PID", #<P value>,<I value>,<D value>
            "RAMP", #<off/on>,<rate value>
            "RANGE", # <range> For outputs 1 and 2: 0 = Off, 1 = Low, 2 = Medium, 3 = High; For outputs 3 and 4: 0 = Off, 1 = On
            "RELAY", #<mode>,<input alarm>,<alarm type>
            "SETP",
            "ZONE", #<upper boundary>,<P value>,<I value>,<D value>,<moutvalue>,<range>,<input>,<rate>
            "RAMPST", #1,2 <ramp status> 0 = Not ramping, 1 = Setpoint is ramping.
            "RELAYST", #1,2<status> 0 = Off, 1 = On.
            "RDGST", #A-D bit flag
            )
            
        aoutput_queries = (
            ## "ANALOG", #<input>,<units>,<high value>,<low value>,<polarity>
            "AOUT", #<output percentage> for output 3 and 4
            # "MOUT? 1",
            # "MOUT? 2",
            # "MOUT? 3",
            # "MOUT? 4", #<value>
            "OUTMODE", #<mode>,<input>,<powerup enable>
            "RANGE",
            "SETP",
            "WARMUP", #<control>,<percentage>
            )

        status_queries = (
            "OPST",
            "OPSTE",
            "OPSTR",
            )
        
        for cmd in input_queries:
            for n in ['A', 'B', 'C', 'D']:
                ret = self.ls336.kdev.query(f'{cmd}? {n}')
                status[f"{cmd}{n}"] = ret

        for cmd in heater_queries:
            for n in [1,2]:
                ret = self.ls336.kdev.query(f'{cmd}? {n}')
                status[f"{cmd}{n}"] = ret

        for cmd in aoutput_queries:
            for n in [3,4]:
                ret = self.ls336.kdev.query(f'{cmd}? {n}')
                status[f"{cmd}{n}"] = ret                
                
        for cmd in status_queries:
            ret = self.ls336.kdev.query(f'{cmd}?')
            try:
                codemap = getattr(fflg,cmd)            
                obj = fflg.code2obj(int(ret), codemap)
                #print(f"{cmd}:       {ret}", obj)                
            #except KeyError:
            #    print(f'Failed to unpack return value {ret} from map {cmd}')
            #except AttributeError:
            #    print(f'No unpacking info for command {cmd}')
            except:
                raise
        
        self.log_ls336_status(status)

        return status


    def log_ls336_status(self, status):
        '''
        '''
        if environ.get('LS336_LOG_STATUS', 'no').lower() not in ['yes', 'true', '1']:
            return

        logger.info(f' --- Status at {time.time()}:')
        for k,v in status.items():
            if isinstance(v, dict):
                for k2,v2 in v.items():
                    logger.info(f'  {k}.{k2}: {v2}')
            else:
                logger.info(f'{k}: {v}')


    @krdg1.putter
    async def krdg1(self, inst, val):
        await self.ls336_write(str(f"SETP 1, {val}"))
    @krdg2.putter
    async def krdg2(self, inst, val):
        await self.ls336_write(str(f"SETP 2, {val}"))
    @krdg3.putter
    async def krdg3(self, inst, val):
        await self.ls336_write(str(f"SETP 3, {val}"))
    @krdg4.putter
    async def krdg4(self, inst, val):
        await self.ls336_write(str(f"SETP 4, {val}"))

    @CRYO_ENABLE.putter
    async def CRYO_ENABLE(self, inst, val):
        if val == "ON":
            await self.ls336_write(f"RELAY 1,1")
        else:
            await self.ls336_write(f"RELAY 1,0")

    @HEATER_ENABLE.putter
    async def HEATER_ENABLE(self, inst, val):
        if val == "ON":
            await self.ls336_write("OUTMODE 1,1,1,0")
            await self.ls336_write("RANGE 1,3")
            await self.ls336_write("OUTMODE 2,1,2,0")
            await self.ls336_write("RANGE 2,3")
        else:
            await self.ls336_write("RANGE 1,0")
            await self.ls336_write("RANGE 2,0")
            

    @HEATER_OFF.putter
    async def HEATER_OFF(self, inst, val):
        await self.ls336_write("RANGE 1,0")
        await self.ls336_write("RANGE 2,0")
        await self.ls336_write("RANGE 3,0")
        await self.ls336_write("RANGE 4,0")
            
    @WARMUP.putter
    async def WARMUP(self, inst, val):
        if val == "ON":
            await self.ls336_write("OUTMODE 3,5,3,0")
            await self.ls336_write("RANGE 3,1")
            # await self.ls336_write("OUTMODE 4,5,4,0")
            # await self.ls336_write("RANGE 4,1")
        else:
            await self.ls336_write("RANGE 3,0")
            await self.ls336_write("RANGE 4,0")

    @PID_SAMPLE.putter
    async def PID_SAMPLE(self, inst, val):
        await self.ls336_write(f"PID 1,{val}")
    # @PID_STAGE
    # async def PID_STAGE(self, inst, val):
    #     await self.ls336_write(f"PID 2,{val}")

    @RAMP.putter
    async def RAMP(self, inst, val):
        await self.ls336_write(f"RAMP 1,1,{val}") 
  
    @TLIM1.putter
    async def TLIM1(self, inst, val):
        await self.ls336_write(f"TLIMIT 1,{val}")
    @TLIM2.putter
    async def TLIM2(self, inst, val):
        await self.ls336_write(f"TLIMIT 2,{val}")
    @TLIM3.putter
    async def TLIM3(self, inst, val):
        await self.ls336_write(f"TLIMIT 3,{val}")
    @TLIM4.putter
    async def TLIM4(self, inst, val):
        await self.ls336_write(f"TLIMIT 4,{val}")
    

    @main_state.scan(period = 1.0)
    async def _update(self, inst, async_lib):

        status = await self.status_query(self.ls336)
        
        await self.krdg1_RBV.write(status['KRDGA'])
        await self.krdg2_RBV.write(status['KRDGB'])
        await self.krdg3_RBV.write(status['KRDGC'])
        await self.krdg4_RBV.write(status['KRDGD'])
        await self.PID_SAMPLE_RBV.write(status['PID1'])
        await self.TLIM1_RBV.write(status['TLIMITA'])
        await self.TLIM2_RBV.write(status['TLIMITB'])
        await self.TLIM3_RBV.write(status['TLIMITC'])
        await self.TLIM4_RBV.write(status['TLIMITD'])
        await self.OUTMODE1_RBV.write(status['OUTMODE1'])
        await self.OUTMODE2_RBV.write(status['OUTMODE2'])
        await self.OUTMODE3_RBV.write(status['OUTMODE3'])
        await self.OUTMODE4_RBV.write(status['OUTMODE4'])
        await self.CRYO_STAT_RBV.write(status['RELAY1'])
        await self.RAMP_RBV.write(status['RAMP1'])
        await self.HEATER1_STAT.write(status['HTR1'])
        await self.HEATER1_OUT_RBV.write(status['HTR1'])
        await self.HEATER2_OUT_RBV.write(status['HTR2'])
        await self.WARMUP1_OUT_RBV.write(status['AOUT3'])
#        await self.WARMUP2_OUT_RBV.write(status['AOUT4'])
