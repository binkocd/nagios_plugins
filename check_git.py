#!/usr/bin/python

import commands
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, choices=['list'])
   #Can I pass Database instead of full URL?
    parser.add_argument('--remote-server-url', '-u', dest='url', type=str, required=True,
                        help="URL that intended to be hit.")
    parser.add_argument('--critical_threshold', "-c", dest='critical_threshold', type=int, required=False,
                        help='Critical threshold for service.')
    parser.add_argument('--debug', action='store_true')

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(4)

    if args.action == 'update':
        check_git_function(url=args.url)
    else:
        print 'Unknown: Check your args?'
        sys.exit(4)


def check_git_function(url):
    git_check, output = commands.getstatusoutput("git ls-remote " + git_repo)

    try:
        if git_check == 0:
            print "OK - Stash Git Responding Normally."
            sys.exit(0)
        elif git_check != 0:
            print "CRITICAL - Stash Git Not Responding."
            sys.exit(2)
    except SystemExit:
        print "UNKNOWN - Check Not Responding Correctly."
        sys.exit(3)


if __name__ == "__main__":
    main()
