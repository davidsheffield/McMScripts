#!/usr/bin/env python

################################
#
# getRequests.py
#
#  Script to get a list of requests from McM
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sys
import os.path
import argparse
import csv
import pprint
import time
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM
from requestClass import * # Load class to store request information


def getArguments():
    parser = argparse.ArgumentParser(description='Get a list of PrepIDs from McM based on a query.')

    # Command line flags
    parser.add_argument('query')
    parser.add_argument('-n', action='store_true', dest='isNew', help='Only get requests with unmodified time and size per event.')
    parser.add_argument('-c', action='store_true', dest='getChain', help='Return PrepID of chain.')

    args_ = parser.parse_args()
    return args_


def checkFile(file_):
    # Check that CSV file exists
    if not os.path.isfile(file_):
        print "Error: File %s does not exist." % file_
        print "Exiting with status 1."
        sys.exit(1)


def getPrepIDList(query_string, isNew, getChain):
    useDev = False
    mcm = restful( dev=useDev ) # Get McM connection
    print query_string
    req_list = mcm.getA('requests', query=query_string)

    out_list = []
    if req_list is None:
        print "\033[1;31mCould not get requests from McM\033[1;m"
    else:
        for req in req_list:
            if isNew:
                if req['time_event'] == -1 or req['size_event'] == -1:
                    continue
            if not getChain:
                out_list.append(req['prepid'])
            else:
                out_list.append(req['member_of_chain'][0])
    print "Found {0} requests".format(len(out_list))
    return out_list


def printList(list):
    print ""
    for i, PrepID in enumerate(list):
        if i == 0:
            sys.stdout.write(PrepID)
        else:
            sys.stdout.write(",{0}".format(PrepID))
    print "\n"
    return


def main():
    args = getArguments() # Setup flags and get arguments

    list = getPrepIDList(args.query, args.isNew, args.getChain)
    printList(list)

    return


if __name__ == '__main__':
    main()
