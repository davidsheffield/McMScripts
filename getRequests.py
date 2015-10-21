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
    parser = argparse.ArgumentParser(
        description='Get a list of PrepIDs from McM based on a query.')

    # Command line flags
    parser.add_argument('query')
    parser.add_argument('-n', action='store_true', dest='getNew',
                        help='Only get requests with unmodified time and size per event.')
    parser.add_argument('-v', action='store_true', dest='getForValidation',
                        help='Only get requests with positive time and size per event.')
    parser.add_argument('-c', action='store_true', dest='getChain',
                        help='Return PrepID of chain.')
    parser.add_argument('-f', dest='format', type=int, default=0,
                        help='Format of output. 0 (default) = input for scripts, 1 = human-readable, 2 = HTML')

    args_ = parser.parse_args()
    return args_


def checkFile(file_):
    # Check that CSV file exists
    if not os.path.isfile(file_):
        print "Error: File {0} does not exist.".format(file_)
        sys.exit(1)


def getPrepIDList(query_string, getNew, getForValidation, getChain):
    useDev = False
    mcm = restful(dev=useDev) # Get McM connection
    print query_string
    req_list = mcm.getA('requests', query=query_string)

    event_sum = 0
    out_list = []
    if req_list is None:
        print "\033[1;31mCould not get requests from McM\033[1;m"
    else:
        for req in req_list:
            if getNew:
                if req['time_event'] != -1 or req['size_event'] != -1:
                    continue
            if getForValidation:
                if req['time_event'] <= 0 or req['size_event'] <= 0:
                    continue
            if not getChain:
                out_list.append(req['prepid'])
                event_sum += req['total_events']
            else:
                out_list.append(req['member_of_chain'][0])
    print "Found {0} requests with {1}M events".format(len(out_list),
                                                       event_sum/1e6)
    return out_list


def isSequential(lastID, currentID):
    last = lastID.split('-')
    current = currentID.split('-')

    if len(last) == 3 and len(current) == 3:
        if last[0] == current[0] and last[1] == current[1] \
                and int(last[2]) + 1 == int(current[2]):
            return True
    return False


def printList(list, format):
    arrow = "-"
    comma = ","
    if format == 1:
        arrow = " ---> "
        comma = ", "
    elif format == 2:
        arrow = " ---> "
        comma = "<br>"

    lastID = "FIRST"
    print_last = False
    last_index = len(list) - 1
    print ""
    for i, PrepID in enumerate(list):
        if isSequential(lastID, PrepID):
            if i < last_index:
                print_last = True
            else:
                sys.stdout.write("{0}{1}".format(arrow, PrepID))
        else:
            if print_last:
                sys.stdout.write("{0}{1}{2}{3}".format(arrow, lastID, comma,
                                                     PrepID))
            elif i > 0:
                sys.stdout.write("{0}{1}".format(comma, PrepID))
            else:
                sys.stdout.write("{0}".format(PrepID))
            print_last = False
        lastID = PrepID
    print "\n"
    return


def main():
    args = getArguments() # Setup flags and get arguments

    list = getPrepIDList(args.query, args.getNew, args.getForValidation,
                         args.getChain)
    printList(list, args.format)

    return


if __name__ == '__main__':
    main()
