#!/usr/bin/env python
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

def main():
    args = getArguments()
    print args.useDev
    print args.campaign
    print args.pwg
    print args.file_in

if __name__ == '__main__':
    main()
