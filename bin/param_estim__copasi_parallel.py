#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# License (GPLv3):
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
#
# Institute for Ageing and Health
# Newcastle University
# Newcastle upon Tyne
# NE4 5PL
# UK
# Tel: +44 (0)191 248 1106
# Fax: +44 (0)191 248 1101
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2010-07-13 12:14:32 $
# $Id: latex_report.py,v 1.0 2010-07-13 12:45:32 Piero Dalle Pezze Exp $
#
# Desc: This program runs parallel estimation computations with pp module 


###############################################################
# You can put this into a script and run it on server side..
# on server side (here: 127.0.0.1), start:
# ppserver.py -p 65000 -i 127.0.0.1 -s -w 5 "donald_duck" &
#
# NB: -w is the number of core YOU can use. If a server is used by more users, 
# set the number lower than the number of cpus
#
# Command line options, ppserver.py
# Usage: ppserver.py [-hda] [-i interface] [-b broadcast] [-p port] [-w nworkers] [-s secret] [-t seconds]
# Options:
# -h                 : this help message
# -d                 : debug
# -a                 : enable auto-discovery service
# -i interface       : interface to listen
# -b broadcast       : broadcast address for auto-discovery service
# -p port            : port to listen
# -w nworkers        : number of workers to start
# -s secret          : secret for authentication
# -t seconds         : timeout to exit if no connections with clients exist
###############################################################



# execute: python run_parallel_param_estim.py [path] [model_pattern] [ncalib] [ncpus]

# On client side, run this program

import math, time
import shutil
import shlex
import subprocess
import sys
import os
SB_PIPE_LIB = os.environ["SB_PIPE_LIB"]
sys.path.append(SB_PIPE_LIB + "/python/")

from SyncCounter import *

# apt-get install python-pp
import pp



# Run a Copasi instance
def run_copasi_instance(filename):
  # Command output=`CopasiSE -s filename filename`
  p1 = subprocess.Popen(["CopasiSE", "-s", filename, filename], stdout=subprocess.PIPE) 
  p1.subprocess.communicate()[0]


# Run parallel instances of Copasi
def run_parallel_copasi(server, args=("","", 1), callback=SyncCounter()):
    (path, model, ncalib) = args
    callbackargs = ()
    filename = ""
    start_time = time.time()
    for index in range(0, ncalib):
        # Submit a Copasi Job
        # callback (SyncCounter.add) - callback function
        callbackargs = (int(index + 1),)
        filename = path + "/" + model + str(index + 1) + ".cps"
        server.submit(run_copasi_instance,(filename,),depfuncs=(Popen,comunicate,),modules=(shlex,subprocess,),callback=callback.add,callbackargs=callbackargs,group="my_processes")
        print("Process P" + str(index) + " started")


# The Main Function
def main(args):
    print("""Usage: python run_parallel_param_estim.py [path] [model_pattern] [ncalib] [ncpus]
	  [path]   - the path of the models
	  [model]  - the model name pattern
	  [ncalib] - the number of calibration to perform
          [ncpus]  - the number of workers to run in parallel, 
          """)
    ### ppserver configuration
    # tuple of all parallel python servers to connect with
    # server tuple
    #ppservers=("127.0.0.1:65000",)
    ppservers=("cisban-node1.ncl.ac.uk:65000","cisban-node2.ncl.ac.uk:65000","cisban-node3.ncl.ac.uk:65000",)
    # a passkey
    secret='donald_duck'
    
    # The path of the models
    path = args[1]
    # Them model name pattern
    model = args[2]
    # The number of calibration to perform
    ncalib = int(args[3])
    # The number of available cpus
    # number of cpus to use IN THE LOCALHOST!
    # IMPORTANT: set ncpus to 0 if all the processes have to run on a server!
    ncpus = int(args[4])
    
    # Create an instance of callback class
    callback = SyncCounter()
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus=ncpus, ppservers=ppservers, secret=secret)
    print("Initialised python_pp with " + str(job_server.get_ncpus()) + " workers.\n")        

    print("\nComputing Parallel Parameter Estimation using Copasi\n")
    run_parallel_copasi(server=job_server, args=(path, model, ncalib), callback=callback)        
    # Wait for jobs in all groups to finish 
    job_server.wait(group="my_processes")

    # print statistics
    job_server.print_stats()
    job_server.destroy()



main(sys.argv)