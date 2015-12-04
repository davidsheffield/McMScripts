#!/usr/bin/env python

################################
#
# BulkCopyToSummer15GS.py
#
#  Script to copy requests from RunIIWinter15GS to RunIISummer15GS
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


def copyRequestContents(request_list):
    mcm = restful(dev=False) # Get McM connection

    csvfile = csv.writer(open('failed.csv', 'w'))
    csvfile.writerow(['Winter15 PrepID', 'Dataset name', 'Reason'])

    for PrepID in request_list:
        time.sleep(0.2)
        winter_req = mcm.getA('requests', PrepID)

        query_string = "dataset_name={0}&member_of_campaign=RunIISummer15GS".format(
            winter_req['dataset_name'])
        failted_to_get = True
        for tries in range(3):
            time.sleep(0.2)
            summer_req_list = mcm.getA('requests', query=query_string)
            if summer_req_list is not None:
                failed_to_get = False
                break
        if failed_to_get:
            print "\033[0;31m{0} modification failed from {1}. Could not get request from McM.\033[0;m".format(
                winter_req['dataset_name'], PrepID)
            csvfile.writerow([PrepID, winter_req['dataset_name'],
                              'Could not get request'])
            continue
        if len(summer_req_list) > 1:
            print "\033[0;31m{0} modification failed from {1}. Too many requests match query.\033[0;m".format(
                winter_req['dataset_name'], PrepID)
            csvfile.writerow([PrepID, winter_req['dataset_name'],
                              'Too many matches'])
            continue
        elif len(summer_req_list) == 0:
            print "\033[0;31m{0} modification failed from {1}. No requests match query.\033[0;m".format(
                winter_req['dataset_name'], PrepID)
            csvfile.writerow([PrepID, winter_req['dataset_name'],
                              'No matches'])
            continue

        summer_req = summer_req_list[0]

        if summer_req['approval'] != 'none' or summer_req['status'] != 'new':
            print "\033[0;34m{0} from {1} not new\033[0;m".format(
                summer_req['prepid'], PrepID)
            continue

        summer_req['generator_parameters'] = [{'match_efficiency_error': winter_req['generator_parameters'][0]['match_efficiency_error'],
                                               'match_efficiency': winter_req['generator_parameters'][0]['match_efficiency'],
                                               'filter_efficiency': winter_req['generator_parameters'][0]['filter_efficiency'],
                                               'version': 0,
                                               'cross_section': winter_req['generator_parameters'][0]['cross_section'],
                                               'filter_efficiency_error': winter_req['generator_parameters'][0]['filter_efficiency_error']}]
        summer_req['generators'] = winter_req['generators']
        summer_req['name_of_fragment'] = winter_req['name_of_fragment']
        summer_req['fragment_tag'] = winter_req['fragment_tag']
        summer_req['time_event'] = winter_req['time_event']
        summer_req['size_event'] = winter_req['size_event']
        summer_req['mcdb_id'] = winter_req['mcdb_id']

        answer = mcm.updateA('requests', summer_req) # Update request
        if answer['results']:
            print "\033[0;32m{0} modified from {1} {2}\033[0;m".format(
                summer_req['prepid'], PrepID, summer_req['dataset_name'])
        else:
            print "\033[0;31m{0} failed to be modified from {1}\033[0;m".format(
                summer_req['prepid'], PrepID)
            csvfile.writerow([PrepID, winter_req['dataset_name'],
                              'Failed to modify {0}'.format(summer_req['prepid'])])

    return


def main():
    args = getArguments() # Setup flags and get arguments
    request_list = parseIDList(args.ids)

    copyRequestContents(request_list)

    return


if __name__ == '__main__':
    main()
