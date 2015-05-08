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

def createTest(compactPrepIDList, outputFile):
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
