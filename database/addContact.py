#!/usr/bin/env python

################################
#
# addContact.py
#
#  Script to add new gen contact to database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import argparse

def getArguments():
    parser = argparse.ArgumentParser(description = 'Create, modify, and clone McM requests.')

    # Command line flags
    parser.add_argument('FirstName')
    parser.add_argument('LastName')
    parser.add_argument('Email')

    args_ = parser.parse_args()
    return args_

def addContact(first_name, last_name, email):
    conn = sqlite3.connect('EXO_MC_Requests.db')
    c = conn.cursor()
    c.execute('INSERT INTO Contacts VALUES(NULL, "{0}", "{1}", "{2}");'.\
                  format(first_name, last_name, email))
    conn.commit()
    conn.close()

    print "Sucessfully added {0} {1} ({2}) to Contacts table.".\
        format(first_name, last_name, email)

    return

def main():
    args = getArguments()
    addContact(args.FirstName, args.LastName, args.Email)
    return

if __name__ == '__main__':
    main()
