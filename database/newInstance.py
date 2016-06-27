#!/usr/bin/env python

################################
#
# newInstance.py
#
#  Script to add new instance of set of requests to database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse
import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
sys.path.append('../')
import mcmscripts_config


# def AddRequester(name_, email_):
#     conn = sqlite3.connect(mcmscripts_config.database_location)
#     c = conn.cursor()
#     c.execute('INSERT INTO Requesters (Name, Email) VALUES ("{0}", "{1}");'.format(
#             name_, email_))
#     requester_id = c.lastrowid
#     conn.commit()
#     conn.close()

#     print "Added new requester: {0} ({1})".format(name_, email_)

#     return requester_id


# def GetRequester(name_, email_):
#     conn = sqlite3.connect(mcmscripts_config.database_location)
#     c = conn.cursor()
#     c.execute("""SELECT RequesterID, Name, Email FROM Requesters
# WHERE Name = "{0}" OR Email = "{1}";""".format(name_, email_))
#     out = c.fetchall()
#     conn.close()
#     requester_id = 0
#     if len(out) == 0:
#         requester_id = AddRequester(name_, email_)
#     elif len(out) == 1:
#         requester_id = out[0][0]
#     else:
#         print "Found more than one requester. Choose the ID to use. 0 creates new requester."
#         for row in out:
#             print "{0} {1} {2}".format(row[0], row[1], row[2])
#         requester_id = raw_input("User ID: ")
#         if requester_id == 0:
#             requester_id = AddRequester(name_, email_)
#     return requester_id


# def AddRequestSet(answers_, requester_id_):
#     conn = sqlite3.connect(mcmscripts_config.database_location)
#     c = conn.cursor()
#     c.execute("""INSERT INTO RequestSets (Process, Tag, Events,
# RequestMultiplicity, Notes, Spreadsheet, Ticket) VALUES ("{0}", "{1}", {2}, {3},
# "{4}", "{5}", "{6}");""".format(answers_[0], answers_[3], answers_[4], answers_[5],
#                                 answers_[6], answers_[7], answers_[8]))
#     set_id = c.lastrowid
#     c.execute("""INSERT INTO Instances (SetID, CampaignChainID, ContactID,
# RequesterID, PriorityBlock) VALUES ({0}, {1}, {2}, {3}, {4});""".format(
#             set_id, answers_[10], answers_[11], requester_id_, 3))
#     instance_id = c.lastrowid
#     c.execute("""SELECT Campaigns.CampaignID FROM CampaignChains
# INNER JOIN CampaignChain_Campaign USING(CampaignChainID)
# INNER JOIN Campaigns USING(CampaignID) WHERE CampaignChainID = {0};""".format(answers_[10]))
#     out = c.fetchall()
#     for campaign in out:
#         c.execute("""INSERT INTO Requests (CampaignID, New, Validating,
# Validated, Defined, Approved, Submitted) VALUES ({0}, 0, 0, 0, 0, 0, 0);""".format(campaign[0]))
#         requests_id = c.lastrowid
#         c.execute("""INSERT INTO Instance_Requests (InstanceID, RequestsID)
# VALUES ({0}, {1});""".format(instance_id, requests_id))
#     conn.commit()
#     conn.close()

#     print "Sucessfully added {0} {1} to RequestSets table.".\
#         format(answers_[0], answers_[1])
#     return


def main():
    loop = True
    while loop:
        tag = raw_input("Tag: ")
        conn = sqlite3.connect(mcmscripts_config.database_location)
        c = conn.cursor()
        c.execute("""SELECT SetID, Process, Events, RequestMultiplicity, Notes,
Spreadsheet, Ticket, ContactID, DisplayName, RequesterID, Requesters.Name,
PriorityBlock, CampaignChains.Name, SuperCampaigns.Name, InstanceID, CampaignChainID
FROM RequestSets INNER JOIN Instances USING(SetID) INNER JOIN CampaignChains
USING(CampaignChainID) INNER JOIN SuperCampaigns USING(SuperCampaignID)
INNER JOIN Contacts USING(ContactID) INNER JOIN Requesters USING(RequesterID)
WHERE Tag = "{0}";""".format(
                tag))
        out = c.fetchall()
        instance_list = [row[14] for row in out]
        print instance_list
        print "Process: {0}".format(out[0][1])
        print "Events: {0}".format(out[0][2])
        print "Request Multiplicity: {0}".format(out[0][3])
        if out[0][4] != "":
            print "Notes: {0}".format(out[0][4])
        print "Spreadsheet: {0}".format(out[0][5])
        print "Ticket: {0}".format(out[0][6])
        for i, row in enumerate(out):
            print "{0} ----------".format(i) #row[14])
            print "Contact: {1}".format(row[7], row[8])
            print "Requester: {1}".format(row[9], row[10])
            print "Block: ".format(row[11])
            print "SuperCampaign: {0}".format(row[13])
            print "Chain: {0}".format(row[12])
        print "------------"
        conn.close()

        print ""
        row_num = int(raw_input("Instance to copy: "))
        chainID = int(raw_input("Chain ID (7,11 GS / 9,13 wmLHE / 10,14 pLHE): "))

        yn = raw_input("Are these acceptable? [y/n] ")
        while True:
            if yn.lower() in ["y", "yes"]:
                loop = False
                break
            elif yn.lower() in ["n", "no"]:
                break
            else:
                yn = raw_input('Please enter "yes" or "no". ')

    print "\n===========\n"

    SetID = out[row_num][0]
    ContactID = out[row_num][7]
    RequesterID = out[row_num][9]
    PriorityBlock = out[row_num][11]
    old_InstanceID = out[row_num][14]

    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute("""INSERT INTO Instances (SetID, CampaignChainID, ContactID,
RequesterID, PriorityBlock) VALUES ({0}, {1}, {2}, {3}, {4});""".format(
            SetID, chainID, ContactID, RequesterID, PriorityBlock))
    new_InstanceID = c.lastrowid
    print "Added new instance"

    c.execute("""SELECT CampaignID FROM CampaignChain_Campaign
WHERE CampaignChainID = {0};""".format(chainID))
    out = c.fetchall()
    for row in out:
        c.execute("""SELECT CampaignID, RequestsID FROM Requests
INNER JOIN Instance_Requests USING(RequestsID) WHERE InstanceID = {0}
AND CampaignID = {1};""".format(old_InstanceID, row[0]))
        out_requests = c.fetchall()
        if (len(out_requests) > 0):
            c.execute("""INSERT INTO Instance_Requests (InstanceID, RequestsID)
VALUES ({0}, {1});""".format(new_InstanceID, out_requests[0][1]))
            print "Added existing request to instance"
        else:
            c.execute("""INSERT INTO Requests (CampaignID, New, Validating,
Validated, Defined, Approved, Submitted) VALUES ({0}, 0, 0, 0, 0, 0, 0);""".format(
                    row[0]))
            new_RequestsID = c.lastrowid
            c.execute("""INSERT INTO Instance_Requests (InstanceID, RequestsID)
VALUES ({0}, {1});""".format(new_InstanceID, new_RequestsID))
            print "Added new request to instance"

    conn.commit()
    conn.close()

    return


if __name__ == '__main__':
    main()
