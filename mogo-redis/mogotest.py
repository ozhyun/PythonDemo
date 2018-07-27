#!/usr/bin/env python3

import sys
import datetime
import time
import pprint
from pymongo import MongoClient

def usage():
	print('Usage:')
	print(sys.argv[0], '<Admin ID> [VSLAN ID] [Interval]')

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

# attributes
cond = {'admin_id': admin_id}
if vslan_id > 0 :
	cond['vslan_id'] = vslan_id

print('Condition:', cond)

# get clients' mac addresses from mogodb
mogoclient = MongoClient('172.16.20.80', 27017)
db = mogoclient['status']
collection = db['clients']

start = time.time()
clients = collection.find(cond)
end = time.time()

print('Match items: ', clients.count(), 'in %f seconds'%(end-start))

#time.sleep(2)

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
