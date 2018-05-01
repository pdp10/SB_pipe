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
import re
from itertools import islice
import shutil
import argparse
import logging
logger = logging.getLogger('sbpipe')

# retrieve SBpipe package path
SBPIPE = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
sys.path.insert(0, SBPIPE)
from sbpipe.simul.copasi import copasi as copasi_simul
from sbpipe.simul import pl_simul


def generic_postproc(infile, outfile, copasi=True):
    """
    Perform post processing file editing for the `simulate` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    shutil.copy(infile, outfile)
    if copasi:
        simulator = copasi_simul.Copasi()
    else:
        simulator = pl_simul.PLSimul()
    simulator.replace_str_in_report(outfile)

    logger.debug(outfile)


def sim_postproc(infile, outfile, copasi=True):
    """
    Perform post processing file editing for the `simulate` pipeline

    :param infile: the model to process
    :param outfile: the directory to store the results
    :param copasi: True if the model is a Copasi model
    """
    generic_postproc(infile, outfile, copasi)

