#!/usr/bin/python

import commands
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description='Check Git Functionality on a remote server.')
    parser.add_argument("--git-repository", "-r", dest="git_repo", type=str, required=True, help="Name of Git Repository")
    parser.add_argument("--debug", action='store_true')
    args = parser.parse_args()


def check_git_function(*args):
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
