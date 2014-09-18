#!/usr/bin/env python
import sys
import os.path
import argparse

def getArguments():
    parser = argparse.ArgumentParser(description='Create McM requests.')

    parser.add_argument('file_in')
    parser.add_argument('-c', '--campaign', action='store', dest='campaign', metavar='name', required=True, help='Set member_of_campaign.')
    parser.add_argument('-p', '--pwg', action='store', dest='pwg', default='XXX', help='Set PWG. Defaults to %(default)s. Change default on this line to your PWG.')
    parser.add_argument('-d', action='store_true', dest='useDev', help='Use dev/test instance.')
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

def main():
    args = getArguments()
    checkPWG(args.pwg)
    checkFile(args.file_in)
    print args.useDev
    print args.campaign
    print args.pwg
    print args.file_in

if __name__ == '__main__':
    main()
