#!/usr/bin/env python

################################
#
# newInstance.py
#
#  Script to add new instance of requests to database
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
        tag = raw_input("Tag: ")
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

        yn = raw_input("Are these acceptable? [y/n] ")
        while True:
            if yn.lower() in ["y", "yes"]:
                loop = False
                break
            elif yn.lower() in ["n", "no"]:
                break
            else:
                yn = raw_input('Please enter "yes" or "no". ')

    return [tag, campaign_chain]


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


def AddRequestSet(answers_):
    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute("""SELECT Instances.SetID, Instances.ContactID,
Instances.RequesterID, Instances.PriorityBlock FROM Instances
INNER JOIN RequestSets USING(SetID) WHERE Tag = "{0}";""".format(answers_[0]))
    out = c.fetchall()
    c.execute("""INSERT INTO Instances (SetID, CampaignChainID, ContactID,
RequesterID, PriorityBlock) VALUES ({0}, {1}, {2}, {3}, {4});""".format(
            out[0][0], answers_[1], out[0][1], out[0][2], out[0][3]))
    instance_id = c.lastrowid
    c.execute("""SELECT Campaigns.CampaignID FROM CampaignChains
INNER JOIN CampaignChain_Campaign USING(CampaignChainID)
INNER JOIN Campaigns USING(CampaignID) WHERE CampaignChainID = {0};""".format(answers_[1]))
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
    AddRequestSet(answers)

    return


if __name__ == '__main__':
    main()
