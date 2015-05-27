import sys
import os.path
import argparse
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM

def getArguments():
    parser = argparse.ArgumentParser(description='Validate chains in McM.')

    # Command line flags
    parser.add_argument('range', type=str, nargs=2, metavar='PrepID PrepID',
                        help='First and last PrepIDs to be validated.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0')

    args_ = parser.parse_args()
    return args_

def checkPrepIDs(first,last):
    firstList = first.split('-')
    lastList = last.split('-')

    shouldExit = False
    if firstList[0] != lastList[0]:
        print "PrepIDs must be for ethe same PWG."
        shouldExit = True
    if firstList[1] != lastList[1]:
        print "PrepIDs must be for the same campaign."
        shouldExit = True

    if shouldExit:
        sys.exit(1)
    elif firstList[2] > lastList[2]:
        print "The first PrepID must be smaller than the last PrepID."
        sys.exit(2)

def getChainList(PrepIDrange):
    checkPrepIDs(PrepIDrange[0],PrepIDrange[1])

    firstSplit = PrepIDrange[0].split('-')
    PrepIDList = []
    for number in  range(int(firstSplit[2]), int(PrepIDrange[1].split('-')[2])+1):
        PrepIDList.append("%s-%s-%05d" % (firstSplit[0], firstSplit[1], number))

    return PrepIDList

def validate(chains):
    mcm = restful(dev=False)

    print "Validating %d chained requests" % (len(chains))
    for PrepID in chains:
        url = 'restapi/chained_requests/test/%s' % (PrepID)
        chain_output = mcm.get(url)

        if chain_output['results']:
            print "%s validating" % (PrepID)
        else:
            print "%s will not be validated, due to the following reason: \n    %s" % (PrepID,chain_output['message'])

def main():
    args = getArguments()             # Setup flags and get arguments
    chains = getChainList(args.range) # Get list of chains and check args
    validate(chains)                  # Tell McM to validate chains

if __name__ == '__main__':
    main()
