#!/us/bin/env python3

import redis
import time

pool = redis.ConnectionPool(host='172.16.20.50', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

#r.set('bing', 'baz')

# pipeline
#pipe = r.pipeline()
#pipe.set('foo', 'bar')
#pipe.get('bing')

#pipe.execute()

start = time.time()
i = 0
while i < 10000:
	r.publish('commands', '%s|%d'%('88|31000|4|EC01EE039C51',i))
	i = i+1

stop = time.time()

print('Send', i, 'commands cost time:', stop-start)
