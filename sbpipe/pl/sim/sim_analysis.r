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
#
# $Revision: 3.0 $
# $Author: Piero Dalle Pezze $
# $Date: 2016-07-7 16:14:32 $



# Retrieve the environment variable SBPIPE
SBPIPE <- Sys.getenv(c("SBPIPE"))
source(file.path(SBPIPE, 'sbpipe','R','sbpipe_sim.r'))


# R Script to plot time courses and collect statistics.
#
# :args[1]: the model name without extension
# :args[2]: the input directory
# :args[3]: the output directory
# :args[4]: the output file name containing the statistics
# :args[5]: the output template file storing the summary of model simulation repeats
# :args[6]: the file containing the experimental data.
# :args[7]: TRUE if the experimental data should also be plotted
# :args[8]: the label for the x axis (e.g. Time [min])
# :args[9]: the label for the y axis (e.g. Level [a.u.])
main <- function(args) {
    model_noext <- args[1]
    inputdir <- args[2]
    outputdir <- args[3]
    outputfile <- args[4]
    repeats_file_template <- args[5]
    exp_dataset <- args[6]
    plot_exp_dataset <- args[7]
    xaxis_label <- args[8]
    yaxis_label <- args[9]

    # generate a table of statistics
    gen_stats_table(inputdir, outputdir, model_noext, outputfile, xaxis_label, yaxis_label)

    # summarise the time course repeats in tables
    summarise_data(inputdir, model_noext, repeats_file_template)
    print(repeats_file_template)
    # plot the time courses
    plot_sep_sims(dirname(repeats_file_template), outputdir, model_noext, exp_dataset, plot_exp_dataset, xaxis_label, yaxis_label)
    plot_comb_sims(dirname(repeats_file_template), outputdir, model_noext, exp_dataset, plot_exp_dataset, xaxis_label, yaxis_label)
}


main(commandArgs(TRUE))
# Clean the environment
rm ( list=ls ( ) )
