#!/usr/bin/python

import sys
import argparse
import pool

def p2f(s):
	return float(s.strip('%')) / 100

def message(resource, warning, critical):
	percent = resource[1] / resource[2]
	code = None
	msg = None
	if percent < warning:
		code = 0
		msg = "OK - "
	elif percent < critical:
		code = 1
		msg = "WARNING - "
	else:
		code = 2
		msg = "ERROR - "
	percent = "{0:.0f}%".format(percent * 100)
	msg += "%s of \"%s\" already used. (%d / %d %s)" % (percent, resource[0], resource[1], resource[2], resource[3])
	return code, msg

parser = argparse.ArgumentParser(description="Check T-Mobile pool quota.")
parser.add_argument("-u", "--username", required=True, help="username")
parser.add_argument("-p", "--password", required=True, help="password")
parser.add_argument("-w", "--warning", required=True, help="warning percentage")
parser.add_argument("-c", "--critical", required=True, help="critical percentage")

args = parser.parse_args()

try:
	resources = pool.fetch(args.username, args.password)
except:
	print("UNKNOWN - malformed website or timeout")
	sys.exit(3)

warning = p2f(args.warning)
critical = p2f(args.critical)
result = 0

for resource in resources:
	c, m = message(resource, warning, critical)
	print(m)
	if c > result: result = c

sys.exit(result)

