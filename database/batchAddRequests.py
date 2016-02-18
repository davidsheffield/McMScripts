#!/usr/bin/env python

################################
#
# batchAddRequests.py
#
#  Script to add requests to database with a CSV file
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse
import sys
import csv
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import *
import time


def addRequestSet(answers, mcm):
    req_list = mcm.getA('requests', query='tags={0}&member_of_campaign=RunIISummer15GS'.format(
            answers[1]))
    multiplicity = len(req_list)
    events = 0
    for req in req_list:
        events += req['total_events']
    conn = sqlite3.connect('EXO_MC_Requests.db')
    c = conn.cursor()
    c.execute('INSERT INTO RequestSets (Process, Tag, Events, Notes, Spreadsheet, RequestMultiplicity) VALUES ("{0}", "{1}", {2}, "{3}", "{4}", {5});'.format(
            answers[0], answers[1], events, answers[6], answers[5], multiplicity))
    conn.commit()
    conn.close()

    print "Sucessfully added {0} {1} to RequestSets table.".\
        format(answers[0], answers[1])
    return

def main():
    csvfile = open('fill.csv', 'r')
    mcm = restful(dev=False)
    print "Adding:"
    for row in csv.reader(csvfile):
        if row[0].startswith("#"):
            continue
        print row[0]
        addRequestSet(row, mcm)
        time.sleep(1)

    return


if __name__ == '__main__':
    main()
