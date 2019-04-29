#!/usr/bin/env python3

import sys
import datetime
import time
import pprint
from pymongo import MongoClient
import redis

def usage():
	print('Usage:')
	print(sys.argv[0], '<pe> <inc rate %> <bond rate %>')


pe = 0
inc_rate = 0
bond_rate = 0
stock_yield = 0 # 1 + (1 + 1/pe) + 1
bond_yield = 0  # SUM of (1 + bond_rate)^n

# parse input params
argc = len(sys.argv)
if argc < 4 :
	usage()
	sys.exit()
elif argc >= 4 :
	pe = float(sys.argv[1])
	inc_rate = float(sys.argv[2])/100
	bond_rate = float(sys.argv[3])/100


print('PE:', pe, 'Increase rate:', inc_rate, 'Bond rate:', bond_rate)
print('--------------------------------------------------------------------------')
print('Turn |   PE   | Bond PE|       E|    Bond E|')

runtime = 0
earn = 1
while True:
	cal_pe = pe/((1+inc_rate)**runtime)
	earn += 1/cal_pe
	print('%4d | %3.3f | %3.3f | %03.3f | %3.3f |' % (runtime, cal_pe, 1/bond_rate,
         (earn-1)*100, bond_rate*(runtime+1)*100))

	runtime += 1

	if runtime > 10 :
		break



