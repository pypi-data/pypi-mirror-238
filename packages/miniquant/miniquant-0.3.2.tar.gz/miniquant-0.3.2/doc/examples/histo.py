#!/usr/bin/python3

import miniquant.harp as harp
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import time
import sys

def harp_init():
    '''
    Initialises Harp for a 1.25 MHz device
    '''
    hdev = harp.Monster().find()
    hdev.initialize(harp.MeasurementMode.Histogramming,
                    harp.ReferenceClock.Internal)

    hdev.calibrate()

    hdev.syncDivider = 1
    hdev.syncCfd = { "level": 0.200, "zerox": 0.01 }
    hdev.syncChannelOffset = 0

    ch = hdev.channels[0]
    ch.cfd = { "level": 0.300, "zerox": 0.01 }
    ch.offset = 0
    ch.enable = True

    hdev.histogramLength = 6
    hdev.binning = 0
    hdev.offset = 0

    return hdev


def harp_info_header(hdev):
    '''
    Prints a bunch of informative stuff.
    '''
    
    print ("Histogram length:", hdev.histogramLength)
    print ("Base resolution:", hdev.baseResolution)
    print ("Real resolution:", hdev.resolution)
    print ("Sync rate:", hdev.syncRate)
    print ("Count rates:", [ch.countRate for ch in hdev.channels])
    print ("Warnings:", [ w for w in hdev.warnings] )
    print ("Flags:", [ f for f in hdev.flags] )
    

def mpl_histo_loop(hdev, fig, aqtime=0.1, axis_index=0, line_index=0, channel=0):
    '''
    Loops endlessly reading histogram and displaying it into the
    specified Matplotlib plot, while also serving the GUI event loop.
    '''
    
    print("Starting plotting interface")
    ax = fig.axes[axis_index] if len(fig.axes)>0 \
        else fig.add_subplot(1, 1, 1)
    
    ax.set_xlim(0, hdev.histogramLength)

    line = ax.lines[line_index] if len(ax.lines)>0 \
        else ax.plot([])[0]

    text  = ax.text(10, 0.0, "Jinkies")

    fig.show(False)

    ch = hdev.channels[channel]

    # For auto-scaling
    xlen = 0
    ymax = 0
    t0 = time.time()

    print("Entering histogram loop, %.5f seconds acquisition time" % aqtime)
    while True:

        hdev.acquire(aqtime)
        while hdev.acquiring:
            fig.canvas.flush_events()
        hdev.acqstop()
    
        data = ch.histogram
    
        if len(data) != xlen:
            xlen = len(data)
            x = np.array(range(xlen))

        ## Some random noise, for testing
        #data[np.random.randint(len(x))] = np.random.randint(100)        

        dmax = data.max()
        if ymax < dmax:
            print ("Adjusting Y range")
            ymax = dmax
            ax.set_ylim(-1, dmax+1)

        tnow = time.time()
        text.set_text("aq: %2.0f Hz | flags: %r | counts: %d" % \
                      (1.0/(tnow-t0),
                       [f for f in hdev.flags],
                       data.sum()))
        t0 = tnow
    
        line.set_data(x, data)
        fig.canvas.draw_idle()
        fig.canvas.flush_events()

    
if __name__ == "__main__":

    print("Initializing device")
    hdev = harp_init()

    time.sleep(0.5)
    harp_info_header(hdev)

    fig = plt.figure()
    
    mpl_histo_loop(hdev, fig)
