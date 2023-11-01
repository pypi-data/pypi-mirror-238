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

import ctypes
from ctypes import byref
from os import environ as env
from os import strerror
from time import sleep
import errno
from numpy.ctypeslib import as_array
from numpy import zeros

from threading import Lock

import logging

class HarpError(Exception):
    '''
    Base class for reporting errors of a Harp device
    '''
    def __init__(self, harpcode=-1, message=None):
        self.harpcode = harpcode
        self.message = message

    def __str__(self):
        return "Harp error: %s (%d)" % (self.message or "*arrrgh!*", self.harpcode)

    def __repr__(self):
        return str(self)

    
class ErrorStringPortal:
    '''
    Wrapper class for GetErrorString(). The purpose is to provide
    an indexing interface which can mimic error strings as being
    an array or a dictionary.
    '''
      
    def __init__(self, hlib):
        self.hlib = hlib
            
    def __getitem__(self, err):
        buf = ctypes.create_string_buffer(b'', 256)
        self.hlib.HH_GetErrorString(buf, err)
        return buf.value.decode('utf-8')

    def __call__(self, ret):
        '''
        Checks `ret` for success value (`==0`) or raises an exception
        containing the error message.
        '''
        if ret < 0:
            raise HarpError(harpcode=ret, message=self[ret] if self.hlib else None)
        
        
class MeasurementControl:
    '''
    Constants / settings for HH_SetM2022-12-10 13:03:24,492 INFO: histogram: has become available again                                                                                             
easControl. See
    [HydraHarp 400 Documentation](https://raw.githubusercontent.com/PicoQuant/HH400-v3.x-Demos/master/Linux/manual_HHLibLinuxv3.0.0.2.pdf).
    '''
    ContC1Gated = 4
    ContC1StartCtcStop = 5
    ContCtcRestart = 6

class MeasurementMode:
    '''
    Constants for HH_Initialize `mode` parameter
    '''
    Histogramming = 0
    T2 = 2
    T3 = 3
    Continuous = 8


class MeasurementControl:
    '''
    Constants for `HH_SetMeasControl`.
    '''
    SingleShotCtc = 0
    C1Gated = 1
    C1StartCtcStop = 2
    C1StartC2Stop = 3
    ContC1Gated = 4
    ContC1StartCtcStop = 5
    ContCtcRestart = 6


class EdgeSelection:
    '''
    Constants for ede determination, used in `HH_SetMeasControl`.
    '''
    Falling = 0
    Rising = 1


class ReferenceClock:
    '''
    Constants for HH_Initialize `refsource`.
    '''
    Internal = 0
    External = 1

class DeviceLimits:
    '''
    Some hard-coded maximal legths and other devicel limits.
    May or may not change...?
    '''
    MaxHistogramLength = 65536    ## MAXHISTLEN
    MaxHistogramKBase  = 6        ## MAXLENCODE (the base for exponent 2 as a KB histo length)
    MaxDevices         = 8        ## MAXDEVNUM
    MaxBinning         = 26       ## MAXBINSTEPS
    CModeMaxHistogramLength = 8192   ## MAXHISTLEN_CONT
    CModeMaxHistogramKBase  = 3      ## MAXLENCODE_CONT
    CModeMaxBufferLength    = 262272 ## MAXCONTMODEBUFLEN
    MaxFifoReadout     = 131072   ## TTREADMAX
    MinFifoReadout     = 128      ## TTREADMIN
    MaxBytesReadout   = 262272    ## MAXCONTMODEBUFLEN
#
# Warning texts from the HHLIB API definition.
#
# This is a map of warning masks to strings.
# We save two strings: the "official" API constant name for recognition,
# and the unofficial "plain English" translation. Most of the time they're
# the same, but they may not be.
HarpWarnings = {
    'SYNC_RATE_ZERO':      (0x001, 'Sync rate is zero'),
    'SYNC_RATE_TOO_LOW':   (0x002, 'Sync rate is too low'),
    'SYNC_RATE_TOO_HIGH':  (0x004, 'Sync rate is too high'),
    'INPT_RATE_ZERO':      (0x010, 'Input rate is zero'),
    'INPT_RATE_TOO_HIGH':  (0x040, 'Input rate is too high'),
    'INPT_RATE_RATIO':     (0x100, 'Bad input rate ratio'),
    'DIVIDER_GREATER_ONE': (0x200, 'Rate divider is greater than 1'),
    'TIME_SPAN_TOO_SMALL': (0x400, 'Time span is too small'),
    'OFFSET_UNNECESSARY':  (0x800, 'Offset unnecessary') }


#
# Flags as specified in the HHLIB API for current status
#
HarpFlags = {
    'OVERFLOW':  (0x0001, "Aquisiton overflow"),
    'FIFOFULL':  (0x0002, "FIFO buffer is full"),
    'SYNC_LOST': (0x0004, "Lost synchronisation"),
    'REF_LOST':  (0x0008, "Lost reference signal"),
    'SYSERROR':  (0x0010, "You broke it, you pay for it"),
    'ACTIVE':    (0x0020, "Data aquisition in process") }

#
# Features as specified in the HHLIB API (a.k.a. device capabilities)
#
HarpFeatures = {
    'DLL':     (0x01, "DLL Mode"),
    'TTTR':    (0x02, "TTTR Mode"),
    'MARKERS': (0x04, "Markers"),
    'LOWRES':  (0x08, "Low resolution mode"),
    'TRIGOUT': (0x10, "Trigger output") }


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
        if code:
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
    

class ModuleInfoPortal:
    '''
    Wrapper class for `HH_GetModuleInfo`. The purpose is to provide
    an indexing interface which can mimic module info as being
    an array.
    '''

    class ModuleInfo:
        '''
        The class with the actuar getter code for HH_GetModuleInfo
        '''
        def __init__(self, harp, modindex):
            self.harp = harp
            self.mod = modindex

        @property
        def info(self):
            code = ctypes.c_int()
            ver  = ctypes.c_int()
            self.harp.hlib.HH_GetModuleInfo(self.harp.devid, self.mod, byref(code), byref(ver))
            return { "code": code.value, "version": ver.value }

            meascontrol
        
    def __init__(self, harp):
        self.harp = harp

    def __iter__(self, *args):
        l = len(self)
        for i in range(l):
            yield self[i]            
            
    def __getitem__(self, mod):
        return self.ModuleInfo(self.harp, mod)
        
    def __len__(self):
        n = ctypes.c_int()
        self.harp.hlib.HH_GetNumOfModules(self.harp.devid, ctypes.byref(n))
        return n.value


class InputChannelPortal:
    '''
    Wrapper class for various channel-based classes The purpose is to provide
    an indexing interface which can mimic module info as being an array.
    Each element in that array is a Channel and has attributes that correspond
    to getter and setter functions like:
      - HH_GetModuleIndex
      - HH_SetInputCFD
      - HH_SetInputChannelOffset
      - HH_SetInputChannelEnable
      - HH_GetHistogram
      - HH_GetCountRate
    '''

    class InputChannel:
        '''
        The actual Channel class that has all the getters/setters.
        '''
        def __init__(self, harp, channel):

            self.harp = harp
            #self.hlib = harp.hlib           # HHLIB handler to talk to
            #self.devid = harp.devid         # Harp device we're using
            self.channel = channel          # that's us, the channel ID
            self.clearOnReadout = False

        def __str__(self):
            return "%r:ch[%d]" % (self.harp, self.channel)

        
        def __repr__(self):
            return str(self)
            

        @property
        def moduleIndex(self):
            ''' module which serves this channel '''
            modofc = ctypes.c_int()
            self.harp.hlib_request('HH_GetModuleIndex', self.channel, byref(modofc))
            return modofc.value

        @property
        def enabled(self):
            return self.harp.shadow('ch%d-enabled' % self.channel, None)

        @enabled.setter
        def enabled(self, val):
            '''
            Wrapper for `HH_SetInputChannelEnable`. Working with a shadow value
            for artificial getter.
            '''
            enbl = 1 if val else 0
            self.harp.hlib_request('HH_SetInputChannelEnable', self.channel, enbl,
                                   shadow='ch%d-enabled' % self.channel, value=bool(val))


        @property
        def offset(self):
            ''' returns last value from shadow cache '''
            return self.harp.shadow('ch%d-offset' % self.channel, None)

        @offset.setter
        def offset(self, value):
            '''
            Wrapper for `HH_SetInputChannelOffset`.
            Working with a shadow value for artificial getter.
            Time offset value here is seconds (floating point),
            opposed to picoseconds of `HH_SetInputChannelOffset`.
            '''
            self.harp.hlib_request('HH_SetInputChannelOffset', self.channel, int(value*1e12),
                                   shadow='ch%d-offset' % self.channel, value=value)

            
        @property
        def cfd(self):
            ''' returns CFD from shadow '''
            return self.harp.shadow('ch%d-cfd' % self.channel, None)

        @cfd.setter
        def cfd(self, data):
            '''
            Sets the CFD -- data is either a tuple `(level, zerox)` or a dict
            `{"value": ..., "zerox": ...}`. This is a wrapper for `HH_SetInputCFD`.
            '''
            if isinstance(data, dict):
                d = data
            else:
                d = dict({"level": data[0], "zerox": data[1]})
            ret = self.harp.hlib_request('HH_SetInputCFD', self.channel,
                                         int(d["level"]*1e3), int(d["zerox"]*1e3),
                                         shadow='ch%d-cfd' % self.channel, value = d)


        @property
        def countRate(self):
            ''' Wrapper for `HH_GetCountRate`. '''
            s = ctypes.c_int()
            self.harp.hlib_request('HH_GetCountRate', self.channel, byref(s))
            return s.value


        @property
        def histogram(self):
            '''
            Returns an ndarray with the current histogram data for this channel.
            Clears the acquisition buffer after data retrieval.
            '''
            numpts = self.harp.feedback.get('histogramLength',
                                             DeviceLimits.MaxHistogramLength) 

            #logging.debug("Flags: %r" % ([f for f in self.harp.flags],))
            
            #if self.harp.acquiring:
            #	return None #zeros([numpts])
            #numpts_param = ctypes.c_int(numpts)
            
            erase = ctypes.c_int32(int(self.clearOnReadout))
            dbuf = (ctypes.c_int32*numpts)()
            self.harp.hlib_request('HH_GetHistogram', dbuf, self.channel, erase)
            data = as_array(dbuf)
            logging.debug("Histogram readout with %d counts total in %d channels, still acquiring: %r" \
            	% (data.sum(), data.shape[0], self.harp.acquiring))
            return data
            
        
    def __init__(self, harp):
        self.harp = harp

    def __iter__(self, *args):
        l = len(self)
        for i in range(l):
            yield self[i]            
            
    def __getitem__(self, ch):
        return self.InputChannel(self.harp, ch)

    def __len__(self):
        n = ctypes.c_int()
        self.harp.hlib_request('HH_GetNumOfInputChannels', ctypes.byref(n))
        return n.value
    

class MonsterHarp(object):
    '''
    Manages one specific HydraHarp device (i.e. one of the `HH_OpenDevice()`
    thingies that has an integer index).
    Offers all the `HH_...` functions of the HydraHarp library with a more
    pythonic interface.
    '''

    class ReferenceCounter:
        ''' Used to know when to close the device '''
        def __init__(self):
            self.counter = 1

        def inc(self):
            self.counter += 1
            return self.counter

        def dec(self):
            self.counter -= 1
            return self.counter

        def __bool__(self):
            return (self.counter > 0)


    def __init__(self, id=0, hlib=None, mt=True):
        '''
        Initializes / opens the device with the specified id.
        
        Parameters:
        
          - `id`: This is an integer to represent which device to open,
            from the point of view of the HH-library. It is unclear how
            the library tells different devices apart and which one
            has which ID; however, apparently valid IDs go from 0 to 7,
            and usually only one is available when only one USB device
            is attached.
        
          - `hlib`: This is a `Monster` object, which is a wrapper around
            a `ctypes.CDLL()` object around the HH-library.
            The `Monster` class is a singleton, i.e. there is only one
            instance available in the system.
            See the `Monster` documentation about how the first default
            instance is initialized.
            You can grab one by calling its constructor (`m = Monster()`).

            Generally, `MonsterHarp` doesn't need an explicit `hlib` parameter
            set, the default being the module's `monster_binding` object.
            But one *can* be specified for... ahem... advanced needs :-)
                
        '''

        # If this is set, access to hlib will be protected my a mutex.
        self._lock = Lock() if mt else None
        
        self._hlib = hlib or Monster().hhlib ##monster_binding.hhlib

        # This is for the __copy__ / __deepcopy__ operator.
        # We need to reference everything from the source object.
        if id < 0:
            return
        
        sbuf = ctypes.create_string_buffer(b'', 16)
        self.refcnt = self.ReferenceCounter()
        ret = self.hlib.HH_OpenDevice(id, sbuf)

        self._shadow = {}
        self.feedback = {}

        if ret == 0:
            self.serial = sbuf.value.decode('utf-8')
            self.devid = id
            
        elif ret == -1:
            errcode = ctypes.get_errno()
            errstr = strerror(errcode)
            if errcode == errno.ETIMEDOUT:
                errstr += " (crappy hardware 0e0d:0009:k?)"
                self.devid = -1
            raise OSError(errcode, errstr)

        else:
            raise RuntimeError("This isn't supposed to return %d" % ret)

    @property
    def clearOnAcquire(self):
        '''
        Automatically clears histogram when acquisition is started
        '''
        return self._shadow.setdefault('clearOnAcquire', True)

    @clearOnAcquire.setter
    def clearOnAcquire(self, val):
        self._shadow['clearOnAcquire'] = val

    @property
    def hlib(self):
        '''
        Returns a reference to the HLIB object we're using, optionally protecting
        calls with a mutex (if the object was initianized with mt=True).
        '''
        return self._hlib

    def hlib_request(self, req, *params, shadow=None, value=None):
        '''
        Executes a lock-protected HLIB request and returns the result.
        If `shadow` is not None, the shadow key `shadow` will be set to
        value `value` while still undmeascontroler mutex protection.
        '''
        requestProc = getattr(self.hlib, req)
        logging.debug("HLIB request: %r" % (req))
        if self._lock:
            with self._lock:
                ret = requestProc(self.devid, *params)
                ErrorStringPortal(self.hlib)(ret)
                if shadow is not None:
                    self._shadow[shadow] = value
                return ret
        else:
            ret = requestProc(self.devid, *params)
            ErrorStringPortal(self.hlib)(ret)
            if shadow is not None:
                self._shadow[shadow] = value            
            return ret
    
        
    def __del__(self):
        if self.refcnt.dec():
            return
        
        if hasattr(self, 'devid') and self.devid >= 0:
            self.hlib.HH_CloseDevice(self.devid)
            self.refcnt = None
            self.devid  = None
            self.serial = None
            self._hlib   = None
            self._shadow = None
            self.feedback = None

            
    def __copy__(self):
        # Upon copy/deepcopy we take over references of the ID and refcounter
        # of the source object. Once opened, we don't want to prematurely
        # close the USB device (hhlib doesn't account for these types of
        # concurrencies.)
        copy = MonsterHarp(hlib)
        copy.serial = self.serial
        copy.devid  = self.devid
        copy.refcnt = self.refcnt
        copy._shadow = self._shadow
        copy.feedback = self.feedback
        copy.refcnt.inc()
        return copy

    
    def __deepcopy__(self):
        return self.__copy__()


    def __str__(self):
        return "HydraHarp[%s]" % (self.serial)


    def __repr__(self):
        return str(self)
    

    def _checkHarpError(self, ret):
        '''
        To simplify error handling: raises an exception if ret < -1.
        '''
        ErrorStringPortal(self.hlib)(ret)
        

    def initialize(self, mode, clock):
        '''
        Wrapper for `HH_Initialize`. Call before any other routines. Parameters:
        - `mode`: See `MeasurementMode`
        - `clock`: `ReferenceClock.Internal` or `ReferenceClock.External`
        Returns `None` on success, or raises 
        '''
        self.hlib.HH_Initialize(self.devid, mode, clock)


    @property
    def hardwareInfo(self):
        '''
        Wrapper for `HH_GetHardwareInfo`. Returns a string tuple of model, partno, version.
        '''
        mod = ctypes.create_string_buffer(b'', 64)
        pno = ctypes.create_string_buffer(b'', 64)
        ver = ctypes.create_string_buffer(b'', 64)
        self.hlib_request('HH_GetHardwareInfo', mod, pno, ver)
        return { "model": mod.value.decode('utf-8'),
                 "part": pno.value.decode('utf-8'),
                 "vesion": ver.value.decode('utf-8') }
    
    
    @property
    def serialNumber(self):
        '''
        Reads out the serial number. Should return the same as `self.serial`, but
        the difference between `self.serial` and this is that `serialNumber` actually
        does query the serial number via the HHLIB API on every call, while `self.serial`
        is the number that was cached when the device was first opened.
        '''
        s = ctypes.create_string_buffer(b'', 64)
        self.hlib_request('HH_GetSerialNumber', s)
        return s.value.decode('utf-8')

    
    @property
    def features(self):
        '''
        Wrapper for `HH_GetFeatures`. Returns a 32-bit bitmask with features.
        See PicoQuant documentation for the meaning of the bits.
        '''
        i = ctypes.c_int()
        self.hlib_request('HH_GetFeatures', ctypes.byref(i))
        m = self._shadow.setdefault('featuresMap', OrthogonalFlagsMap(HarpFeatures))
        m.recode(code=i.value)
        return m

    
    @property
    def baseResolution(self):
        '''
        Wrapper for `HH_GetBaseResolution`. Returns a tuple consisting of
        a floating-point number with resolution in seconds (ACHTUNG, this is
        different from the origina HHLIB API!) and the maximum allowed number
        of binning steps.
        '''

        d = ctypes.c_double()
        i = ctypes.c_int()
        self.hlib_request('HH_GetBaseResolution', ctypes.byref(d), ctypes.byref(i))
        return d.value*1e-12, i.value
    

    @property
    def channels(self):
        ''' Portal for all input channel related attributes '''
        return InputChannelPortal(self)

    
    @property
    def modules(self):
        '''
        (Preparation for) wrapper for `HH_GetModuleInfo`. Returns
        an object that can iterate through module information.
        '''
        return ModuleInfoPortal(self)

    
    @property
    def hardwareDebugInfo(self):
        '''
        Wrapper around `HH_HardwareDebugInfo`. Apparently can be queried if
        HH_ERROR_STATUS_FAIL or FLAG_SYSERROR is encountered.
        Returns a python utf-8 string.
        '''
        s = ctypes.create_string_buffer(b'', 65636)
        self.hlib_request('HH_GetHardwareDebugInfo', s)
        return s.value.decode('utf-8')

    
    def calibrate(self):
        '''
        Wrapper around `HH_Calibrate`. Does something. No return value.
        '''
        self.hlib_request('HH_Calibrate')


    def shadow(self, key, default=None):
        if self._lock:
            with self._lock:
                return self._shadow.get(key) or default
        else:
            return self._shadow.get(key) or default
        

    @property
    def syncDiv(self):
        return self.shadow('syncDiv', None)

    @syncDiv.setter
    def syncDiv(self, val):
        '''
        Wrapper for `HH_SetSyncDiv`. Working with a shadow value for artificial getter.
        '''
        p = ctypes.c_int(val)
        self.hlib_request('HH_SetSyncDiv', p, shadow='syncDiv', value=val)

        
    @property
    def syncCfd(self):
        return self.shadow('syncCfd', None)

    @syncCfd.setter
    def syncCfd(self, data):
        '''
        Wrapper for `HH_SetSyncCfd`. Working with a shadow value for artificial getter.
        `data` is either a tuple `(level, zerox)` or a dict `{"level": ..., "zerox": ...}`.
        ACHTUNG, voltage levels are in V, not mV.
        '''
        if isinstance(data, dict):
            d = data
        else:
            d = dict({"level": data[0], "zerox": data[1]})
        p0 = ctypes.c_int(int(d["level"]*1e3))
        p1 = ctypes.c_int(int(d["zerox"]*1e3))
        self.hlib_request('HH_SetSyncCFD', p0, p1, shadow='syncCfd', value=d)


    @property
    def syncChannelOffset(self):
        return self.shadow('syncChannelOffset', None)

    @syncChannelOffset.setter
    def syncChannelOffset(self, value):
        '''
        Wrapper for `HH_SetSyncChannelOffset`.
        Working with a shadow value for artificial getter.
        '''
        p = ctypes.c_int(int(value*1e12))
        self.hlib_request('HH_SetSyncChannelOffset', p,
                          shadow='syncChannelOffset', value=value)

    @property
    def stopOverflow(self):
        '''
        Returns the stop overflow value from shadow. The value is an integer
        if stop overflow is enabled, `False` if disabled, and `None` if no
        value has yet been set (in which case the device is in an unknown
        state).
        '''
        return self.shadow('stopOverflow', None)

    @stopOverflow.setter
    def stopOverflow(self, value):
        '''
        Wrapper for `HH_SetStopOverflow`. Unlike its C counterpart, this only
        takes one argument: `None` or `False` for disabling stop overflow
        (in which case `HH_SetStopOverflow` will be called with a 0 for its
        `stop_ofl` parameter), or an unsigned integer count at which measurement
        should be stopped in case of overflow.
        '''
        stop_ofl = 0 if not bool(value) else 1
        stop_cnt = 0 if stop_ofl==0 else value
        ret = self.hlib_request('HH_SetStopOverflow', stop_ofl, stop_cnt,
                                shadow='stopOverflow',
                                value=(value if stop_ofl == 1 else False))


    @property
    def binning(self):
        ''' returns last binning value from shadow '''
        return self.shadow('binning', None)

    @binning.setter
    def binning(self, value):
        ''' Wrapper for `HH_SetBinning`, value is base 2. '''
        ret = self.hlib_request('HH_SetBinning', value,
                                shadow='binning', value=value)

    
    @property
    def offset(self):
        ''' returns last offset value from shadow (ACHTUNG, NOT inputChannelOffset!)'''
        return self.shadow('offset', None)
    
    @offset.setter
    def offset(self, value):
        '''
        Wrapper for `HH_SetOffset`. Offset time here is specified
        as floating point in seconds (unlike `HH_SetOffset`
        which is nanoseconds).
        '''
        p = ctypes.c_int(int(value*1e9))
        ret = self.hlib_request('HH_SetOffset', p,
                                shadow='offset', value=value)
        return value


    @property
    def histogramLength(self):
        '''
        Returns histrogram length from feedback cache. ACHTUNG, this
        is not the shadow cache (it acts similarly), it's what the
        device actually transmitted on the last setting.
        '''
        return self.feedback.get('histogramLength', None)

    @histogramLength.setter
    def histogramLength(self, base):
        ''' Wrapper for `HH_SetHistoLen`. '''
        actual = ctypes.c_int()
        ret = self.hlib_request('HH_SetHistoLen', base, byref(actual))
        self.feedback['histogramLength'] = actual.value
        return actual.value

        
    def clearHistogram(self):
        '''
        Wrapper for `HH_ClearHistMem`.
        '''
        ret = self.hlib_request('HH_ClearHistMem')

    @property
    def measurementControl(self):
        ''' returns the measurement control form shadow, or `None` if none was set yet '''
        return self.shadow('measurementControl', None)

    @measurementControl.setter
    def measurementControl(self, data):
        '''meascontrol
        Wrapper for `HH_SetMeasControl`. Working with a shadow value for artificial getter.
        `data` is either a tuple `(ctrl, startedge, stopedge)` or a dict
        `{"control": ..., "startEdge": ..., "stopEdge": ...}`.
        '''
        if isinstance(data, dict):        
           idx = ["control", "startEdge", "stopEdge"]
        else:
           idx = (0, 1, 2)
        
        mc_ctrl = getattr(MeasurementControl, data[idx[0]]) \
                if isinstance(data["control"], str) else data[idx[0]]
                
        [mc_start, mc_stop] = [ getattr(EdgeSelection, data[i]) \
              if isinstance(data[i], str) else data[i] for i in idx[1:] ]
	    
        #print(mc_ctrl, mc_start, mc_stop)
	    
        d = { "control":   mc_ctrl,
              "startEdge": mc_start, 
              "stopEdge":  mc_stop}
              
        logging.debug("Measurement control: %r" % d)

        ret = self.hlib_request('HH_SetMeasControl', mc_ctrl, mc_start, mc_stop,
                                shadow='measurementControl', value=d)

        
    def acquire(self, aqtime):
        '''
        Wrapper for `HH_StartMeas`. ACHTUNG, aquisition time here is in seconds(!).
        '''
        self.aquisitionTime = aqtime
        if self.clearOnAcquire:
            logging.debug("Clearing histogram")
            self.clearHistogram()
        logging.debug("Measurement control: %r" % self.measurementControl)
        v = ctypes.c_int(int(aqtime*1e3))
        self.hlib_request('HH_StartMeas', v)

        
    def acqstop(self):
        '''
        Wrapper for `HH_StopMeas`.
        '''
        self.hlib_request('HH_StopMeas')
        

    @property
    def acquisitionTime(self):
        '''
        Returns the last aquisition time that was set, or a default of 1.0 seconds
        '''
        return self._shadow.setdefault('acquisitionTime', 1.0)


    @acquisitionTime.setter
    def acquisitionTime(self, val):
        self._shadow['acquisitionTime'] = val


    @property
    def acquiring(self):
        '''
        Wrapper for `HH_CTCStatus`. Returns `True` if the aquisition is still running,
        `False` otherwise. Setting this to `False` also stops the current measurement.
        '''
        s = ctypes.c_int()
        self.hlib_request('HH_CTCStatus', byref(s))
        return (s.value == 0)

    @acquiring.setter
    def acquiring(self, enable):
        '''
        If this is set to True, it triggers an acuisition with the last
        acquisition time, or with the default of 1 second. If this is set
        to False, it cancels the current aquisition.
        '''
        if enable:
            if self.acquiring:
                logging.warning("Acquisition already in progress, please stop first")
                return
            t = self.acquisitionTime
            logging.debug("Starting aquisition with %r seconds (enable: %r)" % (t, enable))
            self.acquire(t)
        else:
            logging.debug("Stopping aquisition (requested: %r, running: %r)" \
                          % (enable, self.acquiring))
            self.acqstop()


    @property
    def resolution(self):
        ''' Wrapper for `HH_GetResolution`. Returns the time resolution in seconds (!) '''
        s = ctypes.c_double(-1.0)
        self.hlib_request('HH_GetResolution', byref(s))
        return (s.value * 1e-12)


    @property
    def syncRate(self):
        ''' Wrapper for `HH_GetSyncRate`. '''
        s = ctypes.c_int()
        self.hlib_request('HH_GetSyncRate', byref(s))
        return s.value


    @property
    def syncPeriod(self):
        ''' Wrapper for `HH_GetSyncPeriod`. Returns the sync period in seconds (!). '''
        s = ctypes.c_float()
        self.hlib_request('HH_GetSyncPeriod', byref(s))
        return s.value * 1e-12


    @property
    def warnings(self):
        '''
        Returns the warnings. This is mainly a wrapper for `HH_GetWarnings`, but HHLIB
        documentation states that on all channels `HH_GetCountRate` needs to be called
        for all channels beforehand. Probably also `HH_GetSyncRate`.
        '''
        s = ctypes.c_int()
        cnt = [ c.countRate for c in self.channels ]
        sr = self.syncRate
        self.hlib_request('HH_GetWarnings', byref(s))
        m = self._shadow.setdefault('warningsMap', OrthogonalFlagsMap(HarpWarnings))
        m.recode(s.value)
        return m


    @property
    def flags(self):
        '''
        Returns the flags. This is a wrapper for `HH_GetFlags`.
        '''
        s = ctypes.c_int()
        self.hlib_request('HH_GetFlags', byref(s))
        m = self._shadow.setdefault('flagsMap', OrthogonalFlagsMap(HarpFlags))
        m.recode(s.value)
        return m


    @property
    def markers(self):
        '''
        Returns the markers setup. This is a list of size 4 which holds
        either an `EdgeSelection` object (Rising/Falling), or `None`,
        one for each of the 4 possible markers that a Harp device manages.
        If the entry is `None`, the edge is deactivated.
        The getter returns the last setting from shadow memory, the
        setter is a wrapper for `HH_SetMarkerEdges` / `HH_SetMarkerEnable`.
        If the markers were never set, then the getter returns only `None`
        instead of a list of 4 items (the shadow memory being empty).
        '''
        return self.shadow('markers', None)

    @markers.setter
    def markers(self, status):
        '''
        Sets the edge specification and enables/disables markers.
        The parameter `status` is an enumerable (list, tuple, array)
        with exactly 4 items. Each of the items must be either
        an `EdgeSelection` object, or the keyword `None`.
        If the item is `None`, the marker is deactivated.
        '''
        edges = [ ctypes.c_int(1 if s==EdgeSelection.Rising else 0) for s in status ]
        enablers = [ ctypes.c_int(1 if s is not None else 0) for s in status ]
        self.hlib_request('HH_SetMarkerEdges', *edges),
        self.hlib_request('HH_SetMarkerEnable', *enablers)


    @property
    def markerHoldoffTime(self):
        ''' returns the last markerHoldoffTime from shadow '''
        return self.shadow('markerHoldoffTime', None)
        
    @markerHoldoffTime.setter
    def markerHoldoffTime(self, t):
        '''
        Wrapper for `HH_SetMarkerHoldoffTime`. `t` is time in nanoseconds (integer).
        '''
        s = ctypes.c_int(t)
        self.hlib_request('HH_SetMarkerHoldoffTime', s)


    @property
    def fifo(self):
        '''
        Returns the FIFO contents as much as they are available as
        a numpy array (typically it's a multiple of 128 items).
        This is a wrapper for `HH_ReadFiFo`.
        '''
        nummax = ctypes.c_int(DeviceLimits.MaxFifoReadout)
        numread = ctypes.c_int()
        rbuf = (ctypes.c_int*nummax)()
        self.hlib_request('HH_ReadFiFo', rbuf, nummax, byref(numread))
        return as_array(rbuf)[:numread.value]
        

class Monster(object):
    '''
    Wrapper around PicoQuant's HydraHarp C library, typically called hhlib.so
    on Linux systems.

    This package does *not* distribute any code, Imaginary or Inelectual
    Property of PicoQuant GmbH -- for that, check their GitHub pages
    (specifically that of the
    [HydraHarp 400](https://github.com/PicoQuant/HH400-v3.x-Demos)). You
    will need to download the binaries yourself for this to work,
    and set the `MINIQUANT_HHLIB` enviromnet variable to the
    name, preferrably including full path, of PicoQuant's proprietary
    binary.

    This is a Singleton, by default initialized on `import ...` using the
    ``harp.monster_library` shared object path (which in turn is
    extracted from `MINIQUANT_HHLIB`). If the default initialization
    fails, it does so silently. The most likely reason is that the
    correct HH-library wasn't found or couldn't be loaded.
    Then the user has to initialize the class at least once
    correctly and explicitly pass that instance to any `MonsterHarp`
    initializations, e.g.:
    ```
    # library loading triggers Monster initialisation from env-var
    from harp import Monster, MonsterHarp

    # scenario 1a: implicit intialisation worked; open a harp now
    # by passing an explicit ID to Monsterharp
    h = MonsterHarp(0)

    # scenario 1b: implicit initialization worked; find a harp
    # by obtaining a copy of the Monster singleton first
    mcopy = Monster()
    h = mcopy.find("any")

    # scenario 2a: implicit initialisation failed; re-initialise
    # the HH-lib implicitly and open a harp by creating a Harp object
    m = Monster(library="/path/to/real/hhlib.so")
    h = MonsterHarp(0, hlib=m.hlib)

    # scenario 2b: ...or find a harp by using the singleton
    h = m.find("any")
    ```

    In each of the examples above there is always only one `Monster`
    instance alive.
    '''

    def __new__(self, *args, **kwargs):
        # Make a singleton
        if not hasattr(self, 'instance'):
            self.instance = super(Monster, self).__new__(self)            
        return self.instance
    

    def __init__(self, library=None):
        '''
        Initializes the library / Harp access system. This is just
        a precursor to using the Harp.

        To actually start connecting to one of the devices, see
        `connect()`.
        '''

        lib = env.get('MINIQUANT_HHLIB', "hhlib.so")
        if not hasattr(self, 'hlib'):
            try:
               l = library or lib
               self.hlib = ctypes.CDLL(l, use_errno=True)
            except OSError:
                logging.error("Error opening: %r" % l)
                raise


    def find(self, *serials, maxdev=8):
        '''
        Returns a `MonsterHarp` object (or a list of objects)
        which can be used to talk to one specific PicoQuant
        HydraHarp device.

        Parameters:
          - `serials`: This a list of strings,
             or one of the special values `None`, `all`, or `first`.
        
            If this is a string, the HydraHarp device with
            the given serial number will be opened and a corresponding
            `MonsterHarp` object is returned.

            If this is a list of strings, then a map will be returned --
            one for each device that was found and that has a serial
            number that matches any of the strings in the list.

            If the value is `None` or `"first"`, then the first device
            that will be found is returned.

            If it is `"all"`, then a dictionary with all devices
            (serials as keys) is returned.

            The device serial numbers are all supposed to be strings.

          - `maxdev`: The maximum number of devices to try opening.
            8 is a hardcoded value in the PicoQuant's library. There's
            no harm in trying higher numbers, but it most likely won't
            have any effect.

        Returns:
          - a single `MonsterHarp` object if a single serial number,
            or `serial="any"` was requested and found.
          - a dictionary of `MonsterHarp` objects if more than one
            serial number was requested and found, or `serial="all"`
            was requested.
          - an empty list if no device was specifically requested (e.g.
            the call was `serial="all"`), but several were expected,
            and none were found.
          - raises `ValueError` (i.e. does not return) any of the
            devices specifically requested by string isn't found.
        '''

        devs = {}
        
        for i in range(maxdev):
            try:
                harp = MonsterHarp(i, self.hlib)
                
            except OSError as e:
                if e.errno == errno.EAGAIN:
                    continue
                
                raise
            
            if (harp.serial in serials) or \
               ("first" in serials) or \
               ("any" in serials) or \
               (len(serials) == 0):
                return harp

            if (harp.serial in serials) or ("all" in serials):
                devs[harp.serial] = harp
                continue

            # don't want it, ID doesn't match list
            del harp
            
        if ((len(serials) == 1) and (serials[0] != "all")) or (len(serials) == 0):
            # excatly one Harp requested, but none found.
            raise OSError(errno.ENXIO, "No Harp device attached")

        return devs
            
        

    @property
    def libraryVersion(self):
        '''
        Wrapper for `HH_GetLibraryVersion()`. Returns a string with the
        version of the binary library being used.
        '''
        buf = ctypes.create_string_buffer(b'', 128)
        self.hlib.HH_GetLibraryVersion(buf)
        return buf.value.decode('utf-8')

    
    @property
    def errorString(self):
        '''
        Wrapper for `HH_GetErrorString()`. Returns a string version
        of the specified error code. The string is essentially just
        the name of the error code itself, it presents zero value
        beyond what's already in PicoQuant's header files.
        '''
        return ErrorStringPortal(self.hlib)



# Path to the hhlib.so
monster_library = env.get('MINIQUANT_HHLIB', "hhlib.so")

# ctypes.CDLL binding to the library pointed to by
# the MINIQUANT_HARP_LIBRARY environment variable.
try:
    monster_binding = Monster(monster_library)
except:
    monster_binding = None
