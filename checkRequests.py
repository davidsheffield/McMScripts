#!/usr/bin/env python

################################
#
# checkRequests.py
#
#  Script to check the status of requests
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sys
import os
import subprocess
import argparse
import csv
import pprint
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM


def getArguments():
    parser = argparse.ArgumentParser(description='Test McM requests.')

    # Command line flags
    parser.add_argument('ids', help=
                        'List of PrepIDs to be checked. Separate range by -.')

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
        requests.append("{0}-{1}-{2:05d}".format(pwg, campaign, number))
    return requests


def parseIDList(compactList):
    splitList = compactList.split(',')
    requests = []
    for subList in splitList:
        splitSubList = subList.split('-')
        if len(splitSubList) == 3:
            requests.append(subList)
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


def checkRequests(requests, useDev):
    mcm = restful(dev=useDev) # Get McM connection

    for PrepID in requests:
        base_req = mcm.getA('requests', PrepID)
        print "{0} {1}".format(PrepID, base_req['status'])

        for chainID in base_req['member_of_chain']:
            #print chainID
            chain_req = mcm.getA('chained_requests', chainID)
            space = ""
            for i, member in enumerate(chain_req['chain']):
                if i == 0:
                    continue
                space = space + " "
                req = mcm.getA('requests', member)
                print "{0}{1} {2}".format(space, member, req['status'])
        print ""
    return


def main():
    args = getArguments() # Setup flags and get arguments

    requests = parseIDList(args.ids)
    useDev = False
    checkRequests(requests, useDev)

    return


if __name__ == '__main__':
    main()
