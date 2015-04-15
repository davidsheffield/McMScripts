#!/bin/bash

################################
#
# getMcMTestScript.sh
#
#  Script to grab McM test script and run getTimeSize.sh.
#
#  author: David G. Sheffield (Rutgers)
#
################################

prepid=""
outputFile="test.sh"
number=0
while [ "$1" != "" ]; do
    case $1 in
	-o) shift
	    outputFile=$1
	    ;;
	-n) shift
	    number=$1
	    ;;
	-h | --help) echo "Usage: sh getMcMTestScript.sh PrepID [-o outputFile] [-n numberOfEvents]"
	    exit
	    ;;
	*) prepid=$1
	    ;;
    esac
    shift
done

echo "Getting test script for ${prepid} from McM."

curl --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/${prepid} -o ${outputFile}

sed -i '/grep/d' ${outputFile}
echo "n=\`grep "\""TotalEvents"\"" ${prepid}_rt.xml | awk 'BEGIN{FS="\"">"\""}{print \$2}' | awk 'BEGIN{FS="\""<"\""}{print \$1}'\`
echo "\""Events:       "\""\$n

time=\`grep "\""AvgEventCPU"\"" ${prepid}_rt.xml | awk 'BEGIN{FS="\""\\"\"\""}{print \$4}'\`
echo "\""CPU Time [s]: "\""\$time

total_size=\`grep "\""Timing-tstoragefile-write-totalMegabytes"\"" ${prepid}_rt.xml | awk 'BEGIN{FS="\""\\"\"\""}{print \$4}'\`
avg_size=\`echo "\""\$total_size*1024/\$n"\"" | bc -l\` # Convert total size to kilobytes and calculate average per event
echo "\""Size [kB]:    "\""\$avg_size
" >> ${outputFile}

if [ $number -gt 0 ]; then
    sed -i "s/-n .* ||/-n ${number} ||/" ${outputFile}
    sed -i "s/echo .* events were ran/echo ${number} events were run/" ${outputFile}
fi