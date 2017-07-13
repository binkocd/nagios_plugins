#!/usr/bin/python

import subprocess
import sys
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, choices=['list'])
    parser.add_argument('--remote-git-url', '-r', dest='url', type=str, required=True,
                        help="URL that intended to be hit.")
    parser.add_argument('--critical_threshold', "-c", dest='critical_threshold', type=int, required=False,
                        help='Critical threshold for service in minutes.')
    parser.add_argument('--username', '-u', dest='username', type=str, required=True,
                        help='Username for git repo.')
    parser.add_argument('--password', '-p', dest='password', type=str, required=True,
                        help='Password for specified username.')
    parser.add_argument('--debug', action='store_true')

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(4)

    if args.action == 'list':
        check_git_list(url=args.url, username=args.username, password=args.password)
    else:
        print 'Unknown: Check your args?'
        sys.exit(4)


def check_git_list(url, username, password):

    cmd = subprocess.Popen( 'git ls-remote -h https://' + username + ':' + password + '@' + url, shell=True, stdout=subprocess.PIPE )

    for line in cmd.stdout:
        if "master" in line:
            print 'OK: Git is responding normally. | GIT_UP=1'
            sys.exit(0)
        elif "correct access" in line:
            print 'WARN: Might be a permissions issue. | GIT_UP=0.5'
            sys.exit(1)
        elif "Fatal" in line:
            print 'CRIT: Git has not responded in over 5 minutes. | GIT_UP=0'
            sys.exit(2)


if __name__ == "__main__":
    main()
