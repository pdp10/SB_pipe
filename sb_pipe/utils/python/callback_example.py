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
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2015-07-13 12:14:32 $
#
# Desc: This program demonstrates parallel computations with pp module 
# using callbacks (available since pp 1.3).
# It calculates the succession S: 1 - 1/2 + 1/3 - 1/4 + 1/5 - 1/6 +... (lim(S) = ln(2))


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



# execute 
# python callback.py "NumberOfCores"

# On client side, run this program

import math
import time
import thread
import sys

# apt-get install python-pp
import pp

# For high precision float (slow)
# apt-get install python-gmpy python-mpmath
# wget http://pypi.python.org/packages/source/b/bigfloat/bigfloat-0.1.1.tar.gz
# sudo python setup.py install
# from bigfloat import *



# Class for collecting temporary results of the partial sums. 
# This class is used for callbacks by the parallel algorithm.
class Sum:
  
    _value = 0.0
    _count = 0
    
    # class constructor
    def __init__(self):
        self._value = 0.0
        self.lock = thread.allocate_lock()
        self._count = 0
    
    # the callback function
    # Note: pid is callbackargs passed to submit
    # value is the return value of the function part_sum (which is parallelised), 
    # so it is the callback value.
    def add(self, pid, value):
        # we must use lock here because += is not atomic
        self.lock.acquire()
        self._count = self._count + 1
        self._value = self._value + value
        self.lock.release()
        print("Process P" + str(pid) + " completed")
    
    # get methods
    def get_value(self):
        temp = 0.0
        self.lock.acquire()
        temp = self._value
        self.lock.release()
        return temp
   
   def get_count(self):
        temp = 0.0
        self.lock.acquire()
        temp = self._count
        self.lock.release()
        return temp



# Function to parallelize
"""Calculates partial sum"""
def part_sum(start, end):
    sum = 0
    for x in xrange(start, end):
        if x % 2 == 0:
           sum = sum - 1.0 / x 
        else:
           sum = sum + 1.0 / x 
    return sum



# Parallel Partial Summary function to approximate log(2).
# log(2) = 1 - 1/2 + 1/3 - 1/4 + +1/5 .... 
# Execute the same task with different amount of active workers and measure the time
def parallel_part_sum(server, args=(0,0,0), sum_callback=Sum()):
    (start, end, parts) = args
    step = (end - start) / parts + 1
    start_time = time.time()
    callbackargs = 0
    for index in xrange(parts):
        starti = start+index*step
        endi = min(start+(index+1)*step, end)
        # Submit a job which will calculate partial sum 
        # part_sum - the function
        # (starti, endi) - tuple with arguments for part_sum
        # callback (sum.add) - callback function
        # NOTE: the `index` value inside will be used for the parameter `value` in add(), NOT for pid !!
        callbackargs = (int(index + 1),)
        server.submit(part_sum,(starti, endi),callback=sum_callback.add,callbackargs=callbackargs,group="my_processes")
        print("Process P" + str(index) + \
              " (" + str(starti) + ", " + str(endi) + ") started")




# The Main Function
def main(args):
    print("""Usage: python callback.py [ncpus]
          [ncpus] - the number of workers to run in parallel, 
          if omitted it will be set to the number of processors in the system
          """)

    ### ppserver configuration
    # tuple of all parallel python servers to connect with
    # server tuple
    ppservers=("127.0.0.1:65000",)
    #ppservers=("cisban-node1.ncl.ac.uk:65000",)
    # number of cpus to use IN THE LOCALHOST!
    # IMPORTANT: set ncpus to 0 if all the processes have to run on a server!
    ncpus = 1
    # a passkey
    secret='donald_duck'
    if len(args) > 1:
        ncpus = int(args[1])
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus=ncpus, ppservers=ppservers, secret=secret)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers, secret=secret)
    print("Starting pp with " + str(job_server.get_ncpus()) + " workers.\n")


    # Create an instance of callback class
    sum_callback = Sum()


    # Problem Solving
    start = 1
    end = 1000000000
    # Divide the task into 50 subtasks
    parts = 500
    """ This function calculate the partial sum parallely, invoking 
        the method submit() of the class pp.Server. 
        Note that it passes the callback function too. """
    print("\nCompute the partial sum from " + str(start) + " to " + str(end) + \
          " using " + str(parts) + " processes\n")
    parallel_part_sum(server=job_server, args=(start, end, parts), sum_callback=sum_callback)        
    # Wait for jobs in all groups to finish 
    job_server.wait(group="my_processes")


    # Print the partial sum
    print("\nComputation Results:" + \
          "\n  Partial sum = " + str(sum_callback.get_value()) + \
          "\n  log(2)      = " + str(math.log(2)) +
          "\n  diff        = " + str(math.log(2) - sum_callback.get_value()) + 
          "\n")

    # print statistics
    job_server.print_stats()
    job_server.destroy()




main(sys.argv)
