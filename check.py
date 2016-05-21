#!/usr/bin/python3

import os
import sys
import time
import argparse
import tempfile
import json

import single
import pool

def p2f(s):
	return float(s.strip('%')) / 100

def message(resource, data, warning, critical):
	percent = data["used"] / data["limit"]
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
	msg += "%s of \"%s\" already used. (%d / %d %s)" % (percent, resource, data["used"], data["limit"], data["unit"])
	return code, msg

def cache():
	return os.path.join(tempfile.gettempdir(), "tmobile-scripts")

def cache_read(username, path, timeout):
	if not os.path.isfile(path): return None
	if time.time() - os.path.getmtime(path) > timeout:
		os.remove(path)
		return None
	try:
		with open(path) as f:
			data = json.load(f)
		if username in data: return data[username]
	except:
		pass
	return None

def cache_write(username, path, resources):
	data = {}
	try:
		with open(path) as f:
			data = json.load(f)
	except:
		pass
	data.update({username: resources})
	with open(path, "w") as f:
		json.dump(data, f)

def check(username, password, account):
	if account == "pool": return pool.fetch(username, password)
	elif account == "personal":return single.fetch(username, password) 
	return None

parser = argparse.ArgumentParser(description="Check T-Mobile quota.")
parser.add_argument("-u", "--username", help="username to login", required=True)
parser.add_argument("-p", "--password", help="password to login", required=True)
parser.add_argument("-a", "--account", help="account type (e.g. personal, pool)", choices=["personal", "pool"], required=True)
parser.add_argument("--use-cache", help="activate cache mode", action="store_true")
parser.add_argument("--cache-file", help="cache file to user", default=cache())
parser.add_argument("--cache-timeout", help="cache timeout in seconds", type=int, default=60)
parser.add_argument("-v", "--verbose", help="activate verbose mode", action="store_true")
parser.add_argument("-r", "--resource", help="resource to check")
parser.add_argument("-w", "--warning", help="warning percentage", default="80%")
parser.add_argument("-c", "--critical", help="critical percentage", default="90%")

args = parser.parse_args()
cache_values = False

if args.use_cache:
	resources = cache_read(args.username, args.cache_file, args.cache_timeout)
	if resources: cache_values = True

if not cache_values:
	try:
		resources = check(args.username, args.password, args.account)
	except:
		print("UNKNOWN - malformed website or timeout")
		sys.exit(3)
	if args.use_cache:
		cache_write(args.username, args.cache_file, resources)

warning = p2f(args.warning)
critical = p2f(args.critical)
result = 0

if args.resource:
	if args.resource not in resources:
		print("UNKNOWN - resource not found")
		sys.exit(3)
	result, m = message(args.resource, resources[args.resource], warning, critical)
	print(m)
else:
	for resource in resources:
		c, m = message(resource, resources[resource], warning, critical)
		print(m)
		if c > result: result = c

sys.exit(result)

