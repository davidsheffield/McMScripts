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


def interrogate():
    loop = True
    while loop:
        process = raw_input("Process: ")
        requester = raw_input("Requester name: ")
        email = raw_input("Requester email: ")
        tag = raw_input("Tag: ")
        events = raw_input ("Events: ")
        note = raw_input("Notes: ")
        spreadsheet = raw_input("Spreadsheet: ")
        campaign = raw_input("Campaign: ")

        yn = raw_input("Are these acceptable? [y/n] ")
        while True:
            if yn.lower() in ["y", "yes"]:
                loop = False
                break
            elif yn.lower() in ["n", "no"]:
                break
            else:
                yn = raw_input('Please enter "yes" or "no". ')

    return [process, requester, email, tag, events, note, spreadsheet, campaign]


def addRequestSet(answers):
    mcm = restful(dev=False)
    req_list = mcm.getA('requests', query='tags={0}&member_of_campaign={1}'.format(
            answers[3], answers[7]))
    multiplicity = len(req_list)
    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute('INSERT INTO RequestSets (Process, Tag, Events, Notes, Spreadsheet, RequestMultiplicity) VALUES ("{0}", "{1}", {2}, "{3}", "{4}", {5});'.format(
            answers[0], answers[3], answers[4], answers[5], answers[6], multiplicity))
    conn.commit()
    conn.close()

    print "Sucessfully added {0} {1} to RequestSets table.".\
        format(answers[0], answers[1])
    return

def main():
    answers = interrogate()
    addRequestSet(answers)

    return


if __name__ == '__main__':
    main()
