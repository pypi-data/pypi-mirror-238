#!/usr/bin/python3

import logging

class OrthogonalFlagsMap:
    '''
    This is a mapping helper for various flags-to-strings facilities
    (Harp warnings, Harp flags, ...) encoded as a i.e. a bitwise field
    of *several* items. You can iterate through the warnings to reach
    all of them:
    ```
       >>> warn = OrthogonalFlagsMap(HarpWarnings, 0x441)
       >>> [ warn.text(w) for w in warn ]
       [ 'Sync rate is zero', 'Input rate is too high', 'Time span is too small' ]
       >>> warn.INPT_RATE_ZERO
       True
       >>> warn.INPT_RATE_TOO_HIGH
       False
    ```
    '''
    
    def __init__(self, flagsMap, code=None):
        '''
        Initializes the mapper. Parameters:
          - `code`: This is a bitwise field of flags that this instance represents.
          - `flagsMap`: This is a dictionary which maps single string keys to
            `(flagMask, flagDescription)` tuples. The string key part
            is a non-changeable string that describes the flags for all eternity,
            and which the user (or other program layers) can use to access the flag.
            `flagDescription` is a human-readable string which can change, e.g.
            by translation or a more precise specification, and `flagMask` is a bit
            mask that indicates whether the flag is set or not.
        '''
        self.flagsMap = flagsMap
        
        if not isinstance (flagsMap, dict):
            t = type(flagsMap)
            raise RuntimeError(f'Flags map needs to be a dictionary, received'+
                               f' {t}: {flagsMap}')

        if len(flagsMap) == 0:
            logging.debug(f'Flags map is empty: f{flagsMap}')
        else:
            first = next(iter(flagsMap))
            if not isinstance(flagsMap[first], tuple) or \
               2 != len(flagsMap[first]):
                raise RuntimeError(f'Flags map value needs to be a (key, description)'+
                                   f' tuple; got {flagsMap[first]} instead')
            
        if code is not None:
            self.recode(code)
    
    def recode(self, code):
        '''
        Resets the code to `code` and returns a reference to self.
        This is to update the active/inactive flags list to the
        ones encoded in `code` without altering the identity of the
        object.
        '''
        self.code = code
        return self

    def __str__(self):
        return str([f for f in self.keys()])

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, key):
        return (self.code & self.flagsMap[key][0]) != 0

    def __iter__(self):
        ''' Iterate through all warnings encoded in `self.code`. '''
        for k,v in self.flagsMap.items():
            if (v[0] & self.code) != 0:
                yield k

    def keys(self):
        '''
        Mimic a bit of a `dict`-like interface: return all the HHLIB API
        warning keys that are encoded in `self.code`.
        '''
        for k in self:
            yield k

    def items(self):
        '''
        Mimic a bit more a `dict`-like interface: return all the HHLIB API
        warning keys that are encoded in `self.code`.
        '''
        for k,v in self.flagsMap.items():
            if (v[0] & self.code):
                yield (k, v[1])
    
    def __getitem__(self, flag):
        ''' Another way of reading a flag '''
        return self.__getattr__(flag)

    def text(self, flag):
        '''
        Returns the description text.
        '''
        return self.flagsMap.get(flag, None)[1]

    def mask(self, flag):
        '''
        Returns the numerical mask value.
        '''
        return self.flagsMap.get(flag, None)[0]

    def __len__(self):
        return len([i for i in self.items()])

#
# Flag map names must match the data type reported by PHAROS!
# The first round of keys can be chosen freely, but the number
# relates to the number of parameters reported by Pharos.
#


CHILLER_CTRL = {
    'WATER_TEMP':   "Water temperature",
    'SET_POINT':    "Current setpoint",
    'AMBIENT_TEMP': "Ambient temperature",
    'FLOW_RATE':    "Flow rate",
    'WATER_PRESS':  "Water pressure",
}


MAINS_CTRL = {
    'KEY': {
        'ON':    (0x01, "Power on"),
        'LASER': (0x02, "Laser on"),
    },

    'AC_FAIL': {
        'FAIL': (0x01, "AC voltage failure"),
        'WARN': (0x02, "AC voltage warning"),
    },

    'TEMP': "Temperature",

    'ACCESS': {
        # if no bit is set, that's "user access"
        'TECH_ACCESS': (0x01, "Technician access level"),
        'MANF_ACCESS': (0x02, "Manufacturer access level"),
    },

    'INTERLCK': {
        # 'LEVEL1_STAT': (0x01, "Interlock level 1 is active"),
        'LEVEL2_STAT': (0x01, "Interlock level 2 is active"),
        'LEVEL1_FLAG': (0x02, "Interlock level 1 was activated"),
        'LEVEL2_FLAG': (0x04, "Interlock level 2 was activated"),
        'SAFETY':      (0x08, "Safety button was activated"),
    },

    'POWER_SUPPLY': {
        'PS_ON':  (0x01, "Power supply is ON"),
        'REMOTE': (0x02, "Control from remote panel is blocked"),
        'USB':    (0x04, "Control from USB is blocked"),
        'AC':     (0x08, "AC protection blocked"),
        'OFF':    (0x10, "Key is in position Power OFF"),
        'ON':     (0x20, "Key is in position Power ON"),
        'LASER':  (0x40, "Key is in position Laser ON"),
        'WDOG':   (0x80, "Watchdog was restarted"),
    },

    'CURRENT': "Current measured on 24 V line (mA)",
    'VOLTAGE': "Voltage measured on 24 V line (V)",

}

MOTOR_CTRL = {
    'STATE': {
        'FUNCTIONAL':  (0x01, "Is functional"),
        'MOVING':      (0x02, "Is moving"),
        'LEND_SWITCH': (0x04, "Left end switch active"),
        'REND_SWITCH': (0x08, "Right end switch active"),
        'SHUTTER':     (0x10, "Shutter opened"),
        'WARNING':     (0x20, "Warning light on"),
    },
    
    'CURRENT':     "Current (mA)",
    'POSITION':    "Position (steps)",
    'HUMIDITY':    "Ambient humidity",
    'TEMPERATURE': "Ambient temperature",
}


OSC_SUPPLY = {
    'STATE': {
        0: "OFF",
        4: "CHANGING",
        5: "OFF_PENDING",
        6: "ON",
        7: "POWER_LOCK",
        9: "UNKNOWN",
    },

    'FAILURES': {
        'TEMPDET':   (0x01, "Temperature main power supply failure"),
        'OVERVOLT':  (0x02, "Overvoltage laser diode driver"),
        'UNDERVOLT': (0x04, "Undervoltage laser diode driver"),
        'CANBUS':    (0x08, "CAN bus error"),
        'POWER':     (0x10, "Laser diode driver power failure"),
        'TEMPBAR':   (0x20, "Laser diode bar thermo detector failure"),
        'TEMP':      (0x40, "Laser diode bar overtemperature"),
        'TEMPMAINS': (0x80, "Main power supply overtemperature"),
    },

    'CURRENT': "Current (mA)",
    'VOLTAGE': "Voltage (mV)",
    'SETCUR' : "Programmed current (mA)"
}


RA_SUPPLY = {
    'STATE': {
        0: "OFF",
        4: "CHANGING",
        5: "OFF_PENDING",
        6: "ON",
        7: "POWER_LOCK",
        8: "UNKNOWN"
    },

    'FAILURES': {
        'TEMPDET':   (0x01, "Temperature main power supply failure"),
        'OVERVOLT':  (0x02, "Overvoltage laser diode driver"),
        'UNDERVOLT': (0x04, "Undervoltage laser diode driver"),
        'CANBUS':    (0x08, "CAN bus error"),
        'POWER':     (0x10, "Laser diode driver power failure"),
        'TEMPBAR':   (0x20, "Laser diode bar thermo detector failure"),
        'TEMP':      (0x40, "Laser diode bar overtemperature"),
        'TEMPMAINS': (0x80, "Main power supply overtemperature"),
    },

    'CURRENT': "Current (mA)",
    'VOLTAGE': "Voltage (mV)",
    'SETCUR' : "Programmed current (mA)",
}


OSC_CTRL = {
    'STATE': {
        'UNKWN':   (0x01, "Unknown oscillator state"),
        'LOCKED':  (0x08, "Output power is in locked range"),
        'LOCKING': (0x10, "Power locking state"),
        'START':   (0x20, "Oscillator is starting"),
        'RUN':     (0x40, "Oscillator is running"),
        'ON':      (0x80, "Oscillator is operational"),
    },

    'PDOFFSET':   "Photodiode offset (ADC counts)",
    'PDCONV':     "Photodiode power conversion factor (mW/ADC counts)",
    'TEMP':       "Laser diode bar temperature",
    'PDOUT':      "Photodiode readout value (ADC counts)",
    'PLSETPOINT': "Power lock setpoint (ADC counts) -- P = PDCONV (PDOUT - PDOFFSET)",
}


RA_CTRL = {
    'STATE': {
        'UNKWN':   (0x01, "Unknown RA state"),
        'LOCKED':  (0x08, "RA output power is in locked range"),
        'LOCKING': (0x10, "RA power locking state"),
        'START':   (0x20, "RA is soft starting"),
        'RUN':     (0x40, "RA is running"),
        'ON':      (0x80, "RA is operational"),
    },
    
    'PDOFFSET':   "Photodiode offset (ADC counts)",
    'PDCONV':     "Photodiode power conversion factor (mW/ADC counts)",
    'TEMP1':      "Laser diode bar temperature 1",
    'TEMP2':      "Laser diode bar temperature 2",
    'PDOUT':      "Photodiode readout value (ADC counts)",
    'PLSETPOINT': "Power lock setpoint (ADC counts)",
    'PLCORR':     "Power lock  correction to setpoint",
    'HUMIDITY':   "Relative humidity",
    'TEMP':       "Temperature",
}


SHUTTER_CTRL = {
    'STATE': {
        'ENABLED':    (0x01, "Enabled"),
        'OPENED':     (0x02, "Shutter opened"),
        'REM_INTLCK': (0x04, "Remote interlock active"),
        'EMRGSTOP':   (0x08, "Emergency stop active"),
        # 1: "ENABLED",
        # 2: "SHUTTER_OPENED",
        # 4: "REMOTE_INTERLOCK",
        # 8: "EMERGENCY_STOP",
    },
    
    'CPLD1': {
        'OPERATIONAL':    (0x01, "SHUTTER_CPLD_STATUS_ESTOP_NORMAL"),
        'POWER_FAILURE':  (0x02, "SHUTTER_CPLD_STATUS_POWER_FAILURE"),
        'CLOCK_FAILURE':  (0x04, "SHUTTER_CPLD_STATUS_CLOCK_FAILURE"),
        'HIGH_ACT':       (0x08, "SHUTTER_CPLD_STATUS_SHUTTER_LINE_HIGH_ACTIVE"),
        'LOW_ACT':        (0x10, "SHUTTER_CPLD_STATUS_SHUTTER_LINE_LOW_ACTIVE"),
        'OPEN':           (0x20, "SHUTTER_CPLD_STATUS_SHUTTER_OPENED"),
        'CLOSED1':        (0x40, "SHUTTER_CPLD_STATUS_SHUTTER_CLOSED_1"),
        'CLOSED2':        (0x80, "SHUTTER_CPLD_STATUS_SHUTTER_CLOSED_2"),
        'RELAY_FAILURE': (0x100, "SHUTTER_CPLD_STATUS_INTERLOCK_RELAY_FAILURE"),
        'OVER_FREQ':     (0x200, "SHUTTER_CPLD_STATUS_ESTOP_OVER_FREQUENCY"),
    },

    'CPLD2': {
        'OPERATIONAL':    (0x01, "SHUTTER_CPLD_STATUS_ESTOP_NORMAL"),
        'POWER_FAILURE':  (0x02, "SHUTTER_CPLD_STATUS_POWER_FAILURE"),
        'CLOCK_FAILURE':  (0x04, "SHUTTER_CPLD_STATUS_CLOCK_FAILURE"),
        'HIGH_ACT':       (0x08, "SHUTTER_CPLD_STATUS_SHUTTER_LINE_HIGH_ACTIVE"),
        'LOW_ACT':        (0x10, "SHUTTER_CPLD_STATUS_SHUTTER_LINE_LOW_ACTIVE"),
        'OPEN':           (0x20, "SHUTTER_CPLD_STATUS_SHUTTER_OPENED"),
        'CLOSED1':        (0x40, "SHUTTER_CPLD_STATUS_SHUTTER_CLOSED_1"),
        'CLOSED2':        (0x80, "SHUTTER_CPLD_STATUS_SHUTTER_CLOSED_2"),
        'RELAY_FAILURE': (0x100, "SHUTTER_CPLD_STATUS_INTERLOCK_RELAY_FAILURE"),
        'OVER_FREQ':     (0x200, "SHUTTER_CPLD_STATUS_ESTOP_OVER_FREQUENCY"),
    },
}


SYNC_CTRL = {
    'TEM': [
        {
            0: "DISABLED",
            1: "DISABLED_FAILING",
            4: "ENABLED_STOPPED",
            5: "ENABLED_RUNNING",
            7: "ENABLED_STARTING",
        },
        {
            'PP_OFF':    (0x10, "Pulse picker off"),
            'PP_ON':     (0x20, "Pulse picker on"),
            'PP_OPENED': (0x40, "Pulse picker opened"),
            'PP_DIRECT': (0x80, "Direct pulse picker control"),
        },
    ],

    'CONTROLLER': {
        'EXT_RA':   (0x02, "External control of RA"),
        'EXT_PP':   (0x10, "External control of PP"),
        'EXT_FRQ':  (0x20, "External frequency generator source"),
        'INVERTED': (0x80, "RA and PP control levels are inverted"),
    },

    'FAILURES': {
        'SYNC_SHRT':     (0x01, "Sync period too short"),
        'SYNC_LONG':     (0x02, "Sync period too long"),
        'LASER_COVER1':  (0x20, "Laser cover switch 1 activated"),
        'LASER_COVER2':  (0x30, "Laser cover switch 2 activated"),
        'VOLTAGE':       (0x40, "5 V failure"),
        'OSC_SYNC':     (0x400, "Oscillator synchronisation failure"),
        'NARROW_BW':    (0x800, "Narrow bandwidth failure"),
        'OSC_OFF':     (0x8000, "Oscillator not started"),
        'TEM_FAIL':   (0x10000, "Common TEM failure"),
        'RA_WARN':    (0x20000, "RA level too high warning"),
        'RA_FAIL':    (0x40000, "RA level too high failure"),
        'RA_FREQ':    (0x80000, "RA freqeuncy overrun"),
        'FREQ_FAIL': (0x100000, "Frequency put of locked range failure"),
        'RA_OFF':    (0x800000, "RA laser diode driver not started"),
    },

    'FAILURES_MASK': {
        'SYNC_SHRT':     (0x01, "Sync period too short"),
        'SYNC_LONG':     (0x02, "Sync period too long"),
        'LASER_COVER1':  (0x20, "Laser cover switch 1 activated"),
        'LASER_COVER2':  (0x30, "Laser cover switch 2 activated"),
        'VOLTAGE':       (0x40, "5 V failure"),
        'OSC_SYNC':     (0x400, "Oscillator synchronisation failure"),
        'NARROW_BW':    (0x800, "Narrow bandwidth failure"),
        'OSC_OFF':     (0x8000, "Oscillator not started"),
        'TEM_FAIL':   (0x10000, "Common TEM failure"),
        'RA_WARN':    (0x20000, "RA level too high warning"),
        'RA_FAIL':    (0x40000, "RA level too high failure"),
        'RA_FREQ':    (0x80000, "RA freqeuncy overrun"),
        'FREQ_FAIL': (0x100000, "Frequency put of locked range failure"),
        'RA_OFF':    (0x800000, "RA laser diode driver not started"),
    },
    
    'RA_DUMP_TIME':  "RA dumping time in (ns)",
    'NARROW_BW_CTS': "Narrow bandwidth detector readout (ADC counts)",
    'OSC_LEVEL':     "Oscillator level (ADC counts)",
    'INT_FREQ':      "Laser internal operating frequency (Hz)",
    'EXT_FREQ':      "Laser measured external operating frequency (Hz)",
    
}


HV1_CTRL = {
    'HV_STATE': {
        'SUPPLY': (0x01, "High voltage supply is operational"),
        'HV_ON':  (0x02, "High voltage supply is on"),
        'HV_200': (0x04, "This is 200 W HV supply"),
    },

    'ERROR': {
        'CURRENT': (0x01, "Current too high"),
        'VOLTAGE': (0x02, "Voltage too high"),
        'VOLT_HW': (0x04, "Voltage too high -- hardware comparator error"),
        'TEMP':    (0x08, "Overheat"),
    },

    'VOLTAGE':  "Current voltage (V)",
    'SETPOINT': "Voltage setpoint (V)",
    'CURRENT':  "Current (mA)",
}


HV2_CTRL = {
    'HV_STATE': {
        'SUPPLY': (0x01, "High voltage supply is operational"),
        'HV_ON':  (0x02, "High voltage supply is on"),
        'HV_200': (0x04, "This is 200 W HV supply"),
    },

    'ERROR': {
        'CURRENT': (0x01, "Current too high"),
        'VOLTAGE': (0x02, "Voltage too high"),
        'VOLT_HW': (0x04, "Voltage too high -- hardware comparator error"),
        'TEMP':    (0x08, "Overheat"),
    },

    'VOLTAGE':  "Current voltage (V)",
    'SETPOINT': "Voltage setpoint (V)",
    'CURRENT':  "Current (mA)",
}


CW_CTRL = {
    'CW_LMIN': "CW_Lmin parameter",
    'CW_LDIF': "CW_Ldif parameter",
    'CW_OSCP': "CW_OscPeriod parameter",

    'CW_STATE': {
        0: "CW_STARTUP_STATE_IDLE",
        2: "CW_STARTUP_STATE_WAIT_TEMPERATURE",
        3: "CW_STARTUP_STATE_HEATING",
        4: "CW_STARTUP_STATE_MONITOR",
        5: "CW_STARTUP_STATE_ML_SEARCH",
        6: "CW_STARTUP_STATE_CW_SEARCH",
        7: "CW_STARTUP_STATE_CW_REPORT",
        8: "CW_STARTUP_STATE_ML_BREAKUP_SEARCH",
        9: "CW_STARTUP_STATE_STARTING",
       10: "CW_STARTUP_STATE_STANDBY",
       11: "CW_STARTUP_STATE_ERROR",
    },
    
    'CW_ERROR': {
        'BADSTATE':      (0x01, "CW_STARTUP_ERROR_BAD_STATE"),
        'TEMP':          (0x02, "CW_STARTUP_ERROR_BAD_WRONG_TEMPERATURE"),
        'SIG_LEVEL':     (0x04, "CW_STARTUP_ERROR_BAD_SIGNAL_LEVEL"),
        'LOW_ML':        (0x08, "CW_STARTUP_ERROR_LOW_ML_SIGNAL"),
        'I_LIMIT':       (0x10, "CW_STARTUP_ERROR_BAD_I_LIMIT_REACHED"),
        'ML_NOT_FOUND':  (0x20, "CW_STARTUP_ERROR_BAD_ML_NOT_FOUND"),
        'CW_NOT_FOUND':  (0x30, "CW_STARTUP_ERROR_BAD_CW_NOT_FOUND"),
        'NO_CW':         (0x40, "CW_STARTUP_ERROR_BAD_CW_NOT_PRESENT"),
        'NO_ML':         (0x80, "CW_STARTUP_ERROR_BAD_NO_ML"),
        'COLD_START':   (0x100, "CW_STARTUP_ERROR_BAD_COLD_START"),
        'CANT_START':   (0x200, "CW_STARTUP_ERROR_BAD_CANT_START"),
    }
}
