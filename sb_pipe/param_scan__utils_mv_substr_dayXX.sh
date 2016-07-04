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




# This script moves the substring "_dayXX" at the end of the file.

folder=$1


for filenamein in `ls $folder/*.png `
do
    daynum=`expr match "$filenamein" '.*_day\([[:digit:]]*\)_.*' `
    daynum="_day${daynum}"
#echo "${daynum}"

    filenameout=${filenamein/$daynum/""}
    filenameout=${filenameout/.png/${daynum}.png}

    echo "${filenamein} => ${filenameout}"
    mv ${filenamein} ${filenameout}
done