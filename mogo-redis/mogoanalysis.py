#!/usr/bin/env python3

import sys
import datetime
import time
import pprint
from pymongo import MongoClient

def usage():
	print('Usage:')
	print(sys.argv[0], '<collection> [item]')

coll_name  = 'access_points'
item_name = 'hardware_type'

# parse input params
argc = len(sys.argv)
if argc < 2 :
	usage()
#	sys.exit()
elif argc == 2 :
	coll_name = sys.argv[1]
elif argc >= 3 :
	coll_name = sys.argv[1]
	item_name = sys.argv[2]

print('collection', coll_name, 'item:', item_name)


mogoclient = MongoClient('172.16.20.80', 27017)
db = mogoclient['status']
collection = db[coll_name]


# get distinct items from mogodb
start = time.time()
items = collection.distinct(item_name)
end = time.time()

pprint.pprint(items)

print('Match items: ', len(items), 'in %f seconds'%(end-start))


# get the count of each item
pipeline = [
	{"$group": {"_id": '$' + item_name, "count": { "$sum":1}}},
	{"$sort": {"count": -1, "_id":1}}
]

stts = collection.aggregate(pipeline)

pprint.pprint(list(stts))

