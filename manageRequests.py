#!/usr/bin/env python
import sys
import os.path
import argparse
import csv
import pprint
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import * # Load class to access McM
from requestClass import *

def getArguments():
    defaultPWG = 'XXX'

    parser = argparse.ArgumentParser(description='Create McM requests.')

    parser.add_argument('file_in')
    parser.add_argument('-c', '--campaign', action='store', dest='campaign', metavar='name', help='Set member_of_campaign.')
    parser.add_argument('-p', '--pwg', action='store', dest='pwg', default=defaultPWG, help='Set PWG. Defaults to %(default)s. Change the variable defaultPWG to your PWG.')
    parser.add_argument('-m', '--modify', action='store_true', dest='doModify', help='Modify existing requests. The CSV file must contain the PrepIds of the requests to modify.')
    parser.add_argument('--clone', action='store', dest='cloneId', default='', help='Clone request.')
    parser.add_argument('-d', '--dry', action='store_true', dest='doDryRun', help='Dry run on result. Does not add requests to McM.')
    parser.add_argument('--dev', action='store_true', dest='useDev', help='Use dev/test instance.')
    parser.add_argument('--version', action='version', version='%(prog)s v0.1')
    
    args_ = parser.parse_args()
    return args_

def checkFile(file_):
    if not os.path.isfile(file_):
        print "Error: File %s does not exist." % file_
        print "Exiting with status 1."
        sys.exit(1)

def checkPWG(pwg_):
    pwg_list = ['B2G','BPH','BTW','EGM','EWK','EXO','FSQ','FWD','HCA','HIG','HIN','JME','L1T','MUO','QCD','SMP','SUS','TAU','TOP','TRK','TSG']
    if pwg_ not in pwg_list:
        print "Error: %s is not a recognized PWG." % pwg_
        if pwg_ == 'XXX':
            print "Change the default value for flag -p to your PWG."
        sys.stdout.write("Options are:")
        for iPWG in pwg_list:
            sys.stdout.write(" ")
            sys.stdout.write(iPWG)
        sys.stdout.write("\n")
        print "Exiting with status 2."
        sys.exit(2)

def checkNotCreate(doModify_,cloneId_):
    doClone = False
    if cloneId_ != "": doClone = True
    if doModify_ and doClone:
        print "Error: cannot both --modify and --clone."
        print "Exiting with status 6."
        sys.exit(6)
    return doModify_ or doClone

def exitDuplicateField(file_in_,field_):
    print "Error: File %s contains multiple instances of the field %s" % (file_in_,field_)
    print "Exiting with status 3."
    sys.exit(3)

def getFields(csvfile_,file_in_):
    list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    header = csv.reader(csvfile_).next()
    for ind, field in enumerate(header):
        if field in ['Dataset name','Dataset Name','Dataset','dataset']:
            if list[0] > -1: exitDuplicateField(file_in_,"Dataset Name")
            list[0] = ind
        elif field in ['EOS','eos','Eos','MCDBID','mcdbid']:
            if list[1] > -1: exitDuplicateField(file_in_,"EOS")
            list[1] = ind
        elif field in ['Cross section','Cross section [pb]','Cross section (pb)','Cross Section','Cross Section [pb]','Cross Section (pb)','CS','CS [pb]','CS (pb)','Xsec','Xsec [pb]','Xsec (pb)']:
            if list[2] > -1: exitDuplicateField(file_in_,"Cross Section")
            list[2] = ind
        elif field in ['Total Events','Total events','Events','events','total events','Number of Events']:
            if list[3] > -1: exitDuplicateField(file_in_,"Total Events")
            list[3] = ind
        elif field in ['Fragment name','Fragment Name','Generator fragment name','Generator Fragment Name','Fragment','fragment']:
            if list[4] > -1: exitDuplicateField(file_in_,"Generator Fragment Name")
            list[4] = ind
        elif field in ['Time per event','Time per event [s]','Time per event (s)','Time per Event','Time per Event [s]','Time per Event (s)','Time','Time [s]','Time (s)','time','time [s]','time (s)']:
            if list[5] > -1: exitDuplicateField(file_in_,"Time per Event")
            list[5] = ind
        elif field in ['Size per event','Size per event [kB]','Size per event (kB)','Size per Event','Size per Event [kB]','Size per Event (kB)','size','size [kB]','size (kB)']:
            if list[6] > -1: exitDuplicateField(file_in_,"Size per Event")
            list[6] = ind
        elif field in ['Tag','tag','Fragment Tag','Fragment tag','fragment tag','sha','SHA','SHA-1','sha-1']:
            if list[7] > -1: exitDuplicateField(file_in_,"Fragment Tag")
            list[7] = ind
        elif field in ['Generator','generator']:
            if list[8] > -1: exitDuplicateField(file_in_,"Generator")
            list[8] = ind
        elif field in ['Filter Efficiency','Filter efficiency','filter efficiency']:
            if list[9] > -1: exitDuplicateField(file_in_,"Filter Efficiency")
            list[9] = ind
        elif field in ['Filter Efficiency Error','Filter efficiency error','filter efficiency error']:
            if list[10] > -1: exitDuplicateField(file_in_,"Filter Efficiency Error")
            list[10] = ind
        elif field in ['Match Efficiency','Match efficiency','match efficiency']:
            if list[11] > -1: exitDuplicateField(file_in_,"Match Efficiency")
            list[11] = ind
        elif field in ['Match Efficiency Error','Match efficiency error','match efficiency error']:
            if list[12] > -1: exitDuplicateField(file_in_,"Match Efficiency Error")
            list[12] = ind
        elif field in ['PWG','pwg']:
            if list[13] > -1: exitDuplicateField(file_in_,"PWG")
            list[13] = ind
        elif field in ['Campaign','campaign','Member of Campaign','Member of campaign','member of campaign']:
            if list[14] > -1: exitDuplicateField(file_in_,"Member of Campaign")
            list[14] = ind
        elif field in ['PrepId','PrepID','PREPID','prepid']:
            if list[15] > -1: exitDuplicateField(file_in_,"PrepId")
            list[15] = ind
        else:
            print "Error: The field %s is not valid." % field
            print "Exiting with status 4."
            sys.exit(4)

    return list

def formatFragment(file_,campaign_):
    if len(file_.split("/")) > 1:
        return file_
    elif campaign_ in ['Summer12']:
        return "Configuration/GenProduction/python/EightTeV/"+file_
    elif campaign_ in ['Fall13','RunIIFall14GS']:
        return "Configuration/GenProduction/python/ThirteenTeV/"+file_
    else:
        print "Error: Cannot determine energy of campaign %s." % campaign_
        print "Exiting with status 5."
        sys.exit(5)

def fillFields(csvfile, fields, campaign, PWG, notCreate_):
    requests = []
    num_requests = 0
    for row in csv.reader(csvfile):
        num_requests += 1
        tmpReq = Request()
        if fields[0] > -1: tmpReq.setDataSetName(row[fields[0]])
        if fields[1] > -1:
            tmpReq.setMCDBID(row[fields[1]])
        elif not notCreate_:
            tmpReq.setMCDBID(-1)
        if fields[2] > -1:
            tmpReq.setCS(row[fields[2]])
        elif not notCreate_:
            tmpReq.setCS(1.0)
        if fields[3] > -1: tmpReq.setEvts(row[fields[3]])
        if fields[4] > -1: tmpReq.setFrag(formatFragment(row[fields[4]],campaign))
        if fields[5] > -1: tmpReq.setTime(row[fields[5]])
        if fields[6] > -1: tmpReq.setSize(row[fields[6]])
        if fields[7] > -1: tmpReq.setTag(row[fields[7]])
        if fields[8] > -1: tmpReq.setGen(row[fields[8]].split(" "))
        if fields[9] > -1:
            tmpReq.setFiltEff(row[fields[9]])
        elif not notCreate_:
            tmpReq.setFiltEff(1.0)
        if fields[10] > -1:
            tmpReq.setFiltEffErr(row[fields[10]])
        elif not notCreate_:
            tmpReq.setFiltEffErr(0.0)
        if fields[11] > -1:
            tmpReq.setMatchEff(row[fields[11]])
        elif not notCreate_:
            tmpReq.setMatchEff(1.0)
        if fields[12] > -1:
            tmpReq.setMatchEffErr(row[fields[12]])
        elif not notCreate_:
            tmpReq.setMatchEffErr(0.0)
        if fields[13] > -1:
            tmpReq.setPWG(row[fields[13]])
        elif not notCreate_:
            tmpReq.setPWG(PWG)
        if fields[14] > -1:
            tmpReq.setCamp(row[fields[14]])
        elif not notCreate_:
            tmpReq.setCamp(campaign)
        if fields[15] > -1:
            tmpReq.setPrepId(row[fields[15]])
        requests.append(tmpReq)
    return requests, num_requests

def createRequests(requests, num_requests, doDryRun, useDev):
    mcm = restful( dev=useDev ) # Get McM connection

    if not doDryRun:
        print "Adding %d requests to McM" % num_requests
    else:
        print "Dry run. %d requests will not be added to McM" % num_requests 
    for reqFields in requests:
        if not reqFields.useCamp():
            print "Campaign is missing."
            continue

        new_req = {'pwg':reqFields.getPWG(),'member_of_campaign':reqFields.getCamp(),'mcdb_id':reqFields.getMCDBID()}
        if reqFields.useDataSetName(): new_req['dataset_name'] = reqFields.getDataSetName()
        if reqFields.useEvts(): new_req['total_events'] = reqFields.getEvts()
        if reqFields.useFrag(): new_req['name_of_fragment'] = reqFields.getFrag()
        if reqFields.useTime(): new_req['time_event'] = reqFields.getTime()
        if reqFields.useSize(): new_req['size_event'] = reqFields.getSize()
        if reqFields.useTag(): new_req['fragment_tag'] = reqFields.getTag()
        if reqFields.useGen(): new_req['generators'] = reqFields.getGen()
        
        if not doDryRun:
            answer = mcm.putA('requests', new_req)
            if answer['results']:
                mod_req = mcm.getA('requests',answer['prepid'])
                # Add generator parameters
                mod_req['generator_parameters'][0]['cross_section'] = reqFields.getCS()
                mod_req['generator_parameters'][0]['filter_efficiency'] = reqFields.getFiltEff()
                mod_req['generator_parameters'][0]['filter_efficiency_error'] = reqFields.getFiltEffErr()
                mod_req['generator_parameters'][0]['match_efficiency'] = reqFields.getMatchEff()
                mod_req['generator_parameters'][0]['match_efficiency_error'] = reqFields.getMatchEffErr()
                update_answer = mcm.updateA('requests',mod_req) # Update request with generator parameters
                if update_answer['results']:
                    print answer['prepid'],"created"
                else:
                    print answer['prepid'],"created but generator parameters not set"
            else:
                print reqFields.getDataSetName(),"failed to be created"
        else:
            print reqFields.getDataSetName(),"not created"
            pprint.pprint(new_req)

def modifyRequests(requests, num_requests, doDryRun, useDev):
    mcm = restful( dev=useDev ) # Get McM connection

    if not doDryRun:
        print "Modifying %d requests to McM" % num_requests
    else:
        print "Dry run. %d requests will not be modified in McM" % num_requests
    for reqFields in requests:
        if not reqFields.usePrepId():
            print "PrepId is missing."
            continue
        
        mod_req = mcm.getA('requests',reqFields.getPrepId())
        if reqFields.useDataSetName(): mod_req['dataset_name'] = reqFields.getDataSetName()
        if reqFields.useMCDBID(): mod_req['mcdb_id'] = reqFields.getMCDBID()
        if reqFields.useEvts(): mod_req['total_events'] = reqFields.getEvts()
        if reqFields.useFrag(): mod_req['name_of_fragment'] = reqFields.getFrag()
        if reqFields.useTime(): mod_req['time_event'] = reqFields.getTime()
        if reqFields.useSize(): mod_req['size_event'] = reqFields.getSize()
        if reqFields.useTag(): mod_req['fragment_tag'] = reqFields.getTag()
        if reqFields.useGen(): mod_req['generators'] = reqFields.getGen()
        if reqFields.useCS(): mod_req['generator_parameters'][0]['cross_section'] = reqFields.getCS()
        if reqFields.useFiltEff(): mod_req['generator_parameters'][0]['filter_efficiency'] = reqFields.getFiltEff()
        if reqFields.useFiltEffErr(): mod_req['generator_parameters'][0]['filter_efficiency_error'] = reqFields.getFiltEffErr()
        if reqFields.useMatchEff(): mod_req['generator_parameters'][0]['match_efficiency'] = reqFields.getMatchEff()
        if reqFields.useMatchEffErr(): mod_req['generator_parameters'][0]['match_efficiency_error'] = reqFields.getMatchEffErr()

        if not doDryRun:
            answer = mcm.updateA('requests',mod_req) # Update request
            pprint.pprint(answer)
            if answer['results']:
                print reqFields.getPrepId(),"modified"
            else:
                print reqFields.getPrepId(),"failed to be modified"
        else:
            print reqFields.getPrepId(),"not modified"
            pprint.pprint(mod_req)

def cloneRequests(requests, num_requests, doDryRun, useDev, cloneId_):
    mcm = restful( dev=useDev ) # Get McM connection

    if not doDryRun:
        print "Adding %d requests to McM with clone" % num_requests
    else:
        print "Dry run. %d requests will not be add with clone to McM" % num_requests
    for reqFields in requests:
        clone_req = mcm.getA('requests',cloneId_)
        if reqFields.useDataSetName(): clone_req['dataset_name'] = reqFields.getDataSetName()
        if reqFields.useMCDBID(): clone_req['mcdb_id'] = reqFields.getMCDBID()
        if reqFields.useEvts(): clone_req['total_events'] = reqFields.getEvts()
        if reqFields.useFrag(): clone_req['name_of_fragment'] = reqFields.getFrag()
        if reqFields.useTime(): clone_req['time_event'] = reqFields.getTime()
        if reqFields.useSize(): clone_req['size_event'] = reqFields.getSize()
        if reqFields.useTag(): clone_req['fragment_tag'] = reqFields.getTag()
        if reqFields.useGen(): clone_req['generators'] = reqFields.getGen()
        if reqFields.useCS(): clone_req['generator_parameters'][0]['cross_section'] = reqFields.getCS()
        if reqFields.useFiltEff(): clone_req['generator_parameters'][0]['filter_efficiency'] = reqFields.getFiltEff()
        if reqFields.useFiltEffErr(): clone_req['generator_parameters'][0]['filter_efficiency_error'] = reqFields.getFiltEffErr()
        if reqFields.useMatchEff(): clone_req['generator_parameters'][0]['match_efficiency'] = reqFields.getMatchEff()
        if reqFields.useMatchEffErr(): clone_req['generator_parameters'][0]['match_efficiency_error'] = reqFields.getMatchEffErr()

        if not doDryRun:
            answer = mcm.clone(cloneId_,clone_req) # Clone request
            pprint.pprint(answer)
            if answer['results']:
                newId = answer['prepid']
                print newId,"created with clone"
            else:
                print reqFields.getDataSetName(),"failed to be created with clone"
        else:
            print reqFields.getDataSetName(),"not created with clone"
            pprint.pprint(clone_req)

def main():
    args = getArguments()
    checkPWG(args.pwg)
    notCreate = checkNotCreate(args.doModify,args.cloneId)
    checkFile(args.file_in)
    
    if args.useDev:
        print "Using dev/test instance."

    csvfile = open(args.file_in,'r')
    fields = getFields(csvfile,args.file_in)
    
    requests, num_requests = fillFields(csvfile, fields, args.campaign, args.pwg, notCreate)

    if args.doModify:
        modifyRequests(requests, num_requests, args.doDryRun, args.useDev)
    elif args.cloneId != "":
        cloneRequests(requests, num_requests, args.doDryRun, args.useDev, args.cloneId)
    else:
        createRequests(requests, num_requests, args.doDryRun, args.useDev)
    
if __name__ == '__main__':
    main()
