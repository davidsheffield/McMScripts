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


def interrogate():
    loop = True
    while loop:
        process = raw_input("Process: ")
        #requester = raw_input("Requester name: ")
        #email = raw_input("Requester email: ")
        tag = raw_input("Tag: ")
        events = raw_input ("Events: ")
        note = raw_input("Notes: ")

        yn = raw_input("Are these acceptable? [y/n] ")
        while True:
            if yn.lower() in ["y", "yes"]:
                loop = False
                break
            elif yn.lower() in ["n", "no"]:
                break
            else:
                yn = raw_input('Please enter "yes" or "no". ')

    return [process, tag, events, note]


def addRequestSet(answers):
    conn = sqlite3.connect('EXO_MC_Requests.db')
    c = conn.cursor()
    c.execute('INSERT INTO RequestSets VALUES(NULL, "{0}", NULL, NULL, "{1}", "{2}", "{3}", 0, 0, 0, 0, 0, 0, 0);'.\
                  format(answers[0], answers[1], answers[2], answers[3]))
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
