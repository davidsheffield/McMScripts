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
import argparse
import csv
from requestClass import * # Load class to store request information

def getArguments():
    parser = argparse.ArgumentParser(description='Test McM requests.')

    # Command line flags
    parser.add_argument('-i', '--ids', dest='ids', help=
                        'List of PrepIDs to be tested. Separate range by >.')
    parser.add_argument('-f', '--file', dest='csv', help='Input CSV file.')
    parser.add_argument('-o', '--output', dest='output', default='test.csv',
                        help='Output CSV file')
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

def createTest(compactPrepIDList, outputFile):
    requests = parseIDList(compactPrepIDList)
    return

def extractTest(csvFile):
    return

def main():
    args = getArguments() # Setup flags and get arguments
    if args.ids and args.csv:
        print "Error: Cannot use both -i and -f."
        sys.exit(1)
    elif args.ids:
        createTest(args.ids,args.output)
    elif args.csv:
        extractTest(args.csv)
    else:
        print "Error: Must use either -i or -f."
        sys.exit(2)

if __name__ == '__main__':
    main()
