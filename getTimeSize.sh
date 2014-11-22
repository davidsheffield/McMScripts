#!/bin/bash

################################
#
# getTimeSize.sh
#
#  Script to extract the number of events, average CPU time, and file size
#  from a job report and calculate the size per event in kilobytes.
#
#  author: David G. Sheffield (Rutgers)
#
################################

if [ $# -ne 1 ]
  then
    echo "Provide job report. Usage:"
    echo "sh getTimeSize.sh job_report.xml"
    exit 1
fi

n=`grep "TotalEvents" $1 | awk 'BEGIN{FS=">"}{print $2}' | awk 'BEGIN{FS="<"}{print $1}'`
echo "Events:       "$n

time=`grep "AvgEventCPU" $1 | awk 'BEGIN{FS="\""}{print $4}'`
echo "CPU Time [s]: "$time

total_size=`grep "Timing-tstoragefile-write-totalMegabytes" $1 | awk 'BEGIN{FS="\""}{print $4}'`
avg_size=`echo "$total_size*1024/$n" | bc -l` # Conver total size to kilobytes and calculate average per event
echo "Size [kB]:    "$avg_size
