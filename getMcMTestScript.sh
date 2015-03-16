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

prepid=$1
shift
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
	-h | --help) echo "Usage: sh getMcMTestScript.sh PrepID [-o outputFile] [-n number_of_events]"
	    exit
	    ;;
	*) echo "Bad arguments. Usage:"
	    echo " sh getMcMTestScript.sh PrepID [-o outputFile] [-n number_of_events]"
	    exit 1
    esac
    shift
done

echo "Getting test script for ${prepid} from McM."

curl --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/${prepid} -o ${outputFile}

sed -i '/grep/d' ${outputFile}
echo "sh getTimeSize.sh ${1}_rt.xml" >> ${outputFile}
