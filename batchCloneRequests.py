#!/usr/bin/env python

################################
#
# batchCloneRequests.py
#
#  Script to clone multiple McM requests.
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sys
import os.path
import argparse
import time
import mcmscripts_config
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM


def getArguments():
    parser = argparse.ArgumentParser(
        description='Clone multiple McM requests.')

    # Command line flags
    parser.add_argument('-i', '--ids', dest='ids', help=
                        'List of PrepIDs to be cloned.')
    parser.add_argument('-c', '--campaign', action='store', dest='campaign',
                        metavar='name', help='Set member_of_campaign.')

    args_ = parser.parse_args()
    return args_


def fillIDRange(pwg, campaign, first, last):
    first = int(first)
    last = int(last)
    requests = []
    if first > last:
        print "Error: PrepID range out of order. {0}-{1}-{2:05d} > {0}-{1}-{3:05d}".format(
            pwg, campaign, first, last)
        sys.exit(1)

    for number in range(first, last+1):
        requests.append("{0}-{1}-{2:05d}".format(pwg, campaign, number))
    return requests


def parseIDList(compactList):
    print compactList
    splitList = compactList.split(',')
    requests = []
    for subList in splitList:
        splitSubList = subList.split('-')
        if len(splitSubList) == 3:
            requests.append(subList)
        elif len(splitSubList) == 4:
            requests += fillIDRange(splitSubList[0], splitSubList[1],
                                    splitSubList[2], splitSubList[3])
        elif len(splitSubList) == 6:
            if splitSubList[0] != splitSubList[3]:
                print "Error: PrepID range must be for the same PWG."
                sys.exit(1)
            if splitSubList[1] != splitSubList[4]:
                print "Error: PrepID range must be for the same chained campaign."
                sys.exit(1)
            requests += fillIDRange(splitSubList[0], splitSubList[1],
                                    splitSubList[2], splitSubList[5])
        else:
            print "Error: Poorly formed PrepID list."
            sys.exit(1)
    return requests


def cloneRequests(requests, campaign):
    # Create new requests be cloning an old one based on PrepId
    useDev = False
    mcm = restful(dev=useDev) # Get McM connection

    print "Adding {0} requests to McM using clone.".format(len(requests))
    for PrepID in requests:
        clone_req = mcm.getA('requests', PrepID) # Get request to clone
        clone_req['member_of_campaign'] = campaign
        answer = mcm.clone(PrepID, clone_req) # Clone request
        if answer['results']:
            print "\033[0;32m{0} cloned from {1}\033[0;m".format(
                answer['prepid'], PrepID)
        else:
            print "\033[0;31m{0} failed to be cloned to {1}\033[0;m".format(
                PrepID, campaign)
        time.sleep(0.5)


def main():
    args = getArguments() # Setup flags and get arguments

    requests = parseIDList(args.ids)
    cloneRequests(requests, args.campaign)


if __name__ == '__main__':
    main()
