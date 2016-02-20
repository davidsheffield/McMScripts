#!/usr/bin/env python

################################
#
# addContact.py
#
#  Script to add contact to database
#
#  author: David G. Sheffield (Rutgers)
#
################################

import sqlite3
import sys
sys.path.append('../')
import mcmscripts_config


def interrogate():
    loop = True
    while loop:
        name = raw_input("Name: ")
        email = raw_input("email: ")
        display_name = raw_input("Display name: ")
        user_name = raw_input("Username: ")

        yn = raw_input("Are these acceptable? [y/n] ")
        while True:
            if yn.lower() in ["y", "yes"]:
                loop = False
                break
            elif yn.lower() in ["n", "no"]:
                break
            else:
                yn = raw_input('Please enter "yes" or "no". ')

    return [name, email, display_name, user_name]


def addContact(answers):
    conn = sqlite3.connect(mcmscripts_config.database_location)
    c = conn.cursor()
    c.execute('INSERT INTO Contacts VALUES (Null, "{0}", "{1}", "{2}", "{3}");'.format(
            answers[0], answers[1], answers[2], answers[3]))
    conn.commit()
    conn.close()

    print "Sucessfully added {0} to Contacts table.".format(answers[0])
    return


def main():
    answers = interrogate()
    addContact(answers)

    return


if __name__ == '__main__':
    main()
