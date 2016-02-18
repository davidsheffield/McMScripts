#!/usr/bin/env python

################################
#
# addTags.py
#
#  Script to add tags to old requests.
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
        description='Tag old requests.')

    # Command line flags
    parser.add_argument('ids', metavar='PrepIDs',
                        help='List of PrepIDs to tag copies of.')
    parser.add_argument('tag', metavar='Tag')

    args_ = parser.parse_args()
    return args_


def fillIDRange(pwg, campaign, first, last):
    first = int(first)
    last = int(last)
    chains = []
    if first > last:
        print "Error: PrepID range out of order. {0}-{1}-{2:05d} > {0}-{1}-{3:05d}".format(
            pwg, campaign, first, last)
        sys.exit(1)

    for number in range(first, last+1):
        chains.append("{0}-{1}-{2:05d}".format(pwg, campaign, number))
    return chains


def parseIDList(compactList):
    splitList = compactList.split(',')
    chains = []
    for subList in splitList:
        splitSubList = subList.split('-')
        if len(splitSubList) == 3:
            chains.append(subList)
        elif len(splitSubList) == 4:
            chains += fillIDRange(splitSubList[0], splitSubList[1],
                                  splitSubList[2], splitSubList[3])
        elif len(splitSubList) == 6:
            if splitSubList[0] != splitSubList[3]:
                print "Error: PrepID range must be for the same PWG."
                sys.exit(1)
            if splitSubList[1] != splitSubList[4]:
                print "Error: PrepID range must be for the same chained campaign."
                sys.exit(1)
            chains += fillIDRange(splitSubList[0], splitSubList[1],
                                  splitSubList[2], splitSubList[5])
        else:
            print "Error: Poorly formed PrepID list."
            sys.exit(1)
    return chains


def modifyRequest(mcm, req, tag):
    for existing in req['tags']:
        if existing.startswith("EXO"):
            print "  \033[0;33m{0} has already been tagged with {1}\033[0;m".format(req['prepid'], existing)
            return
    req['tags'] += [tag]
    answer = mcm.updateA('requests', req) # Update request
    if answer['results']:
        print "  \033[0;32m{0} tagged {1}\033[0;m".format(req['prepid'], tag)
    else:
        print "  \033[0;32m{0} not tagged\033[0;m".format(req['prepid'])
    return


def tagRequests(prepids, tag):
    mcm = restful(dev=False)
    campaigns = ['RunIISummer15GS', 'RunIIFall15DR76', 'RunIIFall15MiniAODv1',
                 'RunIIFall15MiniAODv2']

    num = len(prepids)
    counter = 0

    for prepid in prepids:
        counter += 1
        time.sleep(1.0)
        req = mcm.getA('requests', prepid)
        print "{0}/{1} {2} {3}".format(counter, num, prepid, req['dataset_name'])
        if req['member_of_campaign'] == "RunIIWinter15wmLHE"\
                or req['member_of_campaign'] == "RunIIWinter15pLHE":
            modifyRequest(mcm, req, tag)
        dataset_name = req['dataset_name']
        for campaign in campaigns:
            query_string = "dataset_name={0}&member_of_campaign={1}".format(
                dataset_name, campaign)
            failed_to_get = True
            for tries in range(3):
                time.sleep(0.5)
                req_list = mcm.getA('requests', query=query_string)
                if req_list is not None:
                    failed_to_get = False
                    break
            if failed_to_get:
                print "  \033[0;31mCould not find {0} in {1}\033[0;m".format(
                    dataset_name, campaign)
                continue
            if len(req_list) > 1:
                print "  \033[0;31m{0} has too many requests in {1}\033[0;m".format(
                    dataset_name, campaign)
                continue
            if len(req_list) == 0:
                print "  \033[0;31m{0} does not exist in {1}\033[0;m".format(
                    dataset_name, campaign)
                continue
            req = req_list[0]
            modifyRequest(mcm, req, tag)
    return


def main():
    args = getArguments()
    prepids = parseIDList(args.ids)
    print "Tagging {0} base requests".format(len(prepids))
    tagRequests(prepids, args.tag)


if __name__ == '__main__':
    main()
