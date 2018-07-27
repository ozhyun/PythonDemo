#!/usr/bin/env python3

import sys
import datetime
import time
import pprint
from pymongo import MongoClient
import redis

def usage():
	print('Usage:')
	print(sys.argv[0], '<Admin ID> [VSLAN ID] [Interval]')

STDBHOST = '172.16.20.80'
NCHOST = '172.16.20.50'

admin_id = 0
vslan_id = 0
interval = 120 # seconds

# parse input params
argc = len(sys.argv)
if argc < 2 :
	usage()
	sys.exit()
elif argc == 2 :
	admin_id = int(sys.argv[1])
elif argc == 3 :
	admin_id = int(sys.argv[1])
	vslan_id = int(sys.argv[2])
elif argc >= 4 :
	admin_id = int(sys.argv[1])
	vslan_id = int(sys.argv[2])
	interval = int(sys.argv[3])

print('Admin ID:', admin_id, 'VSLAN ID:', vslan_id, 'Interval:', interval, 'Seconds')
print('STDB:', STDBHOST, 'NC:', NCHOST)

# attributes
cond = {'admin_id': admin_id}
if vslan_id > 0 :
	cond['vslan_id'] = vslan_id

print('Condition:', cond)

# init mogodb connection
mogoclient = MongoClient(STDBHOST, 27017)
db = mogoclient['status']
collection = db['clients']

# init redis connection
pool = redis.ConnectionPool(host=NCHOST, port=6379, db=0)
nc = redis.Redis(connection_pool=pool)

runtime = 1
while True:
	print('==[%d] times to force offline stas with %s'%(runtime, cond))

	# get clients' mac addresses from mogodb
	start = time.time()
	clients = collection.find(cond)
	end = time.time()
	print('Match items: ', clients.count(), 'in %f seconds'%(end-start))


	# extract clients' mac addresses
	macs = []
	start = time.time()
	for i in clients:
		macs.append(i['mac'])
		#pprint.pprint(i)
		#print()
	end = time.time()
	print('const', end-start, "seconds to extract clients' mac addresses")
	print(macs)


	#send notify to redis
	start = time.time()
	for mac in macs:
		nc.publish('commands', '%d|31000|4|%s'%(admin_id, mac))

	stop = time.time()
	print('Send', len(macs), 'commands cost time:', stop-start)

	# sleep the interval
	print('Sleep %d seconds' % (interval))
	time.sleep(interval)

	runtime += 1

