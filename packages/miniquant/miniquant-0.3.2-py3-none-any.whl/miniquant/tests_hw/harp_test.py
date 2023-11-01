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

#
# Unit-testing -- it is expected to have a Harp device attached if this
# is to succeed.
#

import pytest
from os import environ as env

if 'MINIQUANT_TEST' in env and env['MINIQUANT_TEST'] != 0:
    from miniquant import mock_harp as harp
else:
    from miniquant import harp

def test_library():
    ##    Finding / initializing the HH-library and singleton wrapper

    if harp.monster_binding is not None:
        
        # This should deliver a valid m, which is the same as monster_library        
        m = harp.Monster()
        assert (m is harp.monster_binding)

        assert len(m.libraryVersion) > 1
        
    else:
        
        # this is the same as default initialisation -- it should fail
        with pytest.raises(Exception):
            m = harp.Monster()

        # special env-var for testing with the *real* location of the library :-)
        if env.get("TEST_MINIQUANT_HHLIB"):
            m = harp.Monster(env.get("TEST_MINIQUANT_HHLIB"))

            assert (m.hlib is not None)

            assert len(m.libraryVersion) > 1


def test_findharp():
    ## Finding a harp device

    m = harp.Monster()
    h = m.find("first")
    assert (h is not None)

    h2 = m.find(h.serial)
    assert (h2.serial == h.serial)

    ## FIXME: at this point we've opened a device twice (h.serial)
    ## What does happen if we closed one? What is supposed to happen?!...
    ## need to test thath.
    

def test_notfindharp():
    mon = harp.Monster()
    with pytest.raises(OSError):
        h3 = mon.find("unlikely")

        
def test_findall():
    h4 = harp.Monster().find("all")
    assert(len(h4) > 0)

@pytest.fixture
def harp_device():
    h = harp.Monster().find('any')

    print ("Initializing Harp No.", h.serial, "...")
    h.initialize(harp.MeasurementMode.Continuous,
                 harp.ReferenceClock.Internal)
    print ("Initialization finished.")
    
    return h

def test_api_getters(harp_device):
    '''
    Tests all kinds of API "HH_Get..." wrappers.
    '''

    hi = harp_device.hardwareInfo
    print ("Hardware Info:", hi)
    assert (len(hi) == 3)

    sn = harp_device.serialNumber
    print ("Serial Number:", sn)
    assert (sn == harp_device.serial)

    ft = harp_device.features
    print ("Features: ")
    [ print("  -", f) for f in ft ]
    
    res = harp_device.baseResolution
    print ("Base Resolution:", res)
    assert (len(res) == 2)

    mods = harp_device.modules
    assert (len(mods) > 0)
    print ("Installed Modules:", len(mods))
    print ("Module Info:")
    [ print ("  -", m.info) for m in mods ]

    ichs = harp_device.channels
    assert (len(ichs) > 0) ## only true for the HydraHarp
    print ("Installed Input Channels:", len(ichs))
    print ("Channel info:")
    [ print("  - module index:", c.moduleIndex,
            "\n    enabled:", c.enabled,
            "\n    offset:", c.offset,
            "\n    cfd:", c.cfd,
            "\n    count rate:", c.countRate) for c in ichs ]

    flg = harp_device.flags
    print("Flags:")
    [ print("  -", f) for f in flg ]

    wrn = harp_device.warnings
    print("Warnings:")
    [ print("  -", w) for w in wrn ]

    hdbg = harp_device.hardwareDebugInfo
    print ("H/W Debug Info: \n---cut-here---")
    print (hdbg, "\n---/cut-here---")

    print ("Sync channel:")
    print ("  - div:", harp_device.syncDiv)
    print ("  - cfd:", harp_device.syncCfd)
    print ("  - offset:", harp_device.syncChannelOffset)
    print ("  - rate:", harp_device.syncRate)
    print ("  - period:", harp_device.syncPeriod)


def test_orthoflags():
    # checks whether the orthogonal flags class works
    wrn = harp.OrthogonalFlagsMap(0x441, harp.HarpWarnings)
    flg = harp.OrthogonalFlagsMap(0x441, harp.HarpFlags)
    assert len(wrn) == 3
    assert len(flg) == 1
    assert flg.OVERFLOW == True
    assert flg.FIFOFULL == False
    assert isinstance(flg.text('OVERFLOW'), str)
    assert type(flg.mask('OVERFLOW')) == int


def test_dostuff(harp_device):

    # Do stuff.
    harp_device.calibrate()

    # do stuff with channels
    print ("Testing input channel writing...")
    for c in harp_device.channels:
        c.enabled = True
        assert (c.enabled)

        c.offset = 5e-12
        assert (c.offset < 7e-12)

        c.cfd = (0, 0)
        assert len(c.cfd) == 2

        c.enabled = False

    harp_device.syncDiv = 1
    assert harp_device.syncDiv == 1

    harp_device.syncCfd = (1, 0)
    assert harp_device.syncCfd['level'] == 1

    harp_device.syncChannelOffset = 3e-9
    assert harp_device.syncChannelOffset < 5e-9

    harp_device.stopOverflow = 2000
    assert harp_device.stopOverflow == 2000

    harp_device.binning = 1
    assert harp_device.binning == 1

    harp_device.offset = 35e-9
    assert harp_device.offset < 50e-9

    with pytest.raises(harp.HarpError):
        # This is likely to fail because of invalid parameter
        # (histrogramm mode inactive / not properly set up)
        harp_device.histogramLength = 1024
        
    harp_device.clearHistogram()
    print ("Histrogram length:", harp_device.histogramLength)
    assert harp_device.histogramLength is None

    assert type(harp_device.acquiring) == bool

    ## The histogram / acquisition stuff is a bit of a mess, since
    ## for this the device would actually have to be properly set
    ## up and produce data. But since this is just a general s/w unit
    ## testing, we don't know in which state the device, and how it's
    ## behaving, which signals it's attached to etc. So we're just
    ## going to go through some of the motions to make sure the code
    ## doesn't crash, but we don't make any assertions / assumptions
    ## about what it'll result into.
    if harp_device.acquiring:
        print ("Stopping acquisition")
        harp_device.acquiring = False
    else:
        print ("Starting acquisition")
        harp_device.acquiring = True
    print ("Acquiring:", harp_device.acquiring)        

    # setMeasurementcontrolControl() / setMeasControl
    # getHistData etc

    
def test_close():
    ## What happens when closing?
    pass
