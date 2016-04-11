#!/usr/bin/env python

################################
#
# makeTicket.py
#
#  Script to create tickets for MCCM.
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sys
import argparse
import pprint
import mcmscripts_config
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM


def getArguments():
    parser = argparse.ArgumentParser(
        description='Script to creat tickets in McM.')

    # Command line flags
    parser.add_argument('-i', '--ids', dest='ids', help='List of PrepIDs.')
    parser.add_argument('-p', '--pwg', action='store', dest='pwg',
                        default=mcmscripts_config.pwg,
                        help='Set PWG. Defaults to %(default)s. Change default in config.py')
    parser.add_argument('-c', '--chain', action='store', dest='chain',
                        metavar='name', help='Set chain.')
    parser.add_argument('-b', '--block', action='store', dest='block', type=int,
                        default=3, help='Set block.')
    parser.add_argument('-r', '--repititions', action='store',
                        dest='repititions', type=int, default=1,
                        help='Number of chains.')
    parser.add_argument('-s', '--staged', dest='staged', action='store',
                        type=int, default=0, help='Number of events needed.')

    args_ = parser.parse_args()
    return args_


def interrogate():
    loop = True
    while loop:
        chain = raw_input("Chain: ")
        block = raw_input("Block: ")
        repititions = raw_input("Repititions: ")
        staged = raw_input("Staged: ")

        yn = raw_input("Are these acceptable? [y/n] ")
        while True:
            if yn.lower() in ["y", "yes"]:
                loop = False
                break
            elif yn.lower() in ["n", "no"]:
                break
            else:
                yn = raw_input('Please enter "yes" or "no". ')

    return [chain, block, repititions, staged]


def formatIDRange(pwg, campaign, first, last):
    first = int(first)
    last = int(last)
    if first > last:
        print "Error: PrepID range out of order. {0}-{1}-{2:05d} > {0}-{1}-{3:05d}".format(
            pwg, campaign, first, last)
        sys.exit(3)

    return ['{0}-{1}-{2:05d}'.format(pwg, campaign, first),
            '{0}-{1}-{2:05d}'.format(pwg, campaign, last)]


def parseIDList(compactList):
    splitList = compactList.split(',')
    requests = []
    for subList in splitList:
        splitSubList = subList.split('-')
        if len(splitSubList) == 3:
            requests.append(subList)
        elif len(splitSubList) == 4:
            requests.append(formatIDRange(splitSubList[0], splitSubList[1],
                                          splitSubList[2], splitSubList[3]))
        elif len(splitSubList) == 6:
            if splitSubList[0] != splitSubList[3]:
                print "Error: PrepID range must be for the same PWG."
                sys.exit(2)
            if splitSubList[1] != splitSubList[4]:
                print "Error: PrepID range must be for the same campaign."
                sys.exit(2)
            requests.append(formatIDRange(splitSubList[0], splitSubList[1],
                                          splitSubList[2], splitSubList[5]))
        else:
            print "Error: Poorly formed PrepID list."
            sys.exit(1)
    return requests


def createTicket(requests, pwg, chain, block, repititions, staged):
    mcm = restful(dev=False)
    ticket = {'prepid': pwg, 'pwg': pwg, 'block': block,
              'chains': [chain], 'repetitions': repititions,
              'requests': requests
              }

    pprint.pprint(ticket)

    # ticket = {'prepid': 'EXO', 'pwg': 'EXO', 'block': 2,
    #           'chains': ['RunIISpring16DR80PU2016MiniAODv1'], 'repetitions': 1,
    #           'requests': [['EXO-RunIISummer15GS-00435', 'EXO-RunIISummer15GS-00509'], ['EXO-RunIISummer15GS-06132', 'EXO-RunIISummer15GS-06139']]
    #           }
    # ticket = {'prepid': 'EXO', 'pwg': 'EXO', 'block': 2,
    #           'chains': ['RunIISpring16DR80PU2016MiniAODv1wmLHE'], 'repetitions': 1,
    #           'notes': 'For B2G',
    #           'requests': ['EXO-RunIIWinter15wmLHE-00288']
    #                         }

    answer = mcm.putA('mccms', ticket)
    if answer['results']:
        print "Created {0}".format(answer['prepid'])
    else:
        print "Failed"

    return


def modifyTicket():
    mcm = restful(dev=False)
    ticket = mcm.getA('mccms', 'EXO-2016Mar30-00024')
    #ticket['block'] = 2
    #ticket['chains'] = ['RunIISpring16DR80PU2016MiniAODv1']
    #ticket['chains'] = ['RunIISpring16DR80PU2016MiniAODv1wmLHE']
    #ticket['repetitions'] = 1
    #ticket['requests'] = [['EXO-RunIIWinter15wmLHE-01572',
    pprint.pprint(ticket)

    # answer = mcm.updateA('mccms', ticket)
    # print answer
    # if answer['results']:
    #     print "Modified"
    # else:
    #      print "Failed"

    return


def main():
    args = getArguments() # Setup flags and get arguments

    (args.chain, args.block, args.repititions, args.staged) = interrogate()

    requests = parseIDList(args.ids)
    print requests

    createTicket(requests, args.pwg, args.chain, args.block, args.repititions,
                 args.staged)
    return


if __name__ == '__main__':
    main()
