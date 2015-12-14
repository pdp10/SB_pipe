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



# Collection of functions for generating Latex code. These functions are used for reporting purposes.

import sys
import os, glob
import csv
import shlex, subprocess

# sort by string considering the locale
import locale
# this reads the environment and inits the right locale
locale.setlocale(locale.LC_ALL, "")
# alternatively, (but it's bad to hardcode)
# locale.setlocale(locale.LC_ALL, "sv_SE.UTF-8")
  

######################
### PREPROCESSING 
######################

# folders is a list of 3 lists. The latter contains the files to sort and to clean (preprocessing phase)
def preprocess_comparison_3hp(folders):
  folders[0].sort(cmp=locale.strcoll)
  folders[1].sort(cmp=locale.strcoll)
  folders[2].sort(cmp=locale.strcoll)
  # Remove unknown_mTORC2_activ and PI3K_like from folders[0] and folders[1]
  folders[0][:] = (value for value in folders[0] if value.find("unknown_mTORC2_activ") == -1)
  
# folders is a list of 4 lists. The latter contains the files to sort and to clean (preprocessing phase)
def preprocess_comparison(folders):
  folders[0].sort(cmp=locale.strcoll)
  folders[1].sort(cmp=locale.strcoll)
  folders[2].sort(cmp=locale.strcoll)
  folders[3].sort(cmp=locale.strcoll)
  # Remove unknown_mTORC2_activ and PI3K_like from folders[0] and folders[1]
  folders[0][:] = (value for value in folders[0] if value.find("unknown_mTORC2_activ") == -1)
  folders[1][:] = (value for value in folders[1] if value.find("PI3K_like") == -1)



######################
### HEADER BUILDING
######################


# Initialize a Latex header with a title and an abstract
def get_latex_header(pdftitle = "", title = "", abstract=""):
  return "\\documentclass[10pt,a4paper]{article}\n" \
	   "\\usepackage[utf8]{inputenc}\n" \
	   "\\usepackage[english]{babel}\n" \
	   "\\usepackage[T1]{fontenc}\n" \
	   "\\usepackage[a4paper,top=2.54cm,bottom=2.54cm,left=3.17cm,right=3.17cm]{geometry}\n" \
	   "\\usepackage{graphicx}\n" \
	   "\\usepackage[plainpages=false,pdfauthor={Generated with SB pipe},pdftitle={" + pdftitle + "},pdftex]{hyperref}\n" \
	   "\\hypersetup{colorlinks=false,linkcolor=blue}\n" \
	   "\\usepackage{url}\n" \
	   "\\usepackage{makeidx}\n" \
	   "\\title{" + title + "}\n" \
	   "\\date{\\today}\n" \
	   "\\makeindex\n" \
	   "\\begin{document}\n" \
	   "\\maketitle\n" \
	   "\\begin{abstract}\n" + abstract + "\\end{abstract}\n" \
	   "\\tableofcontents\n"

## This was right above \title
#	   "\\author{Piero Dalle Pezze \\\ \n" \
#	   "\\small Institute for Ageing and Health\\\[-0.8ex] \n" \
#	   "\\small Newcastle University\\\[-0.8ex] \n" \
#	   "\\small Newcastle Upon Tyne, UK\\\ \n" \
#	   "\\small \\texttt{piero.dallepezze@ncl.ac.uk}} \n" \



#####################################
### COMPARISON BETWEEN HYPOTHESES 
#####################################


# Compare the models of the three hypotheses
def compare_model_hypotheses_3hp(results_dir, folders, models, species):
  file_out = open(results_dir + "/graphs_par_scan_" + species + "_eval_3hp.tex", "w")
  species_name = species[0:].replace("_", " ")
  print("Models: " + models[0] + " " + models[1] + " " + models[2])
  print("Perturbation of the species: " + species)
  # Get latex header
  header = get_latex_header("Graphs of the three mTOR model hypotheses", "Graphs of the three mTOR model hypotheses", "Parameter Scan Task for " + species_name)
  file_out.write(header)
  #print("List of files in " + path + ":\n")
  print("****************** Time Courses *******************")
  file_out.write("\\section{Comparison of the models pi3k\\_indep, pi3k\\_dep, tsc\\_dep - Perturbation of " + species_name + "}\n")
  minimum = min([len(folders[0]), len(folders[1]), len(folders[2])])
  print([len(folders[0]), len(folders[1]), len(folders[2])])
  for i in range(0, minimum):
    filea = folders[0][i]
    fileb = folders[1][i]
    filec = folders[2][i]
    a = filea.find(species)
    b = fileb.find(species)
    c = filec.find(species)
    a_marker = filea.find("_eval_")
    b_marker = fileb.find("_eval_")
    c_marker = filec.find("_eval_")  
    if (a != -1 and b != -1 and c != -1 and
	a < a_marker and b < b_marker and c < c_marker and
	filea[a:] == fileb[b:] and fileb[b:] == filec[c:]):
      print(filea[a:])
      file_out.write("\\includegraphics[scale=0.16]{" + models[0] + "/tc_parameter_scan/" + filea + "}\n")
      file_out.write("\\hfill\n")
      file_out.write("\\includegraphics[scale=0.16]{" + models[1] + "/tc_parameter_scan/" + fileb + "}\n")
      file_out.write("\\hfill\n")
      file_out.write("\\includegraphics[scale=0.16]{" + models[2] + "/tc_parameter_scan/" + filec + "}\n")
      file_out.write("\\hfill\n")
    else:
      print("Skipped file: " + filea)
  file_out.write("\\end{document}\n")
  file_out.close()
  p = subprocess.Popen("pdflatex -output-directory hp_comparison/ " + "hp_comparison/graphs_par_scan_" + species + "_eval_3hp.tex", shell=True)
  sts = os.waitpid(p.pid, 0)[1]
  

# Compare the models of the four hypotheses
def compare_model_hypotheses(results_dir, folders, models, species):
  file_out = open(results_dir + "/graphs_par_scan_" + species + "_KD.tex", "w")
  species_name = species[0:].replace("_", " ")
  print("Models: " + models[0] + " " + models[1] + " " + models[2] + " " + models[3])
  print("Perturbation of the species: " + species)
  # writing on file
  # Get latex header
  header = get_latex_header("Graphs of the four mTOR model hypotheses", "Graphs of the four mTOR model hypotheses", "Parameter Scan Task for " + species_name)
  file_out.write(header)
  #print("List of files in " + path + ":\n")
  print("****************** Time Courses *******************")
  file_out.write("\\section{Comparison of the models pi3k\\_indep, pi3k\\_iso\\_dep, pi3k\\_dep, tsc\\_dep - Perturbation of " + species_name + "}\n")
  minimum = min([len(folders[0]), len(folders[1]), len(folders[2]), len(folders[3])])
  print([len(folders[0]), len(folders[1]), len(folders[2]), len(folders[3])])
  for i in range(0, minimum):
    filea = folders[0][i]
    fileb = folders[1][i]
    filec = folders[2][i]
    filed = folders[3][i]
    a = filea.find(species)
    b = fileb.find(species)
    c = filec.find(species)
    d = filed.find(species)
    a_marker = filea.find("_eval_")
    b_marker = fileb.find("_eval_")
    c_marker = filec.find("_eval_")  
    d_marker = filed.find("_eval_")  
    if (a != -1 and b != -1 and c != -1 and d != -1 and
	a < a_marker and b < b_marker and c < c_marker and d < d_marker and
	filea[a:] == fileb[b:] and fileb[b:] == filec[c:] and filec[c:] == filed[d:]):
      print(filea[a:])
      file_out.write("\\includegraphics[scale=0.12]{" + models[0] + "/tc_parameter_scan/" + filea + "}\n")
      file_out.write("\\hfill\n")
      file_out.write("\\includegraphics[scale=0.12]{" + models[1] + "/tc_parameter_scan/" + fileb + "}\n")
      file_out.write("\\hfill\n")
      file_out.write("\\includegraphics[scale=0.12]{" + models[2] + "/tc_parameter_scan/" + filec + "}\n")
      file_out.write("\\hfill\n")
      file_out.write("\\includegraphics[scale=0.12]{" + models[3] + "/tc_parameter_scan/" + filed + "}\n")
      file_out.write("\\hfill\n")
    else:
      print("Skipped file: " + filea)
  file_out.write("\\end{document}\n")
  file_out.close()
  p = subprocess.Popen("pdflatex -output-directory hp_comparison/ " + "hp_comparison/graphs_par_scan_" + species + "_KD.tex", shell=True)
  sts = os.waitpid(p.pid, 0)[1]  



# Compare the models of the three hypotheses (normal timecourses)
def compare_model_hypotheses_timecourses_3hp(results_dir, folders, models, names_table):
  file_out = open(results_dir + "/graphs_timecourses_3hp.tex", "w")
  # Control variable
  found = False
  print("Models: " + models[0] + " " + models[1] + " " + models[2])
  # writing on file
  # Get latex header
  header = get_latex_header("Graphs of the three mTOR model hypotheses", "Graphs of the three mTOR model hypotheses", "Time Courses Task")
  file_out.write(header)
  #print("List of files in " + path + ":\n")
  print("****************** Time Courses *******************")
  minimum = min([len(folders[0]), len(folders[1]), len(folders[2])])
  print(minimum)
  print([len(folders[0]), len(folders[1]), len(folders[2])])
  #for i in range(0, minimum):
    #print(folders[0][i]) 
    #print(folders[1][i])
    #print(folders[2][i])
    #print("")
  #for row in names_table:
  #  print row
  #  print("")
  file_out.write("\\section{Comparison of the models pi3k\\_indep, pi3k\\_dep, tsc\\_dep - Simulation vs Experiments}\n")
  # it prints following the order of signals (this is not the best performance..)
  for row in names_table:
    for i in range(0, minimum):
      if(folders[0][i].find(row) != -1):
	filea = folders[0][i]
	fileb = folders[1][i]
	filec = folders[2][i]     
	a = filea.find("_sem_")
	b = fileb.find("_sem_")
	c = filec.find("_sem_")
	print(row + "    " + folders[0][i])
	if (a != -1 and b != -1 and c != -1 and
	    filea[a:] == fileb[b:] and fileb[b:] == filec[c:]):
	  print(filea[a:])
	  file_out.write("\\includegraphics[scale=0.16]{" + models[0] + "/tc_mean_with_exp/" + filea + "}\n")
	  file_out.write("\\hfill\n")
	  file_out.write("\\includegraphics[scale=0.16]{" + models[1] + "/tc_mean_with_exp/" + fileb + "}\n")
	  file_out.write("\\hfill\n")
	  file_out.write("\\includegraphics[scale=0.16]{" + models[2] + "/tc_mean_with_exp/" + filec + "}\n")
	  file_out.write("\\hfill\n")
	  break
  file_out.write("\\section{Comparison of the models pi3k\\_indep, pi3k\\_dep, tsc\\_dep - Other Simulations}\n")
  for i in range(0, minimum):
    filea = folders[0][i]
    fileb = folders[1][i]
    filec = folders[2][i]
    a = filea.find("_sem_")
    b = fileb.find("_sem_")
    c = filec.find("_sem_")
    if (a != -1 and b != -1 and c != -1 and
	  filea[a:] == fileb[b:] and fileb[b:] == filec[c:]):
      found = False
      for row in names_table:
	if filea.find(row) != -1:
	  found = True
	  break
      if found == False:    
	print(filea[a:])
	file_out.write("\\includegraphics[scale=0.16]{" + models[0] + "/tc_mean_with_exp/" + filea + "}\n")
	file_out.write("\\hfill\n")
	file_out.write("\\includegraphics[scale=0.16]{" + models[1] + "/tc_mean_with_exp/" + fileb + "}\n")
	file_out.write("\\hfill\n")
	file_out.write("\\includegraphics[scale=0.16]{" + models[2] + "/tc_mean_with_exp/" + filec + "}\n")
	file_out.write("\\hfill\n")
  file_out.write("\\end{document}\n")
  file_out.close()
  p = subprocess.Popen("pdflatex -output-directory hp_comparison/ " + "hp_comparison/graphs_timecourses_3hp.tex", shell=True)
  sts = os.waitpid(p.pid, 0)[1]


# Compare the models of the four hypotheses (normal timecourses)
def compare_model_hypotheses_timecourses(results_dir, folders, models, names_table):
  file_out = open(results_dir + "/graphs_timecourses.tex", "w")
  # Control variable
  found = False
  print("Models: " + models[0] + " " + models[1] + " " + models[2]+ " " + models[3])
  # writing on file
  # Get latex header
  header = get_latex_header("Graphs of the four mTOR model hypotheses", "Graphs of the four mTOR model hypotheses", "Time Courses Task")
  file_out.write(header)
  #print("List of files in " + path + ":\n")
  print("****************** Time Courses *******************")
  minimum = min([len(folders[0]), len(folders[1]), len(folders[2]), len(folders[3])])
  print(minimum)
  print([len(folders[0]), len(folders[1]), len(folders[2]), len(folders[3])])
  #for i in range(0, minimum):
    #print(folders[0][i]) 
    #print(folders[1][i])
    #print(folders[2][i])
    #print("")
  #for row in names_table:
  #  print row
  #  print("")
  file_out.write("\\section{Comparison of the models pi3k\\_indep, pi3k\\_iso\\_dep, pi3k\\_dep, tsc\\_dep - Simulation vs Experiments}\n")
  # it prints following the order of signals (this is not the best performance..)
  for row in names_table:
    for i in range(0, minimum):
      if(folders[0][i].find(row) != -1):
	filea = folders[0][i]
	fileb = folders[1][i]
	filec = folders[2][i]
	filed = folders[3][i]      
	a = filea.find("_sem_")
	b = fileb.find("_sem_")
	c = filec.find("_sem_")
	d = filed.find("_sem_")
	print(row + "    " + folders[0][i])
	if (a != -1 and b != -1 and c != -1 and d != -1 and
	    filea[a:] == fileb[b:] and fileb[b:] == filec[c:] and filec[c:] == filed[d:]):
	  print(filea[a:])
	  file_out.write("\\includegraphics[scale=0.12]{" + models[0] + "/tc_mean_with_exp/" + filea + "}\n")
	  file_out.write("\\hfill\n")
	  file_out.write("\\includegraphics[scale=0.12]{" + models[1] + "/tc_mean_with_exp/" + fileb + "}\n")
	  file_out.write("\\hfill\n")
	  file_out.write("\\includegraphics[scale=0.12]{" + models[2] + "/tc_mean_with_exp/" + filec + "}\n")
	  file_out.write("\\hfill\n")
	  file_out.write("\\includegraphics[scale=0.12]{" + models[3] + "/tc_mean_with_exp/" + filed + "}\n")
	  file_out.write("\\hfill\n")
	  break
  file_out.write("\\section{Comparison of the models pi3k\\_indep, pi3k\\_iso\\_\\_dep, pi3k\\_dep, tsc\\_dep - Other Simulations}\n")
  for i in range(0, minimum):
    filea = folders[0][i]
    fileb = folders[1][i]
    filec = folders[2][i]
    filed = folders[3][i]
    a = filea.find("_sem_")
    b = fileb.find("_sem_")
    c = filec.find("_sem_")
    d = filed.find("_sem_")  
    if (a != -1 and b != -1 and c != -1 and d != -1 and
	  filea[a:] == fileb[b:] and fileb[b:] == filec[c:] and filec[c:] == filed[d:]):
      found = False
      for row in names_table:
	if filea.find(row) != -1:
	  found = True
	  break
      if found == False:    
	print(filea[a:])
	file_out.write("\\includegraphics[scale=0.12]{" + models[0] + "/tc_mean_with_exp/" + filea + "}\n")
	file_out.write("\\hfill\n")
	file_out.write("\\includegraphics[scale=0.12]{" + models[1] + "/tc_mean_with_exp/" + fileb + "}\n")
	file_out.write("\\hfill\n")
	file_out.write("\\includegraphics[scale=0.12]{" + models[2] + "/tc_mean_with_exp/" + filec + "}\n")
	file_out.write("\\hfill\n")
	file_out.write("\\includegraphics[scale=0.12]{" + models[3] + "/tc_mean_with_exp/" + filed + "}\n")
	file_out.write("\\hfill\n")
  file_out.write("\\end{document}\n")
  file_out.close()
  p = subprocess.Popen("pdflatex -output-directory hp_comparison/ " + "hp_comparison/graphs_timecourses.tex", shell=True)
  sts = os.waitpid(p.pid, 0)[1]



###############################
### SINGLE MODEL LATEX REPORT
###############################

# Create a report for a parameter scanning task (1 model)
def latex_report_par_scan(results_dir, tc_parameter_scan_dir, param_scan__single_perturb_prefix_results_filename, model_noext, species, param_scan__single_perturb_legend):
  file_out = open(results_dir + "/" + param_scan__single_perturb_prefix_results_filename + model_noext + ".tex", "w")
  model_ver = model_noext[:].replace("_", " ")
  species_name = species[0:].replace("_", " ")
  print("Model: " + model_ver)
  print("Perturbation of the species: " + species)
  # writing on file
  # Get latex header
  header = get_latex_header("Report: " + model_ver + " (Parameter Scan)", "Report: " + model_ver, "Parameter Scan Task for " + species_name)
  file_out.write(header)
  print("List of files in " + results_dir + '/' + tc_parameter_scan_dir  + '/' + ":\n")
  print("****************** Time Courses *******************")
  file_out.write("\\section{Simulations - Perturbation of " + species_name + "}\n")
  folder = os.listdir(results_dir + '/' + tc_parameter_scan_dir + '/')
  folder.sort()
  for infile in folder:
    if infile.find(model_noext) != -1:
      pos = infile.find(species)
      marker = infile.find("__eval_")
      if pos != -1 and pos < marker:
	print(infile)
	file_out.write("\\includegraphics[scale=0.16]{" + tc_parameter_scan_dir + "/" + infile + "}\n")
	file_out.write("\\hfill\n")
  file_out.write("\\includegraphics[scale=0.16]{" + tc_parameter_scan_dir + "/" + param_scan__single_perturb_legend + ".png}\n")
  file_out.write("\\hfill\n")
  file_out.write("\\end{document}\n")
  file_out.close()
  print("***************************************************\n")  


# Create a report of a time course task (1 model)
def latex_report(results_dir, tc_mean_dir, model_noext, simulate__prefix_results_filename):
  file_out = open(results_dir + "/" + simulate__prefix_results_filename + model_noext + ".tex", "w")
  # Control variable
  found = False
  model_ver = model_noext[:].replace("_", " ")
  print(model_ver)
  # writing on file
  # Get latex header
  header = get_latex_header("Report: " + model_ver + " (Time Courses Task)", "Report: " + model_ver, "Time Courses Task")
  file_out.write(header)  
  print("List of files in " + results_dir + '/' + tc_mean_dir + '/' + ":\n")
  print("****************** Time Courses *******************")
  file_out.write("\\section{Simulation}\n")
  folder = os.listdir(results_dir + '/' + tc_mean_dir + '/')
  folder.sort()  
  # 1) this replaces the commented code below
  for infile in folder:
    if infile.find(model_noext) != -1:
      #if (infile.find('_ci95_') != -1):
      if (infile.find('_sd_n_ci95_') != -1):
      #if (infile.find('_sd_') != -1):	
      #if (infile.find('_sem_') != -1):
	print(infile)
	file_out.write("\\includegraphics[scale=0.08]{" + tc_mean_dir + "/" + infile + "}\n")
	file_out.write("\\hfill\n")
  # 2) it prints following the order of signals (this is not the best performance..)
  #for row in names_table:
      #for infile in folder:    
	#if (infile.find('_sem_') != -1 and infile.find(row) != -1):
	  #file_out.write("\\includegraphics[scale=0.16]{" + "tc_mean_with_exp/" + infile + "}\n")
	  #file_out.write("\\hfill\n")
	  #break
  #file_out.write("\\section{Other Simulations}\n")
  #for infile in folder:
    #if infile.find('_sem_') != -1:
      #found = False
      #print(infile)
      #for row in names_table:
	#if infile.find(row) != -1:
	  #found = True
	  #break
      #if found == False:
	#file_out.write("\\includegraphics[scale=0.16]{" + "tc_mean_with_exp/" + infile + "}\n")
	#file_out.write("\\hfill\n")
  file_out.write("\\end{document}\n")
  file_out.close()
  print("***************************************************\n")    



# Plot combinatorial inhibitors
def plot_inhibitors_comparison(results_dir, model, plots):
  file_out = open(results_dir + "/graphs_par_scan_" + model + ".tex", "w")
  #print("Perturbation of the species: " + specie)
  # Get latex header
  header = get_latex_header("PI3K, TOR, PI3K-TOR inhibitors", "PI3K, TOR, PI3K-TOR inhibitors", "")
  file_out.write(header)
  #print("List of files in " + path + ":\n")
  print("****************** Time Courses *******************")
  file_out.write("\\section*{(1) PI3K Inhib; (2) mTOR Inhib; (3) PI3K+TOR Inhib}\n")
  for i in range(0, len(plots[0])):
    if (plots[0][i].find('only_PI3K_level.png') != -1 or 
	plots[0][i].find('only_mTOR_level.png') != -1 or 
	plots[0][i].find('comb_PI3K_mTOR_level.png') != -1) :
      print(plots[0][i])
      continue
    else:
	file_out.write("\\includegraphics[scale=0.16]{" + model + "/tc_parameter_scan/" + plots[0][i] + "}\n")
	file_out.write("\\hfill\n")
	file_out.write("\\includegraphics[scale=0.16]{" + model + "/tc_parameter_scan/" + plots[1][i] + "}\n")
	file_out.write("\\hfill\n")
	file_out.write("\\includegraphics[scale=0.16]{" + model + "/tc_parameter_scan/" + plots[2][i] + "}\n")
	file_out.write("\\hfill\n")
  file_out.write("\\includegraphics[scale=0.16]{legends/inhibitors_legend.png}\n")
  file_out.write("\\hfill\n")
  file_out.write("\\includegraphics[scale=0.16]{legends/inhibitors_legend.png}\n")
  file_out.write("\\hfill\n")
  file_out.write("\\includegraphics[scale=0.16]{legends/inhibitors_legend.png}\n")
  file_out.write("\\hfill\n")
  file_out.write("\\end{document}\n")
  file_out.close()
  #p = subprocess.Popen("pdflatex -output-directory hp_comparison/ " + "hp_comparison/graphs_par_scan_" + model + ".tex", stdout=subprocess.PIPE).communicate()[0]
  p = subprocess.Popen("pdflatex -output-directory hp_comparison/ " + "hp_comparison/graphs_par_scan_" + model + ".tex", shell=True)
  sts = os.waitpid(p.pid, 0)[1]
