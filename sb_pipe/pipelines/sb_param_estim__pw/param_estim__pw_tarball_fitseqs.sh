#!/bin/bash
# This file is part of sb_pipe.
#
# sb_pipe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sb_pipe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
#
#
# $Revision: 1.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2013-04-20 12:14:32 $
# Author:     Piero Dalle Pezze
#
# Delete previous repositories created using parallel parameter estimation based on potterswheel and openlava, 
# and create a tarball tar.bz2 of the fits sequence folders.



# Import the libraries
. ${SB_PIPE_LIB}/bash/param_estim__pw_func.sh



# The file containing the model configuration, usually in working_folder (e.g. model.conf)
model_configuration=$1
round=$2




if ! [[ "${round}" =~ ^[0-9]+$ ]] ; then
   exec >&2; echo "error: round must be a number"; exit 1
fi



printf "\nReading file ${model_configuration} : \n"
# import the model configuration data (project, model-name, association-pattern)
old_IFS=$IFS
IFS=$'\n'
lines=($(cat ${model_configuration}))  # array
IFS=$old_IFS
printf "\n"
printf "ROUND ${round} : \n\n"



# The project name (e.g. "p3__mtor_foxo_ros")
project=""
# The model name  
model=""
# Job name (e.g. fitseq)
job_name=""
# The folder pattern suffix (e.g. _cluster)
folder_pattern_suffix=""
# The summary folder suffix (e.g. _all_fits)
summary_folder_suffix=""
# The tarball suffix (e.g. _fitseqs_paral_comput_round)
tarball_suffix=""
# The work folder (e.g. working_folder)
work_folder=""


# read the project and the model name
old_IFS=$IFS
IFS=$'='
for line in "${lines[@]}"; do
  read -a array <<< "${line}"
  case "${array[0]}" in
    ("project") 		echo "$line"; project="${array[1]}" ;; 
    ("model") 			echo "$line"; model="${array[1]}" ;; 
    ("job_name") 		echo "$line"; job_name="${array[1]}" ;; 
    ("folder_pattern_suffix") 	echo "$line"; folder_pattern_suffix="${array[1]}" ;; 
    ("summary_folder_suffix") 	echo "$line"; summary_folder_suffix="${array[1]}" ;; 
    ("tarball_suffix") 		echo "$line"; tarball_suffix="${array[1]}" ;; 
    ("work_folder") 		echo "$line"; work_folder="${array[1]}" ;; 
  esac
done
IFS=$old_IFS



# the local working directory containing the parameter estimation output
workdir="${SB_PIPE}/${project}/${work_folder}"

# The folder used for the parallel computation
main_folder="${model%.*}${folder_pattern_suffix}"
# the pattern name of a folder containing a fits sequence
folder_pattern="${main_folder}/${job_name%.*}"
# The tarball file pattern name
tarball="${model%.*}${tarball_suffix}"
# the name of the full repository
full_repository="${model%.*}${summary_folder_suffix}_round${round}/${model%.*}_full_repository.mat"










printf "\nCreating tarball ... "
`create_tarball "${workdir}" "${model}" "${round}" "${main_folder}" "${folder_pattern}" "${tarball}" "${full_repository}" "${summary_folder_suffix}"`
printf "DONE\n"
