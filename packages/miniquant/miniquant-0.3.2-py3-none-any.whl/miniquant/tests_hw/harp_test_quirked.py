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
# Unit-testing the Harp classes with a quirked or unplugged USB
# (i.e. mainly testing for correct error handling / reporting).
#

import pytest

from miniquant import harp

def test_openfail():
    # Fails opening with specific errors, depending on
    # whether unplugged or quirked.

    mon = harp.Monster()
    with pytest.raises(OSError) as e:
        h3 = mon.find()
