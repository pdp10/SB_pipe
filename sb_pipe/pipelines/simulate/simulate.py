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
#
# $Revision: 2.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-06-23 16:14:32 $




# for computing the pipeline elapsed time 
import time

import os
import sys
import glob
import shutil

from ConfigParser import ConfigParser
from StringIO import StringIO


import simulate__generate_data
import simulate__analyse_data
import simulate__generate_report




"""
This module provides the user with a complete pipeline of scripts for running 
a model simulation using copasi
"""

def main(model_configuration):
  """
  Execute and collect results for a model simulation using Copasi
  Keyword arguments:
      model_configuration -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """
  
  print("\nReading file " + model_configuration + " : \n")
  # import the model configuration data (project, model-name, association-pattern)
  parser = ConfigParser()
  with open(model_configuration) as stream:
    stream = StringIO("[top]\n" + stream.read())  # This line does the trick.
    parser.readfp(stream)  
    
  lines=parser.items('top')
  
  # Boolean
  generate_data=True
  # Boolean
  analyse_data=True
  # Boolean
  generate_report=True
  # the project directory
  project_dir=""
  # The Copasi model
  model="mymodel.cps"
  # The path to Copasi reports
  copasi_reports_path="tmp"
  # The parallel mechanism to use (pp | sge | lsf).
  cluster="pp"
  # The number of cpus for pp
  pp_cpus=1
  # The number of jobs to be executed
  runs=1  
  # The plot x axis label (e.g. Time[min])
  # This is required for plotting
  simulate__xaxis_label="Time [min]"


  # Initialises the variables
  for line in lines:
    print line
    if line[0] == "generate_data":
      generate_data = {'True': True, 'False': False}.get(line[1], False)     
    if line[0] == "analyse_data":
      analyse_data = {'True': True, 'False': False}.get(line[1], False)     
    if line[0] == "generate_report":
      generate_report = {'True': True, 'False': False}.get(line[1], False)           
    if line[0] == "project_dir":
      project_dir = line[1] 
    elif line[0] == "model": 
      model = line[1] 
    elif line[0] == "copasi_reports_path": 
      copasi_reports_path = line[1]
    elif line[0] == "cluster": 
      cluster = line[1] 
    elif line[0] == "pp_cpus": 
      pp_cpus = line[1] 
    elif line[0] == "runs": 
      runs = line[1]      
    elif line[0] == "simulate__xaxis_label":
      simulate__xaxis_label = line[1]     


  runs = int(runs)
  pp_cpus = int(pp_cpus)

  # Some controls
  if runs < 1: 
    print("ERROR: variable `runs` must be greater than 0. Please, check your configuration file.");
    return 1


  # INTERNAL VARIABLES
  # The data folder containing the dataset
  data_folder="Data"  
  # The folder containing the models
  models_folder="Models"
  # The folder containing the working results
  working_folder="Working_Folder"
  # The dataset working folder
  sim_raw_data="sim_raw_data"
  # The dataset timecourses dir
  tc_dir="tc"
  # The dataset mean timecourses dir
  tc_mean_dir="tc_mean"
  # The dataset mean timecourses with experimental data dir
  tc_mean_with_exp_dir="tc_mean_w_exp_dir"

  models_dir = os.path.join(project_dir, models_folder)
  results_dir = os.path.join(project_dir, working_folder, model[:-4])
  data_dir = os.path.join(project_dir, data_folder)
  tmp_dir = copasi_reports_path



  print("\n<START PIPELINE>\n")
  # Get the pipeline start time
  start = time.clock()


      
  print("\n")
  print("#############################################################")
  print("### Processing model "+ model)
  print("#############################################################")
  print("")
	
  # preprocessing
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir) 
 
 
  if generate_data == True:
    print("\n")
    print("Data generation:")
    print("################")
    simulate__generate_data.main(model, models_dir, os.path.join(results_dir, sim_raw_data), tmp_dir, cluster, pp_cpus, runs)


  if analyse_data == True:
    print("\n")
    print("Data analysis:")
    print("##############")
    simulate__analyse_data.main(model[:-4], os.path.join(results_dir, sim_raw_data), results_dir, tc_dir, tc_mean_dir, tc_mean_with_exp_dir, simulate__xaxis_label)    


  if generate_report == True:
    print("\n")
    print("Report generation:")
    print("##################")
    simulate__generate_report.main(model[:-4], results_dir, tc_mean_dir)


  # Print the pipeline elapsed time
  end = time.clock()
  print("\n\nPipeline elapsed time (using Python time.clock()): " + str(end-start)) 
  print("\n<END PIPELINE>\n")


  if len(glob.glob(os.path.join(results_dir, tc_mean_dir, model[:-4]+'*.png'))) > 0 and len(glob.glob(os.path.join(results_dir, '*'+model[:-4]+'*.pdf'))) == 1:
       return 0
  return 1
