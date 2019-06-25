#!/usr/bin/python

import os
import time
import re
import sys
import socket


def usage():
	print('Usage:' + sys.argv[0])
	print('\t-h  help info')
	print('\t--help  help info')
	print('\t[IP] [port]  -- default is  127.0.0.1 5555')


def send_logs(file, sock, addr):
	lines = 0
	process_start = time.time()
	print("Start: {0}".format(process_start))

	with open(file, 'r') as f:
		while 1:
			line = f.readline()
			if line :
				#print(line)
				lines += 1
				logitem = line.split('CLIENT_LOG:')[1].strip()
				#print(logitem)
				ret = sock.sendto(logitem, addr)
			else:
				break;

	process_end = time.time()
	print("Finished, cost {0} seconds".format(process_end - process_start))

	return lines

ipaddr = '127.0.0.1'
port = 5555

# parse input params
argc = len(sys.argv)
print('argc:' + str(argc))
if argc == 2 :
	if sys.argv[1] == '-h' or sys.argv[1] == '--help' :
		usage()
		sys.exit()
	else :
		ipaddr = sys.argv[1]

elif argc >= 3 :
	ipaddr = sys.argv[1]
	port = sys.argv[2]
else :
	usage()
	sys.exit()

print('ipaddr: {0} port: {1}'.format(ipaddr,port))

# Get files to process
pwd = os.getcwd()
files = []
print("PWD: " + pwd)
print(os.listdir(pwd))
for f in os.listdir(pwd) :
	item = re.search(r"client.log-2019.*?", f)
	#print(item)
	if item != None :
		#print(item.group())
		#print(f)
		files.append(f)

print("This files will be processed: " + str(files))
time.sleep(1)

# create udp socket
server = (ipaddr, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# sent logs to server
for f in files:
	print("Now process: " + f)
	time.sleep(1)
	n = send_logs(f, sock, server)
	print("send {0} lines log from {1}".format(n, f))
