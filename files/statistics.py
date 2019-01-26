#!/usr/bin/env python3

#class app:
	

fd = open('result.txt', 'r')

applist = []
recv_bytes_total = 0
recv_pkts_total = 0
send_bytes_total = 0
send_pkts_total = 0

account = 0
fd.readline()
for line in fd:
	#print("#%d: %s" % (account, line.strip()))
	attr = line.strip().split(',')
	a = {}
	a["id"] = int(attr[0])
	a["recv_bytes"] = int(attr[1])
	a["recv_pkts"] = int(attr[2])
	a["send_bytes"] = int(attr[3])
	a["send_pkts"] = int(attr[4])
	#print(attr)
	#print(a)
	recv_bytes_total += a['recv_bytes']
	recv_pkts_total += a['recv_pkts']
	send_bytes_total += a['send_bytes']
	send_pkts_total += a['send_pkts']

	applist.append(a)
	account += 1

fd.close()

#print(applist)
print('There are %s Applications' % account)

for app in applist:
	app["recv_bytes_ratio"] = app["recv_bytes"] / recv_bytes_total * 100
	app["recv_pkts_ratio"] = app["recv_pkts"] / recv_pkts_total * 100
	app["send_bytes_ratio"] = app["send_bytes"] / send_bytes_total * 100
	app["send_pkts_ratio"] = app["send_pkts"] / send_pkts_total * 100

#print(applist)

for app in applist:
	#print(str(app["id"]) + " : " + app["recv_bytes"] +"/" + app["recv_bytes_ratio"] + " " + \
	#	app["recv_pkts"] + "/" + app["recv_pkts_ratio"] + " " + \
	#	app["send_bytes"] + "/" + app["send_bytes_ratio"] + " " + \
	#	app["send_pkts"] + "/" + app["send_pkts_ratio"] )
	print("APP[{id}] : \tRecv {rbytes:*>10}KB/{rb_ratio:5.2f}  {rpkts:*>15}/{rpkts_ratio:>5.2f}| \tSend {tbytes:*>10}KB/{tb_ratio:>5.2f} \t{tpkts:*>15}/{tpkts_ratio:>5.2f}".format( \
		id=app["id"], rbytes=app["recv_bytes"]//1024, rb_ratio=app["recv_bytes_ratio"], \
		rpkts=app["recv_pkts"], rpkts_ratio=app["recv_pkts_ratio"], \
		tbytes=app["send_bytes"]//1024, tb_ratio=app["send_bytes_ratio"], \
		tpkts=app["send_pkts"], tpkts_ratio=app["send_pkts_ratio"]))
