#!/usr/bin/python3

#
#        Diddy Library for terminal access to Menlo DDS synchronizers.
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

import serial
import time
from yaml import load, dump
from pprint import pprint

from os import environ

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except:
    from yaml import Loader, Dumper

class DdsIo(object):
    '''
    Basic input / output methods for the Menlo DDS. Tested with the DDS-120.
    '''

    errors = {
        'E0': "Ill-formatted command",
        'E1': "Parameter outside of valid range",
    }

    def __init__(self, port=None, **pyserial_kwargs):
        '''
        Opens the specified USB device for communication.
        `port` is the USB device name. The rest of the parameters
        are passed to the `Serial` initialisation.
        '''

        if port is None:
            port = environ.get("DIDDY_PORT", "/dev/ttyUSB0")

        defaults = {
            'timeout': 3.0 ## seconds -- should be enough.
        }

        for k in defaults.keys():
            if pyserial_kwargs.get(k, None) is None:
                pyserial_kwargs[k] = defaults[k]

        self.device = serial.Serial(port, **pyserial_kwargs)
        self.port   = port


    def exec(self, cmd):
        '''
        Sends a command string and checks the response.

        `cmd` is expected to be the string part of the command,
        without start/stop bytes.

        If the response is any of the `Ex` strings, a corresponding
        exception is raised (based on `IOError`). The same happens
        if the response is anything but `OK` for any of the `SET`
        commands.

        For the `GET` commands, an error is raised on any error,
        or the response string is returned on success.
        '''

        # We check whether this is a setter command by explicitly
        # checking some of the commands here. Yes, it's ugly, but
        # we expect the protocol to be exremely simple :-) If
        # we get stuck, we need a better design.
        scmd = cmd.strip().upper()
        is_setter = scmd.find('SET') == 0 or scmd.find('AUSGANG') == 0

        data = bytes('\01%s\03' % cmd, encoding='ascii')
        #print ("<", data)
        self.device.write(data)
        self.device.flush()

        response = bytes()
        while True:
            b = self.device.read()
            #print (">", b)
            if len(b) < 1:
                raise IOError('Timeout while reading from %s after %r' \
                              % (self.port, response))
            response += b
            if response[-1] == 3:
                break

        if response[0] != 1:
            raise IOError('Unexpected start byte in response %r' % response)

        rstr = response.decode('ascii')[1:-1]

        try:
            raise IOError("%s: %s" % (rstr, DdsIo.errors[rstr]))
        except KeyError:
            pass

        if not is_setter:
            return rstr

        if rstr.upper() != 'OK':
            raise IOError("Unexpected answer: %r" % rstr)


    @property
    def config(self):
        '''
        Wrapper for `GET KONFIG`, returns a dict with the fields
        "clock", "multiplier", "daq" and "buzzer"
        '''

        cfg = self.exec('GK').upper().split('-')
        plist = [ c.split(':') for c in cfg[1:]]
        params = { c[0]: c[1:] for c in plist }

        return { "clockMHz": int(params['IC'][0]) if params['IC'][1] == "E" else None,
                 "maxClockMHz": int(params['MX'][0]),
                 "multiplier": int(params['ML'][0]) if params['ML'][1] == "1" else None,
                 "daq": float(params['DQ'][0])/100.0,
                 "buzzer": float(params['BZ'][0])/100.0 }

    @config.setter
    def config(self, cfg):
        '''
        Sets the config. `cfg` is either a config map with the following fields:
          - `clockMHz`: input clock in MHz, or `None` for internal clock
          - `multiplier`: Multiplier, `None` for disabled
          - `buzzer`: buzzer (floating point 0..1)
          - `daq`: DAQ (floating point 0..1)
        '''

        s = '-IC:%03d:%c' % (cfg["clockMHz"] or 0,
                             'E' if cfg["clockMHz"] is not None else 'I') + \
            '-ML:%02d:%c' % (cfg["multiplier"] or 0,
                             '1' if cfg["multiplier"] is not None else '0') + \
            '-DQ:%03d' % (cfg["daq"] * 100) + \
            '-BZ:%03d' % (cfg["buzzer"] * 100)

        return self.exec(s)

    @property
    def frequencyHz(self):
        return float(self.exec("GF"))*1e-5

    @frequencyHz.setter
    def frequencyHz(self, val):
        self.exec("SF%014d" % int(val*1e5))


    @property
    def phaseDeg(self):
        return float(self.exec("GP"))*1e-3

    @phaseDeg.setter
    def phaseDeg(self, val):
        self.exec("SP%06d" % int(val*1e3))


    @property
    def outputChannel(self):
        return int(self.exec("GOUT"))

    @outputChannel.setter
    def outputChannel(self, val):
        self.exec("SOUT%1d" % val)


    @property
    def amplitude(self):
        yobj = {}
        ampl = self.exec("GA")

        if ampl[0] == "V":
            yobj["value"] = float(ampl[1:])*1e-3
            yobj["units"] = "mV"
        elif ampl[0:2] == "dB":
            yobj["value"] = float(ampl[2:])*1e-1
            yobj["units"] = "dB"
        else:
            raise RuntimeError("Confusing amplifier value: %s" % ampl)

        return yobj

    @amplitude.setter
    def amplitude(self, val):
        if isinstance(val, dict):
            yobj = val
        else:
            yobj = { "value": val[0], "units": val[1] }

        if yobj["units"] == "mV":
            self.exec("SAV%05d" % int(yobj["value"]*1e3))
            self.exec("SMAV")

        elif yobj["units"] == "dB":
            self.exec("SAD%-03d" % int(yobj["value"]*1e1))
            self.exec("SMAD")


    @property
    def remoteControl(self):
        return self.exec("GR") == '1'

    def setRemoteControl(self):
        self.exec("SR")

    @outputChannel.setter
    def outputChannel(self, val):
        self.exec("SOUT%1d" % val)


    @property
    def firmwareVersion(self):
        return self.exec("GV")


    @property
    def serialNumber(self):
        return self.exec("GS")


    @property
    def settings(self):
        '''
        Returns a dictionary with all DDS-120 settings.
        '''

        yobj = {}

        yobj["remoteControl"] = self.remoteControl

        yobj["amplitude"]     = self.amplitude
        yobj["frequencyHz"]   = self.frequencyHz
        yobj["phaseDeg"]      = self.phaseDeg
        yobj["outputChannel"] = self.outputChannel

        yobj["configuration"] = self.config

        # read-only
        yobj["firmwareVersion"] = self.firmwareVersion
        yobj["serialNumber"] = self.serialNumber

        ## available in documentation, but not existent?
        #yobj["frequencyOffset"] = dds.exec("GO")

        return yobj


    @settings.setter
    def settings(self, yobj):
        '''
        Sets all configuration parameters at once from a Yaml object.
        '''

        self.setRemoteControl()
        self.amplitude     = yobj["amplitude"]
        self.frequencyHz   = yobj["frequencyHz"]
        self.phaseDeg      = yobj["phaseDeg"]
        self.outputChannel = yobj["outputChannel"]

        #dds.exec("SO%07d" % offset)

        try:
            self.config = yobj["configuration"]
        except IOError:
            print("ACHTUNG, the SET-KONFIG command timed out, possibly without "
                  "any effect. This is a known bug of the DDS-120.")


def test_setconfig():

    dds = DdsIo("/dev/menlodds0")
    conf = dds.config

    dds.exec('SR')
    dds.config = conf
    conf2 = dds.config

    assert conf == conf2


def test_writesettings():
    '''
    Reads the current settings and tries to write them back.
    This of course won't check if the DDS behaves as it should,
    only of the API responds as documented.
    '''

    dds = DdsIo("/dev/menlodds0")
    conf = dds.settings
    dds.settings = conf
    conf2 = dds.settings

    assert conf == conf2


def test_getversion():
    '''
    Read a version string.
    '''

    con = serial.Serial("/dev/menlodds0", 9600, timeout=1.0)
    cmd = bytes('\01GV\03', encoding='ascii')
    print (">>>", cmd)
    con.write(cmd)
    con.flush()

    data = bytes()
    while True:
        d = con.read()
        if len(d) < 1:
            break
        else:
            data += d
    print ("<<<", data)

    assert data[0] == 1
    assert data[1] == 3


def test_readsettings():

    dds = DdsIo()
    foo = dds.settings
    assert len(foo) > 3


if __name__ == "__main__":

    from sys import argv

    # rapid testing: read input off argv[1]
    dds = DdsIo(argv[1] if len(argv) >= 2 else None)
    print (dds.settings)
