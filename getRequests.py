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

class bcolors:
    MAGENTA = '\033[35m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    # RED = '\033[31m'
    YELLOW = '\033[33m'
    WHITE = '\033[1;37m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Gray_like_Ghost = '\033[1;30m'
    RED = '\033[1;31m' 
    Green_like_Grass = '\033[1;32m' 
    Yellow_like_Yolk = '\033[1;33m'
    Blue_like_Blood = '\033[1;34m'
    Magenta_like_Mimosa = '\033[1;35m'
    CYAN = '\033[1;36m'
    Crimson_like_Chianti = '\033[1;38m'
    Highlighted_Red_like_Radish = '\033[1;41m'
    Highlighted_Green_like_Grass = '\033[1;42m'
    Highlighted_Brown_like_Bear = '\033[1;43m'
    Highlighted_Blue_like_Blood = '\033[1;44m'
    Highlighted_Magenta_like_Mimosa = '\033[1;45m'
    Highlighted_Cyan_like_Caribbean = '\033[1;46m'
    Highlighted_Gray_like_Ghost = '\033[1;47m'
    Highlighted_Crimson_like_Chianti = '\033[1;48m'

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
    parser.add_argument('-listattr', dest='listAttr', type=int, default=-1,
                        help='List attributes for each PrepID. 0 (default) to 5 in increasing level of verbosity')
    parser.add_argument('-f', dest='format', type=int, default=0,
                        help='Format of output. 0 (default) = input for scripts, 1 = human-readable, 2 = HTML')

    args_ = parser.parse_args()
    return args_


def checkFile(file_):
    # Check that CSV file exists
    if not os.path.isfile(file_):
        print "Error: File {0} does not exist.".format(file_)
        sys.exit(1)


def getMcMlist(query_string,printout):
    useDev = False
    mcm = restful(dev=useDev) # Get McM connection
    if printout:
        print 'MCM query string: {0}{1}{2}'.format(bcolors.MAGENTA,
                                                   query_string, bcolors.ENDC)
    req_list = mcm.getA('requests', query=query_string)
    return req_list

def getPrepIDListWithAttributes(query_string,listAttr):
    req_list = getMcMlist(query_string,True)
    print '\n'
    print '======================================================================================================================================================================\n'
    for req in req_list:
        if listAttr > 5: # full dump of the request object, useful for debugging purpose
            print bcolors.MAGENTA +\
                  'prepid='+ bcolors.ENDC,req['prepid'],\
                  ''+ bcolors.ENDC
            print str(req).replace("u'",'')
            print ''
        else:
            # print '======================================================================================================================================================================\n',\
                  # '======================================================================================================================================================================'
            print bcolors.MAGENTA +\
                  'prepid='+ bcolors.ENDC,req['prepid'],\
                  ', '+bcolors.MAGENTA+'Dataset name='+ bcolors.ENDC,req['dataset_name'],\
                  ', '+bcolors.MAGENTA+'Extension='+ bcolors.ENDC,req['extension'],\
                  ', '+bcolors.MAGENTA+'Completed/Total events='+ bcolors.ENDC,str(req['completed_events'])+'/'+str(req['total_events']),\
                  ''+ bcolors.ENDC
            if listAttr > 0:
                print bcolors.RED +\
                      'Approval='+ bcolors.ENDC,req['approval'],\
                      ', '+bcolors.RED+'Status='+ bcolors.ENDC,req['status'],\
                      ', '+bcolors.RED+'Time Event='+ bcolors.ENDC,req['time_event'],\
                      ', '+bcolors.RED+'CMSSW Release='+ bcolors.ENDC,req['cmssw_release'],\
                      ', '+bcolors.RED+'Priority='+ bcolors.ENDC,req['priority'],\
                      ''+ bcolors.ENDC
            if listAttr > 1:
                if(len(req['generator_parameters'])>0):
                    print bcolors.GREEN +\
                        'Cross Section='+ bcolors.ENDC,req['generator_parameters'][0]['cross_section'],'pb',\
                        ', '+bcolors.GREEN+'Filter efficiency='+ bcolors.ENDC,str(req['generator_parameters'][0]['filter_efficiency'])+' +/- '+str(req['generator_parameters'][0]['filter_efficiency_error']),\
                        ', '+bcolors.GREEN+'Match efficiency='+ bcolors.ENDC,str(req['generator_parameters'][0]['match_efficiency'])+' +/- '+str(req['generator_parameters'][0]['match_efficiency_error']),\
                        ''+ bcolors.ENDC
                else:
                    print bcolors.GREEN +\
                        'Cross Section= -1 pb',\
                        ', Filter efficiency= -1',\
                        ', Match efficiency= -1',\
                        ''+ bcolors.ENDC
                print bcolors.CYAN +\
                      'Tags='+ bcolors.ENDC,str(req['tags']).replace("u'",'').replace("'",""),\
                      ', '+bcolors.CYAN+'Generators='+ bcolors.ENDC,req['name_of_fragment'],\
                      ', '+bcolors.CYAN+'Name of Fragment='+ bcolors.ENDC,req['name_of_fragment'],\
                      ', '+bcolors.CYAN+'Notes='+ bcolors.ENDC,req['notes'],\
                      ''+ bcolors.ENDC
            if listAttr > 2:
                print bcolors.BLUE +\
                      'Last Updater Name='+ bcolors.ENDC,req['history'][0]['updater']['author_name'],\
                      '(',req['history'][0]['updater']['author_email'],')',\
                      '\n'\
                      + bcolors.Gray_like_Ghost +\
                      'McM View Link= https://cms-pdmv.cern.ch/mcm/requests?shown=2199023255551&prepid='+req['prepid'],\
                      '\n'\
                      'McM Edit Link= https://cms-pdmv.cern.ch/mcm/edit?db_name=requests&prepid='+req['prepid'],\
                      ''+ bcolors.ENDC
            if listAttr > 3:
                print bcolors.YELLOW +\
                  'Member of chain(s)'
                for current_chain in req['member_of_chain']:
                    query_chains = "member_of_chain="+current_chain
                    # print "req['member_of_chain'][0]",query_chains
                    temp = sys.stdout
                    f = open('/dev/null', 'w')
                    sys.stdout = f
                    chained_prepIds=getMcMlist(query_chains,False)
                    sys.stdout = temp
                    prepid1 = []
                    for req1 in chained_prepIds:
                      prepid1.append(req1['prepid'])
                    print current_chain+" : "+ bcolors.ENDC+str(prepid1).strip('[]').replace("u'",'').replace("'","")
                    print bcolors.Gray_like_Ghost +\
                    'McM View Link= https://cms-pdmv.cern.ch/mcm/chained_requests?shown=4095&prepid='+current_chain,\
                    ''+ bcolors.YELLOW
            if listAttr > 4:
                print bcolors.WHITE +'Fragment code=\n'+\
                      bcolors.Gray_like_Ghost +\
                      req['fragment'],\
                      ''+ bcolors.ENDC
            print bcolors.ENDC
        
        print '======================================================================================================================================================================\n\n',\
        
def getPrepIDList(query_string, getNew, getForValidation, getChain):
    req_list = getMcMlist(query_string,True)

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

    print 'args.listAttr',args.listAttr
    if args.listAttr < 0:
        list = getPrepIDList(args.query, args.getNew, args.getForValidation,
                             args.getChain)
        printList(list, args.format)
    else:
        dict = getPrepIDListWithAttributes(args.query,args.listAttr)
        
    return


if __name__ == '__main__':
    main()
