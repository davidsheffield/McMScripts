#!/usr/bin/env python

################################
#
# CheckDataset.py
#
#  Check whether input datasets are only on tape
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
import subprocess
import json
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM
from requestClass import * # Load class to store request information

def getArguments():
    parser = argparse.ArgumentParser(
        description='Script to copy requests.')

    parser.add_argument('ids', metavar='PrepIDs',
                        help='List of PrepIDs to copy to RunIISummer15GS.')

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


def getInputDatasets(request_list):
    mcm = restful(dev=False) # Get McM connection

    csvfile = csv.writer(open("datasets_on_tape.csv", 'w'))
    csvfile.writerow(['PrepID', 'Input dataset'])

    for PrepID in request_list:
        is_on_disk = False
        time.sleep(0.2)
        req = mcm.getA('requests', PrepID)

        if req is None:
            print "\033[0;31mCould not get {0} from McM.\033[0;m".format(PrepID)
            continue

        out = subprocess.check_output(['das_client.py', '--format=json',
                                       '--query=site dataset={0}'.format(req['input_dataset'])])
        out_dict = json.loads(out)

        for sites in out_dict['data']:
            for site in sites['site']:
                if 'kind' in site:
                    if site['kind'] == 'Disk':
                        is_on_disk = True

        if is_on_disk:
            print "\033[0;32m{0}'s input dataset on disk.\033[0;m".format(PrepID)
        else:
            csvfile.writerow([PrepID, req['input_dataset']])
            print "\033[0;31m{0}'s input dataset not on disk.\033[0;m".format(PrepID)

    return


def main():
    args = getArguments() # Setup flags and get arguments
    request_list = parseIDList(args.ids)

    getInputDatasets(request_list)

    return


if __name__ == '__main__':
    main()
