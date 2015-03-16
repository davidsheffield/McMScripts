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

if [ $# -ne 1 ]
  then
    echo "Provide PrepID. Usage:"
    echo "sh getMcMTestScript.sh EXO-RunIIWinter15GS-00001"
    exit 1
fi

outputFile="test.sh"

curl --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/${1} -o ${outputFile}

sed -i '/grep/d' ${outputFile}
echo "sh getTimeSize.sh ${1}_rt.xml" >> ${outputFile}
