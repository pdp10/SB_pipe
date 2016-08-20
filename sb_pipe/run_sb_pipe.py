#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Object: sb_pipe main 
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-27 10:18:32 $

# NOTE: 
# don't name this file: __init__.py or sb_pipe.py . 
# They both cause a conflict when these are invoked from the tests

import os
import sys
import getopt

import logging
from logging.config import fileConfig

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "create_project"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "simulate"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "param_estim"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "single_param_scan"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "double_param_scan"))
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "pipelines", "sensitivity"))

# pipelines
from create_project import CreateProject
from simulate import Simulate
from param_estim import ParamEstim
from single_param_scan import SingleParamScan
from double_param_scan import DoubleParamScan
from sensitivity import Sensitivity


def get_sb_pipe_logo():
    """
  	Return sb_pipe logo.

  	:return: sb_pipe logo
  	"""
    logo = (
            "\n"
            "                            _             \n"
            "          /\               (_)            \n"
            "    ___  / /_        ____    ____  ___    \n"
            "   / __\/ __ \      / __ \/\/ __ \/ _ \   \n"
            "  _\ \_/ /_/ /     / /_/ / / /_/ /  __/   \n"
            " \____/\____/     / ____/_/ ____/\____/   \n"
            "            -----/ /     / /              \n"
            "                /_/     /_/               \n"
            )
    return logo


def get_sb_pipe_help():
    """
    Return help message.

    :return: the help message
    """
    message = (
               "Usage: run_sb_pipe.py [OPTION] [FILE]\n"
               "Pipelines for systems modelling of biological networks.\n\n"
               "List of mandatory options:\n"
               "\t-h, --help\n\t\tShows this help.\n"
               "\t-c, --create-project\n\t\tCreate a project structure using the argument as name.\n"
               "\t-s, --simulate\n\t\tSimulate a model.\n"
               "\t-p, --single-param-scan\n\t\tSimulate a single parameter scan.\n"
               "\t-d, --double-param-scan\n\t\tSimulate a double parameter scan.\n"
               "\t-e, --param-estim\n\t\tGenerate a parameter fit sequence.\n"
               "\t-n, --sensitivity\n\t\tRun a sensitivity analysis (in progress).\n\n"
               "Exit status:\n"
               " 0  if OK,\n"
               " 1  if minor problems (e.g., a pipeline did not execute correctly),\n"
               " 2  if serious trouble (e.g., cannot access command-line argument).\n\n"
               "Report bugs to sb_pipe@googlegroups.com\n"
               "sb_pipe home page: <https://pdp10.github.io/sb_pipe>\n"
               "For complete documentation, see README.md .\n"
              )
    return message


def read_file_header(filename):
    """
    Read the first line of a file

    :param filename: the file name to read
    :return: the first line
    """
    line = ""
    with open(os.path.join(SB_PIPE, filename)) as file:
        line = file.readline().strip() + " " + file.readline().strip()
    return line


def check_args(args, msg):
    """
    Check that at least one argument is passed.

    :param args: the list of arguments
    :param msg: the message to print
    :raise: Usage exception if less than one argument is passed
    :return: no output
    """
    if len(args) < 1:
        raise (Usage(msg))


class Usage(Exception):
    """
    This class is used for printing a generic exception
    """

    def __init__(self, msg):
        """
        Constructor

        :param msg: the message to print
        """
        self.msg = msg


def main(argv=None):
    """
    The main launcher for sb_pipe.
    """

    if argv is None:
        argv = sys.argv

    # logging settings
    home = os.path.expanduser("~")
    if not os.path.exists(os.path.join(home, '.sb_pipe', 'logs')):
        os.makedirs(os.path.join(home, '.sb_pipe', 'logs'))
    # disable_existing_loggers=False to enable logging for Python third-party packages
    fileConfig(os.path.join(SB_PIPE, 'logging_config.ini'),
               defaults={'logfilename': os.path.join(home, '.sb_pipe', 'logs', 'sb_pipe.log')},
               disable_existing_loggers=False)
    logger = logging.getLogger('sbpipe')

    exit_status = 0
    no_conf_file_msg = "no configuration file received"
    no_project_name_msg = "no project name received"

    try:
        try:
            opts, args = getopt.getopt(argv[1:],
                                       "hcspenlv",
                                       ["help",
                                        "create-project",
                                        "simulate",
                                        "single-param-scan",
                                        "double-param-scan",
                                        "param-estim",
                                        "sensitivity",
                                        "license",
                                        "version"
                                        ])

            for opt, arg in opts:

                if opt in ("-h", "--help"):
                    print(get_sb_pipe_help())

                elif opt in ("-l", "--license"):
                    print(read_file_header("LICENSE"))

                elif opt in ("-v", "--version"):
                    print(read_file_header("VERSION"))

                elif opt in ("-c", "--create-project"):
                    check_args(args, no_project_name_msg)
                    cp = CreateProject()
                    exit_status = cp.run(args[0])

                elif opt in ("-s", "--simulate"):
                    check_args(args, no_conf_file_msg)
                    print(get_sb_pipe_logo())
                    s = Simulate()
                    exit_status = s.run(args[0])

                elif opt in ("-p", "--single-param-scan"):
                    check_args(args, no_conf_file_msg)
                    print(get_sb_pipe_logo())
                    sps = SingleParamScan()
                    exit_status = sps.run(args[0])

                elif opt in ("-d", "--double-param-scan"):
                    check_args(args, no_conf_file_msg)
                    print(get_sb_pipe_logo())
                    dps = DoubleParamScan()
                    exit_status = dps.run(args[0])

                elif opt in ("-e", "--param-estim"):
                    check_args(args, no_conf_file_msg)
                    print(get_sb_pipe_logo())
                    pe = ParamEstim()
                    exit_status = pe.run(args[0])

                elif opt in ("-n", "--sensitivity"):
                    check_args(args, no_conf_file_msg)
                    print(get_sb_pipe_logo())
                    print("not yet available. Apologise.")
                    exit_status = 0
                    s = Sensitivity()
                # exit_status = s.run(args[0])

            if len(opts) < 1:
                raise Usage("no option received")

        except getopt.error, msg:
            raise Usage(msg)

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use -h, --help"
        exit_status = 2

    return exit_status


if __name__ == "__main__":
    sys.exit(main())
