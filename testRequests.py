#!/usr/bin/env python

################################
#
# testRequests.py
#
#  Script to test the time and size per event of
#  requests in McM. Prepares results in a CSV file
#  that can be used by manageRequests.py
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sys
import subprocess
import argparse
import csv
import re
from requestClass import * # Load class to store request information

def getArguments():
    parser = argparse.ArgumentParser(description='Test McM requests.')

    # Command line flags
    parser.add_argument('-i', '--ids', dest='ids', help=
                        'List of PrepIDs to be tested. Separate range by >.')
    parser.add_argument('-f', '--file', dest='csv', help='Input CSV file.')
    parser.add_argument('-o', '--output', dest='output', default='test.csv',
                        help='Output CSV file')
    parser.add_argument('-n', dest='nEvents', help='Number of events to test.')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s v0.0')

    args_ = parser.parse_args()
    return args_

def fillIDRange(pwg, campaign, first, last):
    first = int(first)
    last = int(last)
    requests = []
    if first > last:
        print "Error: PrepID range out of order. %s-%s-%05d > %s-%s-%05d" % (
            pwg, campaign, first, pwg, campaign, last)
        print "Exiting with status 4."
        sys.exit(4)

    for number in range(first, last+1):
        tmpReq = Request()
        tmpReq.setPrepId("%s-%s-%05d" % (pwg, campaign, number))
        requests.append(tmpReq)
    return requests

def parseIDList(compactList):
    splitList = compactList.split(',')
    requests = []
    for subList in splitList:
        splitSubList = subList.split('-')
        if len(splitSubList) == 3:
            tmpReq = Request()
            tmpReq.setPrepId(subList)
            requests.append(tmpReq)
        elif len(splitSubList) == 4:
            requests = requests + fillIDRange(splitSubList[0], splitSubList[1],
                                              splitSubList[2], splitSubList[3])
        elif len(splitSubList) == 6:
            if splitSubList[0] != splitSubList[3]:
                print "Error: PrepID range must be for the same PWG."
                print "Exiting with status 4"
                sys.exit(4)
            if splitSubList[1] != splitSubList[4]:
                print "Error: PrepID range must be for the same campaign."
                print "Exiting with status 4"
                sys.exit(4)
            requests = requests + fillIDRange(splitSubList[0], splitSubList[1],
                                              splitSubList[2], splitSubList[5])
        else:
            print "Error: Poorly formed PrepID list."
            print "Exiting with status 3."
            sys.exit(3)
    return requests

def getTestScript(PrepID, nEvents):
    request_type = "requests"
    if "chain_" in PrepID:
        request_type = "chained_requests"

    get_test = ""
    if nEvents is None:
        get_test =  "curl --insecure \
https://cms-pdmv.cern.ch/mcm/public/restapi/%s/get_test/%s -o %s.sh" % (
            request_type, PrepID, PrepID)
    else:
        get_test =  "curl --insecure \
https://cms-pdmv.cern.ch/mcm/public/restapi/%s/get_test/%s/%s -o %s.sh" % (
            request_type, PrepID, nEvents, PrepID)
    # add "/N" to end of URL to get N events
    print get_test
    subprocess.call(get_test, shell=True)
    subprocess.call("chmod 755 %s.sh" % (PrepID), shell=True)
    return

def submitToBatch(PrepId):
    batch_command = "bsub -q 8nh %s.sh" % (PrepId)
    print batch_command
    output = subprocess.Popen(batch_command, stdout=subprocess.PIPE,
                              shell=True).communicate()[0]
    match = re.match('Job <(\d*)> is',output)
    jobID = match.group(1)
    return jobID

def createTest(compactPrepIDList, outputFile, nEvents):
    requests = parseIDList(compactPrepIDList)

    csvfile = csv.writer(open(outputFile, 'w'))
    csvfile.writerow(['PrepId','JobId','Time per event [s]'
                      'Size per event [kB]'])

    print "Testing %d requests" % (len(requests))
    for req in requests:
        getTestScript(req.getPrepId(), nEvents)
        jobID = submitToBatch(req.getPrepId())
        req.setJobID(jobID)
        csvfile.writerow([req.getPrepId(), req.getJobID(), "", ""])
    return

def extractTest(csvFile):
    return

def main():
    args = getArguments() # Setup flags and get arguments
    if args.ids and args.csv:
        print "Error: Cannot use both -i and -f."
        sys.exit(1)
    elif args.ids:
        createTest(args.ids,args.output,args.nEvents)
    elif args.csv:
        extractTest(args.csv)
    else:
        print "Error: Must use either -i or -f."
        sys.exit(2)

if __name__ == '__main__':
    main()
