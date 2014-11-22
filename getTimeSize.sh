#!/bin/bash

if [ $# -ne 1 ]
  then
    echo "Provide job report. Usage:"
    echo "./getTimeSize.sh CMSSW_X_X_X/src/test.xml"
    exit 1
fi

n=`grep "TotalEvents" $1 | awk 'BEGIN{FS=">"}{print $2}' | awk 'BEGIN{FS="<"}{print $1}'`
echo "Events:       "$n

time=`grep "AvgEventCPU" $1 | awk 'BEGIN{FS="\""}{print $4}'`
echo "CPU Time [s]: "$time

total_size=`grep "Timing-tstoragefile-write-totalMegabytes" $1 | awk 'BEGIN{FS="\""}{print $4}'`
avg_size=`echo "$total_size*1024/$n" | bc -l`
echo "Size [kB]:    "$avg_size
