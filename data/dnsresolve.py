#!/usr/bin/python
# coding=utf-8

import socket
import time
import sys
import os
import signal

def usage():
	print('Usage:' + sys.argv[0])
	print('\t-h  help info')
	print('\t--help  help info')
	print('\t<domain>  [interval]  -- domain name & interval in seconds, default 60s')



def dns_resolve(dn):
	#print('Input: ' + dn)
	ipaddrs = set()

	try:
		addr = socket.getaddrinfo(dn, None)
		#print(addr)
	except socket.error, e:
		print(e)
		return None

	#print("There's {0} items".format(len(addr)))
	for i in addr:
		#print(i)
		ipaddrs.add(i[4][0])

	#print(ipaddrs)
	return (dn, ipaddrs)



def sig_handler(signum, frame):
	global total_times
	global fail_times

	print('Catch kill signal, exit now:\n')
	now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	print('{0}   Total {1:-8}  Failed {2:-8}'.format(now, total_times, fail_times))
	sys.exit()



def main():
	global domain
	global interval

	# parse input params
	argc = len(sys.argv)
	#print('argc:' + str(argc))
	if argc == 2 :
		if sys.argv[1] == '-h' or sys.argv[1] == '--help' :
			usage()
			sys.exit()
		else :
			domain = sys.argv[1]
	elif argc == 3:
		domain = sys.argv[1]
		interval = int(sys.argv[2])
	else :
		usage()
		sys.exit()

	signal.signal(signal.SIGINT, sig_handler)

	print('Domain: {0}         Interval: {1}\n'.format(domain, interval))

	now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
	print(now + '   Start')

	global total_times
	global fail_times

	while True:
		now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
		total_times = total_times + 1
		ips = dns_resolve(domain)
		if ips == None:
			fail_times = fail_times + 1
			print("{0} F {1:8}".format(now, fail_times))
		'''else :
			print(ips[0])
			for i in ips[1]:
				print('\t' + i)
		'''

		if total_times > 0 and total_times % 20 == 0:
			print('{0}   Total {1:-8}  Failed {2:-8}'.format(now, total_times, fail_times))

		time.sleep(interval)


# globals
domain = ''
interval=60
fail_times = 0
total_times = 0

# main
if __name__ == '__main__':
	main()

