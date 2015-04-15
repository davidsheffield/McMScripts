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
echo "sh getTimeSize.sh ${prepid}_rt.xml" >> ${outputFile}

#numberFromFile=`sed -n 's/.*-n \(.*\) ||.*/\1/p' ${outputFile}`
if [ $number -gt 0 ]; then
    sed -i "s/-n .* ||/-n ${number} ||/" ${outputFile}
    sed -i "s/echo .* events were ran/echo ${number} events were run/" ${outputFile}
fi