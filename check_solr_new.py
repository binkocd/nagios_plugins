#!/usr/bin/python

import json
import urllib2
import sys
import datetime
import xml.etree.ElementTree as et
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, choices=['update','query'])
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
        check_solr_update(url=args.url, critical_threshold=args.critical_threshold)
    elif args.action == 'query':
        solr_query_rate(url=args.url)
    else:
        print 'Unknown: Check your args?    '
        sys.exit(4)


def check_solr_update(url, critical_threshold):
    root = et.parse(urllib2.urlopen(url)).getroot()
    update_time = root[1][12].text

    update_in_epoch = int((datetime.datetime.strptime(update_time, "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.datetime(1970, 1, 1)).total_seconds())
    time_now = int(datetime.datetime.now().strftime('%s'))

    time_delta = time_now - update_in_epoch

    if time_delta < critical_threshold:
        print 'OK: Updates are Working. | DELTA_TIME = %s' % time_delta
        sys.exit(0)
    elif time_delta <= critical_threshold:
        print 'WARN: Updates are older than %s. | DELTA_TIME = %s' % (critical_threshold, time_delta)
        sys.exit(1)
    elif time_delta > critical_threshold:
        print 'CRIT: Database has not updated in %s seconds. | DELTA_TIME = %s' % (time_delta, time_delta)
        sys.exit(2)


def solr_query_rate(url):
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
        jsonResp = response.read()
        stats = json.loads(jsonResp)["solr-mbeans"][3]["/select"]["stats"]
    except Exception as e:
        print "WARNING: Failed to retrieve stats from SOLR server"
        sys.exit(1)


    for key,val in sorted(stats.items()):
        print "%s: %.3f" % (key, val)

    sys.stdout.write('| ')
    for key in ['avgRequestsPerSecond', 'avgTimePerRequest','75thPcRequestTime','95thPcRequestTime', '99thPcRequestTime']:
        sys.stdout.write('%s=%.3f ' % (key, stats[key]))
    sys.exit(0)


if __name__ == "__main__":
    main()
