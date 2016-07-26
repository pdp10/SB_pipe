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
import datetime

import os
import sys
import glob
import shutil
import logging
logger = logging.getLogger('sbpipe')


import simulate__generate_data
import simulate__analyse_data
import simulate__generate_report

SB_PIPE = os.environ["SB_PIPE"]
sys.path.append(os.path.join(SB_PIPE, "sb_pipe", "utils", "python"))
from config_parser import config_parser



"""
This module provides the user with a complete pipeline of scripts for running 
a model simulation using copasi
"""

def main(config_file):
  """
  Execute and collect results for a model simulation using Copasi
  Keyword arguments:
      config_file -- the file containing the model configuration, usually in working_folder (e.g. model.conf)
  """
  
  logger.info("Reading file " + config_file + " : \n")

  # Initialises the variables for this pipeline
  (generate_data, analyse_data, generate_report,
      project_dir, model, copasi_reports_path, 
      cluster, pp_cpus, runs, 
      simulate__xaxis_label) = config_parser(config_file, "simulate")
  
  
  runs = int(runs)
  pp_cpus = int(pp_cpus)

  # Some controls
  if runs < 1: 
    logger.error("variable `runs` must be greater than 0. Please, check your configuration file.");
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


  # Get the pipeline start time
  start = datetime.datetime.now().replace(microsecond=0)


      
  logger.info("\n")
  logger.info("Processing model "+ model)
  logger.info("#############################################################")
  logger.info("")
	
  # preprocessing
  if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
  if not os.path.exists(results_dir):
    os.makedirs(results_dir) 
 
 
  if generate_data == True:
    logger.info("\n")
    logger.info("Data generation:")
    logger.info("################")
    simulate__generate_data.main(model, models_dir, os.path.join(results_dir, sim_raw_data), tmp_dir, cluster, pp_cpus, runs)


  if analyse_data == True:
    logger.info("\n")
    logger.info("Data analysis:")
    logger.info("##############")
    simulate__analyse_data.main(model[:-4], os.path.join(results_dir, sim_raw_data), results_dir, tc_dir, tc_mean_dir, tc_mean_with_exp_dir, simulate__xaxis_label)    


  if generate_report == True:
    logger.info("\n")
    logger.info("Report generation:")
    logger.info("##################")
    simulate__generate_report.main(model[:-4], results_dir, tc_mean_dir)


  # Print the pipeline elapsed time
  end = datetime.datetime.now().replace(microsecond=0)
  logger.info("\n\nPipeline elapsed time (using Python datetime): " + str(end-start)) 


  if len(glob.glob(os.path.join(results_dir, tc_mean_dir, model[:-4]+'*.png'))) > 0 and len(glob.glob(os.path.join(results_dir, '*'+model[:-4]+'*.pdf'))) == 1:
       return 0
  return 1

