#!/usr/bin/env python

################################
#
# check.py
#
#  Script to check status of requests and save in database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import time
sys.path.append('../')
import mcmscripts_config


def getArguments():
    parser = argparse.ArgumentParser(
        description='Check status of requests in McM and save in database.')

    # Command line flags
    parser.add_argument('--check', action='store', dest='check',
                        help='Type of check to perform. 0 Check all sets, 1 Check sets that are not finished, 2 Check requests being validated.')
    parser.add_argument('-t', '--tag', action='store', dest='tag',
                        help='Check status of requests based on tag.')

    args_ = parser.parse_args()
    return args_


def getRequestSets():
    mcm = restful(dev=False)

    wmLHE_campaign  = "RunIIWinter15wmLHE"
    pLHE_campaign   = "RunIIWinter15pLHE"
    GS_campaign     = "RunIISummer15GS"
    DR_campaign     = "RunIIFall15DR76"
    Mini_campaign   = "RunIIFall15MiniAODv1"
    Miniv2_campaign = "RunIIFall15MiniAODv2"
    status_name = [["LHE_New", "LHE_Validating", "LHE_Validated", "LHE_Defined",
                    "LHE_Approved", "LHE_Submitted", "LHE_Done"],
                   ["GS_New", "GS_Validating", "GS_Validated", "GS_Defined",
                    "GS_Approved", "GS_Submitted", "GS_Done"],
                   ["DR_New", "DR_Validating", "DR_Validated", "DR_Defined",
                    "DR_Approved", "DR_Submitted", "DR_Done"],
                   ["MiniAOD_New", "MiniAOD_Validating", "MiniAOD_Validated",
                    "MiniAOD_Defined", "MiniAOD_Approved", "MiniAOD_Submitted",
                    "MiniAOD_Done"],
                   ["MiniAODv2_New", "MiniAODv2_Validating",
                    "MiniAODv2_Validated", "MiniAODv2_Defined",
                    "MiniAODv2_Approved", "MiniAODv2_Submitted",
                    "MiniAODv2_Done"]]

    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute('SELECT SetID, Tag FROM RequestSets WHERE RequestMultiplicity != MiniAODv2_Done')
    out = c.fetchall()

    print "Checking:"
    for request in out:
        print request[1]

        campaigns = [wmLHE_campaign, GS_campaign, DR_campaign, Mini_campaign, Miniv2_campaign]
        req_list = mcm.getA('requests', query='tags={0}'.format(
                request[1]))
        statuses = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        for req in req_list:
            for i in range(len(campaigns)):
                if req['member_of_campaign'] == campaigns[i]:
                    if req['approval'] == "none" and req['status'] == "new":
                        statuses[i][0] += 1
                    elif req['approval'] == "validation" and req['status'] == "new":
                        statuses[i][1] += 1
                    elif req['approval'] == "validation" and req['status'] == "validation":
                        statuses[i][2] += 1
                    elif req['approval'] == "define" and req['status'] == "defined":
                        statuses[i][3] += 1
                    elif req['approval'] == "approve" and req['status'] == "approved":
                        statuses[i][4] += 1
                    elif req['approval'] == "submit" and req['status'] == "submitted":
                        statuses[i][5] += 1
                    elif req['approval'] == "submit" and req['status'] == "done":
                        statuses[i][6] += 1
        #print statuses
        #print request[0]
        for i in range(len(statuses)):
            for j in range(len(statuses[0])):
                c.execute('UPDATE RequestSets SET {0} = {1} WHERE SetID = {2}'.format(
                        status_name[i][j], statuses[i][j], request[0]))
        time.sleep(1)
    conn.commit()
    conn.close()

    return


def checkRequests():
    mcm = restful(dev=False)

    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute("""SELECT DISTINCT Tag, RequestMultiplicity, Done, Campaigns.Name,
RequestsID FROM Requests INNER JOIN Campaigns USING(CampaignID)
INNER JOIN Instance_Requests USING(RequestsID) INNER JOIN Instances
USING(InstanceID) INNER JOIN RequestSets USING(SetID);""")
    out = c.fetchall()

    status_names = ["New", "Validating", "Validated", "Defined", "Approved",
                    "Submitted", "Done"]

    for row in out:
        if row[1] == row[2]:
            continue
        print "{0} {1}".format(row[0], row[3])
        req_list = mcm.getA('requests',
                            query='tags={0}&member_of_campaign={1}'.format(
                            row[0], row[3]))
        time.sleep(1)
        statuses = [0, 0, 0, 0, 0, 0, 0]
        for req in req_list:
            if req['approval'] == "none" and req['status'] == "new":
                statuses[0] += 1
            elif req['approval'] == "validation" and req['status'] == "new":
                statuses[1] += 1
            elif req['approval'] == "validation" and req['status'] == "validation":
                statuses[2] += 1
            elif req['approval'] == "define" and req['status'] == "defined":
                statuses[3] += 1
            elif req['approval'] == "approve" and req['status'] == "approved":
                statuses[4] += 1
            elif req['approval'] == "submit" and req['status'] == "submitted":
                statuses[5] += 1
            elif req['approval'] == "submit" and req['status'] == "done":
                statuses[6] += 1

        for i, status_name in enumerate(status_names):
            c.execute("""UPDATE Requests SET {0} = {1} WHERE RequestsID = {2}""".format(
                    status_name, statuses[i], row[4]))

    c.execute("""\
UPDATE Settings
SET Value = "{0}"
WHERE SettingID = 1;""".format(time.asctime()))

    conn.commit()
    conn.close()

    return


def main():
    args = getArguments() # Setup flags and get arguments
    #getRequestSets()
    checkRequests()

    return


if __name__ == '__main__':
    main()
