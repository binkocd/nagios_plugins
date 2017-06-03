#!/usr/bin/python

import urllib2
import sys
import datetime
import dateutil.parser as dp
import xml.etree.ElementTree as et
import argparse


def check_solr_update(url, critical_threshold):
    root = et.parse(urllib2.urlopen(url)).getroot()
    update_time = root[1][12].text

    update_epoch = int(dp.parse(update_time).strftime('%s'))
    time_now = int(datetime.datetime.now().strftime("%s"))

    time_delta = time_now - update_epoch

    if time_delta < critical_threshold:
        print "Updates are Working OK"
        sys.exit(0)
    elif time_delta <= critical_threshold:
        print "Updates are older than %s." % critical_threshold
        sys.exit(1)
    elif time_delta > critical_threshold:
        print "UnifiedSearch has not updated in %s seconds" % time_delta
        sys.exit(2)


parser = argparse.ArgumentParser()
parser.add_argument("--action", type=str, choices='update')
parser.add_argument("--remote-server-url", "-u", dest="url", type=str, required=True,
                    help="URL that intended to be hit.")
parser.add_argument("--critical_threshold", "-c", dest="critical_threshold", type=int, required=True,
                    help="Critical threshold for service.")
parser.add_argument("--debug", action='store_true')

try:
    args = parser.parse_args()
except SystemExit:
    sys.exit(4)

if args.action == "update":
    check_solr_update(url=args.url, critical_threshold=args.critical_threshold)
else:
    print "Unknown: Check your args?"
    sys.exit(4)
