#!/usr/bin/python3

from caproto.server import pvproperty, PVGroup
import logging, asyncio

import pyvisa
from parse import parse

from functools import partial, partialmethod

from emmi.scpi import MagicPharos

import funzel.flags as fflg

from caproto import ChannelType

logger = logging.getLogger(__name__)

class PharosIoc(PVGroup):
    main_state =         pvproperty(value=False)

    
    INTERLOCK_STATUS =   pvproperty(value = "",
                                    max_length = 40,
                                    dtype = ChannelType.STRING,
                                    doc = "Status of laser interlock")
    MAINS_STATUS =       pvproperty(value = "",
                                    max_length = 40,
                                    dtype = ChannelType.STRING,
                                    doc = "Status of main power supply")
    MAIN_KEY_STATUS =    pvproperty(value = "",
                                    max_length = 40,
                                    dtype = ChannelType.STRING,
                                    doc = "Status of main key")
    OSC_STATUS =         pvproperty(value = "",
                                    max_length = 40,
                                    dtype = ChannelType.STRING,
                                    doc = "Status of oscillator")
    RA_STATUS =          pvproperty(value = "",
                                    max_length = 40,
                                    dtype = ChannelType.STRING,
                                    doc = "Status of RA")
    PP_STATUS =          pvproperty(value = "",
                                    dtype = ChannelType.STRING,
                                    max_length = 40,
                                    doc = "Status of pulse picker")
    RA_OPERATING_STATE = pvproperty(value = "",
                                    dtype = ChannelType.STRING,
                                    max_length = 40,
                                    doc = "Indicates whether the RA is operating, i.e. the PPs are active")
    SHUTTER_STATUS =     pvproperty(value = "",
                                    max_length = 40,
                                    dtype = ChannelType.STRING,
                                    doc = "Status of laser shutter")

    
    OSC_CLEAR_ERRORS =   pvproperty(doc = "Clear all oscillator diode driver related errors")
    RA_CLEAR_ERRORS =    pvproperty(doc = "Clear all RA diode driver related errors")
    TEM_CLEAR_ERRORS =   pvproperty(doc = "Clear all timing unit related errors")

    
    # chiller control
    CHILLER_TEMP =       pvproperty(value=23.0,
                                    doc = "Temperature setpoint of the Pharos chiller (deg C)")
    CHILLER_TEMP_RBV =   pvproperty(value=0.0,
                                    doc = "Temperature readback value of the Pharos chiller (deg C)")
    CHILLER_FLOW_RBV =   pvproperty(value=0.0,
                                    doc = "Water flow readback from Pharos chiller")

    # compressor
    MOTOR_POSITION     = pvproperty(value = 43434,
                                    doc = "Motor position of compressor grating (steps)")
    MOTOR_POSITION_RBV = pvproperty(value = 0.0,
                                    doc = "Readback value of compressor position (steps)")

    # oscillator control/monitor
    OSC_ENABLE =         pvproperty(doc = "Start pump diode of Pharos oscillator")
    OSC_RUN_STARTER =    pvproperty(doc = "Run starter for modelock")
    OSC_CURRENT =        pvproperty(doc = "Pump current for Pharos oscillator")
    OSC_CURRENT_RBV =    pvproperty(value = 0.0,
                                    doc = "Readback value of oscillator pump current (mA)")
    # OSC_START =         pvproperty(doc = "Start of the Pharos oscillator")
    OSC_POWER_RBV =      pvproperty(value = 0.0,
                                    doc = "Readback and converted value of oscillator output power (mW)")
    # RA control/monitor
    RA_CURRENT =         pvproperty(value = "",
                                    doc = "Current setpoint of RA pump diodes")
    RA_CURRENT_RBV =     pvproperty(value = 0.0,
                                    doc = "Readback value of RA pump current (mA)")
    RA_ENABLE =          pvproperty(doc = "Start pump diodes of Pharos RA")
    RA_START =           pvproperty(doc = "Start Pharos RA")
    RA_POWER =           pvproperty(doc = "Power setpoint of the Pharos RA output")
    RA_POWER_RBV =       pvproperty(value = 0.0,
                                    doc = "Readback value of RA output power (mW)")
    RA_POWER_AUTO =      pvproperty(doc = "Setpoint for constant RA output power mode (mW)")

    # RA operating frequency
    RA_INT_FREQ =        pvproperty(doc = "Setpoint of the internal laser frequency (Hz)")
    RA_INT_FREQ_RBV =    pvproperty(value = 0.0,
                                    doc = "Readback value of the internal laser frequency (Hz)")
    RA_EXT_FREQ_RBV =    pvproperty(value = 0.0,
                                    doc = "Readback value of the measurement of the external laser trigger signal (Hz)")

    # laser shutter
    SHUTTER_OPEN =       pvproperty(doc = "Opening/closing of laser shutter")

    # pulse picker control
    PP_DIV =             pvproperty(value = 1,
                                    doc = "Pulse picker (Pockels cell) divider")
    PP_DIV_RBV =         pvproperty(doc = "Readbackvalue of the PP divider")
    PP_VOLT =            pvproperty(value = 2200,
                                    doc = "Setpoint of the PP voltage (HV2) in V")
    PP_VOLT_RBV =        pvproperty(value = 0.0,
                                    doc = "Readback value of the PP voltage of HV2 in V")
    PP_ENABLE =          pvproperty(value=False,
                                    doc = "'Enable'/'Open' pulse picker PP")
    
    # PP_STATUS =           pvproperty(value="n/a",
    #                                  enum_strings=["off", "on", "open"],
    #                                  #record="mbbi",
    #                                  dtype=ChannelType.ENUM)

    def __init__(self, prefix, dev=None, rman=None, motors=None):

        self.pharos = self._init_device(dev, rman)
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
        
        pharos = MagicPharos(device=dev, resource_manager=rman)
        helo = pharos.VERSION()

        try:
            assert "PHAROS UART module ver" in helo
            self.fsmc_version = tuple([int(i) for i in helo[23:].split('.')])
        except:
            raise RuntimeError(f'Cannot parse version from "{helo}"')
        
        logger.info(f'Pharos version: {self.fsmc_version}')
        
        return pharos
    

    async def status_query(self, dev):
        # Queries current status of the device
        # Returns a dictionary with flags/registers as defined in funzel.flags,
        # and their corresponding value.

        status = {}
        
        # Put the command in here (for commands which return orthogonal flags)
        ph_queries = (
            'MAINS_CTRL_STATE',
            'CHILLER_STATE',
            'MOTOR_CTRL_STATE',
            'OSC_STATE',           
            'OSC_SUPPLY_STATE',
            'CW_STATE',
            'RA_SUPPLY_STATE',
            'RA_STATE',
            'HV1_CTRL_STATE',
            'HV2_CTRL_STATE',
            'SYNC_CTRL_STATE',
            'SHUTTER_STATE',
        )
        
        # Helper for command queries;
        # The idea is that every command has the same structure of reply, i.e.:
        #
        #   >>> CMD
        #   <<< DATA_TYPE: a b c d ...
        #
        # where CMD is the command, DATA_TYPE is a self-reported Pharos data structure
        # name (reproduced in funzel.flags), and a, b, c, d, ... are numerical values.
        # Reading commands is done therefore in a loop
        #
        # The main challenge is in the meaning of the numerical values (a, b, c...):
        #
        #   - flags-query commands: numbers are binary flags OR'ed together,
        #
        #   - values-query commands: numbers "plain" values (i.e. floating point
        #     numbers representing temperatures, counts, ...).
        #
        # The read-unpack loop is the same for all kinds of commands, but unpacking
        # is different for each of them. For the "values-query" numbers, we simply
        # associate each number (value) its corresponding key from funzel.flags.
        # For "flags-query" numbers, we wrap each number in a OrthogonalFlagsMap(),
        # allowing later easy access to the individual flags.
        #
        # The 'translator' lambdas to this.
        #
        # We decide which translator lambda to use for every value, depending
        # on how the corresponding funzel.flags.DATA_TYPE[field] is defined.

        ph_values_translator = lambda vmap, value: value

        ph_flags_translator = lambda vmap, value: \
            fflg.OrthogonalFlagsMap(vmap, code=value)

        ph_enum_translator = lambda vmap, value: vmap[value]

        for ph_cmd in ph_queries:

            ph_vals = dev.branch(ph_cmd).get()

            if not isinstance(ph_vals, tuple):
                logger.error(f'Unexpected reply for "{ph_cmd}": {ph_vals}')
                #raise RuntimeError(f'Unexpected reply for "{ph_cmd}": {ph_vals}')
                continue

            try:
                ph_type = ph_vals[-1]
                ph_map = getattr(fflg, ph_type)
            except AttributeError:
                logging.debug(f"Can't unpack {ph_type}, data is: {ph_vals}")
                continue

            ph_flags = {}

            for k, v in zip(ph_map, ph_vals[:-1]):

                # At this point, ph_map is a map of the values that were returend by
                # the query, by name.
                #
                # Now picking a 'translator' is tricky:                
                #
                #   - default case is that 'value' corresponds to a single numerical
                #     value (e.g. a physical value -- pressure, voltage etc).
                #     In this case, the current ph_map[k] item does not contain
                #     anything but an explanation string.
                #
                #   - fancy case is that 'value' is a bit field / orthogonal flags.
                #     In this case, the current ph_map[k] item is a dictionary
                #     suitable as an OrthogonalFlagsMap input (i.e. { 'key': (nr, "desc"), ...}.
                #
                #   - boring case is that 'value' is an enum value -- i.e. a discrete
                #     integer number which maps to a human-readable word. In that case,
                #     ph_map[k] is a dictionary { nr: "WORD", ... }.
                #
                #   - brain-damaged case is that 'value' is split, i.e. some parts (e.g.
                #     first nibble) contains an enum value, and the rest (e.g. 2nd nibble)
                #     contains a bit field.
                #     I don't know how to handle this.
                #     But I *am* getting a gun, as this *clearly* constitutes a shooting
                #     offense.
                #

                if isinstance(ph_map[k], dict):
                    # This is the fancy and the boring case
                    translator = ph_flags_translator
                    try:
                        first = next(iter(ph_map[k].items()))
                        if type(first[0]) == int:
                            translator = ph_enum_translator
                    except StopIteration: pass
                    ph_subtype_map = ph_map[k]
                elif isinstance(ph_map[k], str):
                    # the default case
                    translator = ph_values_translator
                    ph_subtype_map = ph_map[k]
                else:
                    # The brain-damaged case.
                    # *sigh* this means that 'v' is split: some of it contains an enum,
                    # some contains fancy OR'ed flags. We handle this directly because
                    # we know the exact brainfart location in terms of PHAROS data types...
                    assert k == "TEM" and ph_type == "SYNC_CTRL"

                    # First we split the values
                    v1 = v & 0xf0
                    v2 = v & 0x0f

                    # We hi
                    ph_flags[k+"ln"] = ph_enum_translator(ph_map[k][0], v2)

                    # We pass the rest (v1) to the usual mechanics as if it were
                    # a regular flags. This will split SYNC_CTRL.TEM into two
                    # entries, one for each nibble: SYNC_CTRL.TEMln and SYNC_CTRL.TEMhn.
                    v = v1
                    translator = ph_flags_translator
                    ph_subtype_map = ph_map[k][1]
                    k += "hn"

                    # I'm sure there's a more elegant way of doing this hidden somerhere...

                    
                ph_flags[k] = translator(ph_subtype_map, v)

            status[ph_type] = ph_flags

        self.log_pharos_status(status)
        print()

        return status


    async def pharos_write(self, cmd):

        # FIXME! Need to make this async!
        
        nr = self.pharos.kdev.write(cmd)
        tmp = len(cmd) + len(self.pharos.kdev.write_termination)
        
        if nr != tmp:
            raise RuntimeError(f'Error writing {cmd}: should have '+
                               f'been {tmp} bytes, were {nr}')
        
        ret = self.pharos.kdev.read()
        if ret != "Ok":
            raise RuntimeError(f'Command "{cmd}": received "{ret}"'+
                               f' instead of "Ok"')
                               
        logger.info(f'"{cmd}": "{ret}"')
     

    async def pharos_query(self, cmd):

        # FIXME! Need to make this async!
        
        nr = self.pharos.kdev.write(cmd)
        tmp = len(cmd) + len(self.pharos.kdev.write_termination)
        
        if nr != tmp:
            raise RuntimeError(f'Error writing {cmd}: should have '+
                               f'been {tmp} bytes, were {nr}')
        
        return self.pharos.kdev.read()


    @CHILLER_TEMP.putter
    async def CHILLER_TEMP(self, inst, val):
        #v = int(val*100)
        v = val
        await self.pharos_write(f"CHILLER_SET_TEMP {v}")

    @MOTOR_POSITION.putter
    async def MOTOR_POSITION(self, inst, val):
        await self.pharos_write(f"MOTOR_CTRL_MOVE_TO_POS 0,{val}")

    @OSC_ENABLE.putter
    async def OSC_ENABLE(self, inst, val):
        if val:
            await self.pharos_write("OSC_SUPPLY_START")
        else:
            await self.pharos_write("OSC_SUPPLY_STOP")

    @OSC_RUN_STARTER.putter
    async def OSC_RUN_STARTER(self, inst, val):
        if val:
            await self.pharos_write("OSC_CTRL_RUN_STARTER")

    @RA_ENABLE.putter
    async def RA_ENABLE(self, inst, val):
        if val:
            await self.pharos_write("RA_SUPPLY_START")
        else:
            await self.pharos_write("RA_SUPPLY_STOP")
    
    @RA_START.putter
    async def RA_START(self, inst, val):
        if val:
            await self.pharos_write("SYNC_ENABLE_AMPLIFIER")
        else:
            await self.pharos_write("SYNC_DISABLE_AMPLIFIER")

            
    # @RA_POWER.putter
    # async def RA_POWER(self, inst, val):
    #     ioc = fields.parent.group
    #     print(f'output: {val}')
    #     factor = status['RA_CTRL']['PDCONV']
    #     offset = status['RA_CTRL']['PDOFFSET']
    #     power  = val 
    #     cts    = (power / factor) + offset
    #     await print(cts)
    #     await self.pharos_write(f"RA_CTRL_SET_PID_SETPOINT {cts}") 

    
    @RA_INT_FREQ.putter
    async def RA_INT_FREQ(self, inst, val):
        await self.pharos_write(f"SYNC_SET_INT_FREQUENCY {val}")

    @PP_ENABLE.putter
    async def PP_ENABLE(self, inst, val):
        if val:
            await self.pharos_write("SYNC_SET_PP_ON")
        else:
            await self.pharos_write("SYNC_SET_PP_OFF")

    @PP_DIV.putter
    async def PP_DIV(self, inst, val):
        v = val - 1
        await self.pharos_write(f"SYNC_SET_REGISTER 54,{v}")
    
    @SHUTTER_OPEN.putter
    async def SHUTTER_OPEN(self, inst, val):
        await self.pharos_write(f"SHUTTER_SET_REGISTER 4096,{val}")

    @OSC_CLEAR_ERRORS.putter
    async def OSC_CLEAR_ERRORS(self, inst, val):
        await self.pharos_write("OSC_SUPPLY_SET_CLEAR_ERRORS")

    @RA_CLEAR_ERRORS.putter
    async def RA_CLEAR_ERRORS(self, inst, val):
        await self.pharos_write("RA_SUPPLY_SET_CLEAR_ERRORS")

    @TEM_CLEAR_ERRORS.putter
    async def TEM_CLEAR_ERRORS(self, inst, val):
        await self.pharos_write("SYNC_GET_ACC_FAILURES")


    def log_pharos_status(self, status):
        for k,v in status.items():
            if isinstance(v, dict):
                for k2,v2 in v.items():
                    logger.info(f'  {k}.{k2}: {v2}')
            else:
                logger.info(f'{k}: {v}')


    @main_state.scan(period=1.0)
    async def _update(self, inst, async_lib):

        status = await self.status_query(self.pharos)

        await self.INTERLOCK_STATUS.write(status['SHUTTER_CTRL']['STATE'])

        await self.MAINS_STATUS.write(status['MAINS_CTRL']['POWER_SUPPLY'])
        await self.MAIN_KEY_STATUS.write(status['MAINS_CTRL']['KEY'])
        await self.OSC_STATUS.write(status['OSC_CTRL']['STATE'])
        await self.RA_STATUS.write(status['RA_CTRL']['STATE'])
        await self.RA_OPERATING_STATE.write(status['SYNC_CTRL']['TEMln'])
        await self.PP_STATUS.write(status['HV2_CTRL']['HV_STATE'])

        await self.CHILLER_TEMP_RBV.write(status['CHILLER_CTRL']['WATER_TEMP'])
        await self.CHILLER_FLOW_RBV.write(status['CHILLER_CTRL']['FLOW_RATE'])

        await self.MOTOR_POSITION_RBV.write(status['MOTOR_CTRL']['POSITION'])

        await self.OSC_CURRENT_RBV.write(status['OSC_SUPPLY']['CURRENT'])
        await self.RA_CURRENT_RBV.write(status['RA_SUPPLY']['CURRENT'])
        
        await self.OSC_POWER_RBV.write(status['OSC_CTRL']['PDCONV'] * (status['OSC_CTRL']['PDOUT'] - status['OSC_CTRL']['PDOFFSET'])) # f(cts-off)
        await self.RA_POWER_RBV.write(status['RA_CTRL']['PDCONV'] * (status['RA_CTRL']['PDOUT'] - status['RA_CTRL']['PDOFFSET'])) # f(cts-off)
        await self.RA_INT_FREQ_RBV.write(status['SYNC_CTRL']['INT_FREQ'])
        await self.RA_EXT_FREQ_RBV.write(status['SYNC_CTRL']['EXT_FREQ'])

        await self.PP_VOLT_RBV.write(status['HV2_CTRL']['VOLTAGE'])

        await self.SHUTTER_STATUS.write(status['SHUTTER_CTRL']['CPLD1'])
        
        await self.PP_DIV_RBV.write(await self.pharos_query("SYNC_GET_REGISTER 54"))
               
        #if status['SYNC_CTRL']['TEM'].PP_OFF:
        #    await self.ppick_state.write("off")
        #if status['SYNC_CTRL']['TEM'].PP_ON:
        #    await self.ppick_state.write("on")

        #for pv_name,pv_obj in self.pvdb:
        #    if pv.find('auto_') == -1:
        #        continue
        #    await pv_obj.write(..'SHUTTER_CTRL_STATE_OPENED')        

        # update PVs...

        # Setter PVs

        # OSC_CTRL_SET_LOCKING
        # RA_CTRL_SET_LOCKING
        # OSC_SUPPLY_GET_WORK_TIME
        # OSC_SUPPLY_SET_CLEAR_ERRORS
        # RA_SUPPLY_SET_CLEAR_ERRORS
        # MOTOR_CTRL_OPEN_SHUTTER
        # HV_PP_SET_ENABLE
        # HV_PP_SET_VOLTAGE


#def state_init():
#    ...
#    if init not done:
#        return "init"
#
#    if init done:
#        return "boo"
#
#        
#state_procedures = {
#    'init': self.state_init,
#    'boo': self.state_boo,
#}

#self.current_state = "init"
#
#async def loop():
#    
#    while True:
#        new_state = state_procedures[self.curret_state]()
#
#        ....
#        if new_state is not None:
#            self.current_state = new_state
#
#        await asyncio.sleep(0.1)
        
