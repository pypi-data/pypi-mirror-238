#!/usr/bin/python3

#
#        Syncster Library for terminal access to Menlo Syncro synchronizers.
#        Copyright (C) 2022 Florin Boariu.
#
#        This program is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        (at your option) any later version.
#
#        This program is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import struct
import serial
from syncster import rbp, hrt

'''
HR Tree information specific to the Menlo Syncro RRE
'''

SyncroTree = {
    "DEV_addr":   { "addr": b'\x60', "typeid": 0x07, "access": "rw" },
    "DEV_type":   { "addr": b'\x61', "typeid": 0x08, "access": "r"  },
    "MSGLOGHIST": { "addr": b'\xac', "typeid": 0xe4, "access": "r" },
    "RegFP":      { "addr": b'\xfc', "typeid": 0x81, "access": "r" }
}

'''
This is a list with names and numbers of submodules that can/may be found
in Syncro RRE boxes (mine definitely has most of these :-) The others I
got from the documentation.)
'''
SubmoduleAddrPrefixes = {
    "LOCKBOX":  b'\x01',
    "TRACKER0": b'\x02',
    "TRACKER1": b'\x03',

    "MOTOR1": b'\x05',
    "MOTOR2": b'\x06',
    "MOTOR3": b'\x07',

    "TEC-CTRL0": b'\x08',     # Tec-Ctrl 1 (prefix 0x08)
    "TEC-CTRL1": b'\x09',     # Tec-Ctrl 2 (prefix 0x09)    

    "DIO":   b'\x14',         # DIO Unit (prefix 0x14)

    "MOTOR4": b'\x1a',
    
    "DDS1":   b'\x3a',        # DDS Unit 1 (prefix 0x3a)

    "DEV":      b'\x6a',
    "DEV_FILE": b'\x6b',
    "REMOTE":   b'\x6c',
    
    "SCX1": b'\xc8',
    "HFS1": b'\xcc'
}

'''
Actionable parameters from the LOCKBOX.INPUT module (no submodules here).
LOCKBOX is typically, 0x01, INPUT is 0x01 on top of that.
'''
LockboxInputTree = {
    'ModEnable': { "addr": b'\x03', "access": "rw", "format": "B" },
    'AutoH2F':   { "addr": b'\x10', "access": "rw", "format": "B" },
    'TrigF2H':   { "addr": b'\x11', "access": "rw", "format": "B" },
}

'''
Prefix for this is LOCKBOX.INPUT (\x01\x01), then
Ch0 is prefix 0x04, Ch1 is prefix 0x05.
'''
LockboxInputChannelTree = {
    'Offset':           { "addr": b'\x01', "access": "rw", "format": ">l" },
    'Gain':             { "addr": b'\x02', "access": "rw", "format": ">l" },
    'Attenuate10dB':    { "addr": b'\x03', "access": "rw", "format": "B" },
    'Invert':           { "addr": b'\x04', "access": "rw", "format": "B" },
    'RawGain':          { "addr": b'\x05', "access": "rw", "format": ">l" }
}

'''
Prefix LOCKBOX.FAULTDETECTION (\x01 \x02).
'''
LockboxFaultDetectionTree = {
    'AcThreshold':           {},
    'DcThreshold':           {},
    'AcAutodetectEnable':    {},
    'AcAutodetectThreshold': {},
    'AcViolationsPerSec':    {},
}

'''
Prefix LOCKBOX (\x01), PID (\x03).
'''
LockboxPidTree = {
}

'''
Prefix LOCKBOX (\x01), PID (\x03), P (\x07)
'''
LockboxPidPTree = {
}

'''
Prefix LOCKBOX (\x01), PID (\x03), I (\x08)
'''
LockboxPidITree = {
}


'''
Prefix LOCKBOX (\x01), PID (\x03), D (\x09)
'''
LockboxPidDTree = {
}

'''
Prefix LOCKBOX (\x01), PID (\x03), INDICATOR (\x20)
'''
LockboxPidIndicatorTree = {
}


'''
Prerix LOCKBOX (\x01), OUTPUT (\x04)
'''
LockboxOutputTree = {
}

'''
Prefix LOCKBOX (\x01), Monitor (\x05).
'''
LockboxMonitorTree = {
}

'''
Prefix LOCKBOX (\x01), SLOWINT (\x06).
'''
LockboxSlowintTree = {
}

DdsTree = {
    "Phase": { "addr": b'\x06', "access": "rw", "format": ">l" }
}

def test_devaccess():
    
    hrt.debug_ls_node(0x01, name='LOCKBOX')

    hrt.debug_ls_node(0x02, name='TRACKER0')
    hrt.debug_ls_node(0x03, name='TRACKER1')

    hrt.debug_ls_node(0x05, name='MOTOR1')
    
    hrt.debug_ls_node(0x6a, name='DEV')
    hrt.debug_ls_node(0x6b, name='DEV_FILE')
    hrt.debug_ls_node(0x6c, name='REMOTE')

    hrt.debug_ls_node(0xc8, name='SCX1')
    hrt.debug_ls_node(0xcc, name='HFS1')
