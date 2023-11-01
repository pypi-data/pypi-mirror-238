#!/usr/bin/python3

#
#        MiniQuant --  Wrapper for PicoQuant's HydraHarp access libraries.
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

## This implements a mock interface for the HydraHarp. The mock interface
## does not supply any meaningful data or behavior, it is only designed to
## not outright crash the application when run against.
##
## It should, however, be able to pass all unit tests that the real interface
## is also passing.
##
## The idea is that software based on miniquant can be run and tested using
## the mock interface in all instances that don't actually depend on reliable
## data. This should allow for automated unit testing of higher appliaction
## levels without actual access to a Harp device.

import numpy as np
import time

from miniquant.harp import MeasurementControl, MeasurementMode, EdgeSelection, \
    ReferenceClock, DeviceLimits, HarpWarnings, HarpFlags, HarpFeatures, \
    OrthogonalFlagsMap, HarpError

class ModuleInfo:
    def __init__(self, harp, modindex):
        self.info = { "code": 3, "version": 4 }

class InputChannel:
    def __init__(self, harp, channel):
        self.harp = harp
        self.channel = channel
        self.moduleIndex = 1
        self.clearOnReadout = False
        self.enabled = False
        self.offset = 0
        self.cfd = {"level": 0.345, "zerox": 0.002 }
        self.countRate = 0
        self.histogram = np.array([0 for i in range(256)])

    def __repr__(self):
        return "MockChannel[%d]" % self.channel
        

class MonsterHarp(object):

    def __repr__(self):
        return "MockHarp-%d" % self.serial
    
    def initialize(self, mode, clock):
        pass

    def calibrate(self):
        pass

    def clearHistogram(self):
        pass

    def acquire(self, aqtime):
        self._acq_stop_time = time.time()+aqtime
        
    def acqstop(self):
        self._acq_stop_time = time.time()

    @property
    def acquiring(self):
        '''
        This will mock aquisition by return `True` for a period of time
        after turning it on
        '''
        return time.time() < self._acq_stop_time

    @acquiring.setter
    def acquiring(self, enable):
        if enable:
            self.acquire(self.acquisitionTime)
        else:
            self.acqstop()

    # This is also trick, acquisition should turn itself off.

    @property
    def serialNumber(self):
        return self.serial

    @property
    def syncCfd(self):
        return self._syncCfd
    
    @syncCfd.setter
    def syncCfd(self, data):
        if isinstance(data, dict):
            self._syncCfd = data
        else:
            self._syncCfd = dict({"level": data[0], "zerox": data[1]})

    @property
    def histogramLength(self):
        if self._histogramLength is None:
            return None
        return (2**self._histogramLength) 

    @histogramLength.setter
    def histogramLength(self, val):
        if val > 6:
            raise HarpError("Should be <=6")
        self._histogramLength = val

    @property
    def resolution(self):
        return self.baseResolution[0] * 2**self.binning
    
    def __init__(self, id=0, hlib=None):
        self.serial = 4711
        self.hardwareInfo = { "model": 'MockHarp', "part": '23', "vesion": '17' }
        self.features = []
        self.channels = [ InputChannel(None, i) for i in range(4) ]
        self.modules =  [ ModuleInfo(None, i) for i in range(4) ]
        self.hardwareDebugInfo = "There is no harp."
        self.syncDiv = 1
        self._syncCfd = {"level": 0.312, "zerox": 0.011 }
        self.syncChannelOffset = 0.3
        self.stopOverflow = False
        self.binning = 0
        self.offset = 0
        self.baseResolution = (1e-12, DeviceLimits.MaxBinning)
        self._histogramLength = None
        
        self.measurementControl = {"control": MeasurementControl.ContC1Gated,
                                   "startedge": EdgeSelection.Rising,
                                   "stopedge": EdgeSelection.Falling }

        self.acquisitionTime = 1.0
        self._acq_stop_time = 0        
        self.clearOnAcquire = True
        self.syncRate = 23
        self.syncPeriod = 1/self.syncRate
        self.warnings = [ 'BATMAN_IS_DEAD' ]
        self.flags = [ 'BATMAN_IS_NOT_DEAD' ]
        self.markers = [ None for i in range(4) ]
        self.markerHoldoffTime = 0.003
        self.fifo = np.array([0 for i in range(self.histogramLength or DeviceLimits.MaxHistogramLength)])
        

class Monster(object):

    def find(self, *serials, maxdev=8):

        r = []
        for s in serials:

            if s in [ "first", "any" ]:
                return MonsterHarp()

            if s in [ "all" ]:
                return [MonsterHarp()]

            if s in [ "unlikely" ]:
                raise OSError("Unit tests demand that this serial doesn't exist")            
            
            if isinstance(s, str) or type(s) == int:
                m = MonsterHarp()
                m.serial = s
                return m
            
            r.append(MonsterHarp())
            r[-1].serial = s
            
        return r

    def __new__(self, *args, **kwargs):
        # Make a singleton
        if not hasattr(self, 'instance'):
            self.instance = super(Monster, self).__new__(self)            
        return self.instance
    
    def __init__(self, library=None):
        self.libraryVersion = 'Mock v0.1'
        self.errorString = ''

monster_binding = Monster()
