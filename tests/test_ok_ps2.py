#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sbpipe.
#
# sbpipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sbpipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sbpipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: run a list of tests for the insulin receptor model.
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-01-21 10:36:32 $

import os
import sys
import unittest

SBPIPE = os.environ["SBPIPE"]
sys.path.append(SBPIPE)
from sbpipe import main as sbmain


class TestCopasiPS2(unittest.TestCase):

    _orig_wd = os.getcwd()  # remember our original working directory
    _ir_folder = os.path.join('insulin_receptor')

    @classmethod
    def setUp(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._ir_folder))

    @classmethod
    def tearDown(cls):
        os.chdir(os.path.join(SBPIPE, 'tests', cls._orig_wd))

    def test_ps2_inhib_only(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib.yaml"), 0)

    def test_stoch_ps2_inhib_only(self):
        self.assertEqual(sbmain.sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_stoch_inhib.yaml"), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)