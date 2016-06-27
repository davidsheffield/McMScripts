#!/usr/bin/env python

################################
#
# addRequests.py
#
#  Script to add requests to database
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


def Interrogate():
    loop = True
    while loop:
        process = raw_input("Process: ")
        requester = raw_input("Requester name: ")
        email = raw_input("Requester email: ")
        tag = raw_input("Tag: ")
        events = raw_input ("Events: ")
        multiplicity = raw_input ("Number of requests: ")
        note = raw_input("Notes: ")
        spreadsheet = raw_input("Spreadsheet: ")
        ticket = raw_input("Ticket: ")
        conn = sqlite3.connect(mcmscripts_config.database_location)
        c = conn.cursor()
        c.execute("""SELECT SuperCampaignID, Name FROM SuperCampaigns
WHERE Active > 0;""")
        out = c.fetchall()
        for row in out:
            print "{0} {1}".format(row[0], row[1])
        super_campaign = raw_input("SuperCampaign: ")
        c.execute("""SELECT CampaignChainID, Name FROM CampaignChains
WHERE SuperCampaignID = {0};""".format(super_campaign))
        out = c.fetchall()
        for row in out:
            print "{0} {1}".format(row[0], row[1])
        campaign_chain = raw_input("Chain: ")
        conn.close()
        contact_id = raw_input("Contact: ")

        yn = raw_input("Are these acceptable? [y/n] ")
        while True:
            if yn.lower() in ["y", "yes"]:
                loop = False
                break
            elif yn.lower() in ["n", "no"]:
                break
            else:
                yn = raw_input('Please enter "yes" or "no". ')

    return [process, requester, email, tag, events, multiplicity, note,
            spreadsheet, ticket, super_campaign, campaign_chain, contact_id]


def AddRequester(name_, email_):
    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute('INSERT INTO Requesters (Name, Email) VALUES ("{0}", "{1}");'.format(
            name_, email_))
    requester_id = c.lastrowid
    conn.commit()
    conn.close()

    print "Added new requester: {0} ({1})".format(name_, email_)

    return requester_id


def GetRequester(name_, email_):
    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute("""SELECT RequesterID, Name, Email FROM Requesters
WHERE Name = "{0}" OR Email = "{1}";""".format(name_, email_))
    out = c.fetchall()
    conn.close()
    requester_id = 0
    if len(out) == 0:
        requester_id = AddRequester(name_, email_)
    elif len(out) == 1:
        requester_id = out[0][0]
    else:
        print "Found more than one requester. Choose the ID to use. 0 creates new requester."
        for row in out:
            print "{0} {1} {2}".format(row[0], row[1], row[2])
        requester_id = raw_input("User ID: ")
        if requester_id == 0:
            requester_id = AddRequester(name_, email_)
    return requester_id


def AddRequestSet(answers_, requester_id_):
    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute("""INSERT INTO RequestSets (Process, Tag, Events,
RequestMultiplicity, Notes, Spreadsheet, Ticket) VALUES ("{0}", "{1}", {2}, {3},
"{4}", "{5}", "{6}");""".format(answers_[0], answers_[3], answers_[4], answers_[5],
                                answers_[6], answers_[7], answers_[8]))
    set_id = c.lastrowid
    c.execute("""INSERT INTO Instances (SetID, CampaignChainID, ContactID,
RequesterID, PriorityBlock) VALUES ({0}, {1}, {2}, {3}, {4});""".format(
            set_id, answers_[10], answers_[11], requester_id_, 3))
    instance_id = c.lastrowid
    c.execute("""SELECT Campaigns.CampaignID FROM CampaignChains
INNER JOIN CampaignChain_Campaign USING(CampaignChainID)
INNER JOIN Campaigns USING(CampaignID) WHERE CampaignChainID = {0};""".format(answers_[10]))
    out = c.fetchall()
    for campaign in out:
        c.execute("""INSERT INTO Requests (CampaignID, New, Validating,
Validated, Defined, Approved, Submitted) VALUES ({0}, 0, 0, 0, 0, 0, 0);""".format(campaign[0]))
        requests_id = c.lastrowid
        c.execute("""INSERT INTO Instance_Requests (InstanceID, RequestsID)
VALUES ({0}, {1});""".format(instance_id, requests_id))
    conn.commit()
    conn.close()

    print "Sucessfully added {0} {1} to RequestSets table.".\
        format(answers_[0], answers_[1])
    return


def main():
    answers = Interrogate()
    requester_id = GetRequester(answers[1], answers[2])
    AddRequestSet(answers, requester_id)

    return


if __name__ == '__main__':
    main()
