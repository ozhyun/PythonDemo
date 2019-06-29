#!/usr/bin/python

import sys
import time
import os
import re

class ClientEvent:
	"""Event"""

	def __init__(self):
		self.timestamp = ''
		self.action = ''
		self.action_result = ''
		self.ssid = ''
		self.ap = ''
		self.vsm = ''
		self.download = 0
		self.upload = 0

	def __str__(self):
		return '{0:22}{1:22}{2:26}{3:34}{4:20}{5:20}{6:10}{7:10}'.format(self.timestamp, 
								self.action, 
								self.action_result,
								self.ssid, self.ap, self.vsm,
								self.upload, self.download)


class Client:
    """client """

    def __init__(self):
        self.events = []
        self.upload = 0
        self.download = 0

    def __str__(self):
        return '{0:20}{1:22}{2:22}{3:22}{4:22}{5:18}{6:18}'.format(self.mac,
                                                       self.online_time, 
                                                       self.login_time, 
                                                       self.logoff_time, 
                                                       self.offline_time,
                                                       self.upload,
                                                       self.download)

    def showevents(self):
        for l in self.events:
            print(l)


def list_all_clients(file):

    clients = dict()

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

                item = re.search(r"\"(.*?)\"", logitem)
                #print(item.group())

                items = re.findall(r"\"(.*?)\"", logitem)
                #print("L"+str(lines)+": ", items)
           
                client_mac = items[3]
                if client_mac in clients:
                    c = clients[client_mac]
                else:
                    c = Client()
                    c.login_time = '-'
                    c.mac = client_mac
                    c.online_time ='-' 
                    c.login_time = '-'
                    c.logoff_time = '-'
                    c.offline_time = '-'
                    clients[c.mac] = c
            
                # append event
                event = ClientEvent()
                event.timestamp = items[0]
                event.action = items[17]
                event.action_result = items[18]
                event.ap = items[4]
                event.ssid = items[5]
                event.vsm = items[7]
                event.upload = int(items[16])/1024
                event.download = int(items[13])/1024
                c.events.append(event)

                if items[17] == 'client_add':
                    c.online_time = items[0]
                elif items[17] == 'client_state_switch' and items[18] == 'client_state_common2white':
                    c.login_time = items[0]
                elif items[17] == 'client_del':
                    c.offline_time = items[0]
                    c.upload = int(items[16])/1024
                    c.download = int(items[13])/1024
                elif items[17] == 'client_update':
                    c.upload = int(items[16])/1024
                    c.download = int(items[13])/1024

                #print("MAC      Online              Login         Logoff                 Offline")
                #print("-------------------------------------------------------------------------------")
                #print(c)
            else:
                break

    process_end = time.time()
    print("Finished, cost {0} seconds".format(process_end - process_start))

    return clients


def usage():
	print('Usage:' + sys.argv[0])
	print('\t-h  help info')
	print('\t--help  help info')
	print('\t[MAC]  get login history and logs')


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

#sys.exit()

# parse input params
argc = len(sys.argv)
if argc == 2 :
	if sys.argv[1] == '-h' or sys.argv[1] == '--help' :
		usage()
		sys.exit()
	else :
		mac = sys.argv[1]

		clients = dict()
		for f in files:
			c = list_all_clients(f)
			clients.update(c)

		print('{0:20}{1:22}{2:22}{3:22}{4:22}{5:18}{6:18}'.format("MAC", "Online", "Login","Logoff", "Offline", "Upload(KB)", "Download(KB)"))
		print("-------------------------------------------------------------------------------")
		for k in clients:
			if k == mac :
    				print(clients[k])
				print("-------------------------------------------------------------------------------")
				clients[k].showevents()


	print("list " + mac)
else :
	clients = dict()
	for f in files:
		print("Now process: " + f)
		time.sleep(1)
		c = list_all_clients(f)
		print("{0} clients in {1}".format(len(c), f))
		clients.update(c)
	time.sleep(2)

	print('{0:20}{1:22}{2:22}{3:22}{4:22}'.format("MAC", "Online", "Login","Logoff", "Offline"))
	print("-------------------------------------------------------------------------------")
	for k in clients:
    		print(clients[k])
		print("There're {0} clients in the log".format(len(clients)))





