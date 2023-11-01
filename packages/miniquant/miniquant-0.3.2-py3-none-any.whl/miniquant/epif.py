#!/usr/bin/python3

try:
    from . import harp
except:
    import harp

from softioc import softioc, builder, asyncio_dispatcher
import asyncio

import sys, time

import numpy as np

def init_harp():
    dev = harp.Monster().find("first")

    print ("Initializing Harp device", dev.serial)
    dev.initialize(harp.MeasurementMode.Histogramming,
                   harp.ReferenceClock.Internal)

    dev.calibrate()

    dev.syncDivider = 1
    dev.syncCfd = { "level": 0.300, "zerox": 0.04 }
    dev.syncChannelOffset = 0

    ch = dev.channels[0]
    ch.cfd = { "level": 0.300, "zerox": 0.04 }
    ch.offset = 0
    ch.enable = True

    dev.histogramLength = 3
    dev.binning = 13
    dev.offset = 0

    return dev

def harp_info_header(hdev):
    '''
    Prints a bunch of informative stuff.
    '''
    
    print ("Histogram length:", hdev.histogramLength)
    print ("Base resolution:", hdev.baseResolution)
    print ("Real resolution:", hdev.resolution)
    print ("Histogram delta:", hdev.baseResolution[0]*(2**hdev.binning))
    print ("Histogram reach:", hdev.resolution*hdev.histogramLength)
    print ("Sync rate:", hdev.syncRate)
    print ("Count rates:", [ch.countRate for ch in hdev.channels])
    print ("Warnings:", [ w for w in hdev.warnings] )
    print ("Flags:", [ f for f in hdev.flags] )



    

async def update_iocvars():
    while True:
        #ai.set(ai.get() + 1)
        await asyncio.sleep(1)

        
class HarpSettings(object):
    '''
    Need this to provide some callbacks for variables set via EPICS.
    '''
    def __init__(self, dev):
        self.aqfrequency = 1.0 # in Hz
        self.histogramDelta = dev.resolution
        self.histogramOffset = 0.0
        self.histogramReach = self.histogramDelta * dev.histogramLength

    def setAquisitionFrequency(self, v):
        print ("New acquisition time:", 1.0/v, "seconds")
        self.aqfrequency = v
        
        
if __name__ == "__main__":
    
    dev = init_harp()
    harp_info_header(dev)

    devSettings = HarpSettings(dev)

    dispatcher = asyncio_dispatcher.AsyncioDispatcher()
    builder.SetDeviceName("KMC3XPP_RINGSYNC")

    # some records
    # "input" and "output" are from the client's point of view,
    # i.e. an "output" record is one where the client would send
    # a value to a device.

    # Aquisition time for the Harp device
    aqFrequencySetHz = builder.aOut("aqfrequency_sethz", initial_value=10.0, always_update=True,
                                    on_update=devSettings.setAquisitionFrequency)
    aqFrequency   = builder.aIn("aqfrequency")
    devResolution = builder.aIn("resolution", initial_value=dev.resolution)
    devSyncPeriod = builder.aIn("syncPeriod", initial_value=dev.syncPeriod)
    devSyncRate   = builder.aIn("syncRate",   initial_value=dev.syncRate)
    devWarnings   = builder.stringIn("warnings", initial_value="")
    devFlags      = builder.stringIn("flags", initial_value="")
    
    # Signal / waveform
    axis = np.array([devSettings.histogramOffset + i*devSettings.histogramDelta for i in range(dev.histogramLength)])
    ch0Signal    = builder.Waveform("ch0_signal", length=dev.histogramLength, datatype=float)
    ch0XAxis     = builder.Waveform("ch0_xaxis", length=dev.histogramLength)
    ch0XAxis.set(axis)
    ch0XOffset   = builder.aIn("ch0_xoffset", initial_value=devSettings.histogramOffset)
    ch0XDelta    = builder.aIn("ch0_xdelta", initial_value=devSettings.histogramDelta)
    ch0XReach    = builder.aIn("ch0_xreach", initial_value=devSettings.histogramReach)
    ch0CountRate = builder.aIn("ch0_countrate")
    ch0Peaktime  = builder.aIn("ch0_peaktime")
    

    builder.LoadDatabase()
    softioc.iocInit(dispatcher)

    dispatcher(update_iocvars)

    ch = dev.channels[0]
    t0 = time.time()
    
    while True:
        dev.acquire(1.0/devSettings.aqfrequency)
        while dev.acquiring:
            time.sleep(1.0/devSettings.aqfrequency * 0.01)
        dev.acqstop()
    
        data = ch.histogram
        #data = np.random.rand(*(ch.histogram.shape))
        
        ch0Signal.set(data)
        ch0Peaktime.set(devSettings.histogramOffset+data.argmax()*devSettings.histogramDelta)
        ch0CountRate.set(ch.countRate)
        
        devSyncPeriod.set(dev.syncPeriod)
        devSyncPeriod.set(dev.syncRate)
        devResolution.set(dev.resolution)

        devWarnings.set(" ".join([ w for w in dev.warnings]))
        devFlags.set(" ".join([ f for f in dev.flags]))
    
        tnow = time.time()
        aqFrequency.set(1.0/(tnow-t0))
        t0 = tnow
