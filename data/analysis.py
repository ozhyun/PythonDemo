#env /usr/bin/python 

import time
import os
import re

class Client:
    """client """

    def __str__(self):
        return '{0:20}{1:22}{2:22}{3:22}{4:22}'.format(self.mac, self.online_time, self.login_time, self.logoff_time, self.offline_time)


clients = dict()

file = 'client.log-20190604'
lines = 0
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
           
            if items[3] in clients:
                c = clients[items[3]]
            else:
                c = Client()
                c.login_time = '-'
                c.mac = items[3]
                c.online_time ='-' 
                c.login_time = '-'
                c.logoff_time = '-'
                c.offline_time = '-'
                clients[c.mac] = c
            
            if items[17] == 'client_add':
                c.online_time = items[0]
            elif items[17] == 'client_state_switch' and items[18] == 'client_state_common2white':
                c.login_time = items[0]
            elif items[17] == 'client_del':
                c.offline_time = items[0]


            #print("MAC      Online              Login         Logoff                 Offline")
            #print("-------------------------------------------------------------------------------")
            #print(c)
        else:
            break


print('{0:20}{1:22}{2:22}{3:22}{4:22}'.format("MAC", "Online", "Login","Logoff", "Offline"))
print("-------------------------------------------------------------------------------")
for k in clients:
    print(clients[k])
