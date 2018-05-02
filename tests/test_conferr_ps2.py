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


import os
import sys
import unittest
import subprocess
from tests.context import sbpipe


class TestCopasiPS2(unittest.TestCase):

    _orig_wd = os.getcwd()
    _ir_folder = 'config_errors'
    _output = 'OK'

    @classmethod
    def setUpClass(cls):
        os.chdir(cls._ir_folder)
        try:
            subprocess.Popen(['CopasiSE'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()[0]
        except OSError as e:
            cls._output = 'CopasiSE not found: SKIP ... '

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls._orig_wd)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # skip this test because it is:
    # 0, if the optional Python binding code for COPASI is not found,
    # 1, otherwise
    #def test_ps2_inhib_only1(self):
    #    if self._output == 'OK':
    #        self.assertEqual(
    #           sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib1.yaml", quiet=True), 1)
    #    else:
    #        sys.stdout.write(self._output)
    #        sys.stdout.flush()

    def test_ps2_inhib_only2(self):
        if self._output == 'OK':
            self.assertEqual(
                sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib2.yaml", quiet=True), 0)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()

    def test_ps2_inhib_only3(self):
        if self._output == 'OK':
            self.assertEqual(
                sbpipe(parameter_scan2="ir_model_insulin_ir_beta_dbl_inhib3.yaml", quiet=True), 1)
        else:
            sys.stdout.write(self._output)
            sys.stdout.flush()


if __name__ == '__main__':
    unittest.main(verbosity=2)
