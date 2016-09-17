# - async I/O
#	- non-blocking sockets
#	- callbacks (not elegant, replace with coroutines)
#	- event loop
#	- efficiency! (single-threaded concurrency)

# - coroutines
#	- Future
#	- generators
#	- Task

import socket
import time
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

PORT = 80
BUF_SIZE = 1000

selector = DefaultSelector()

start = time.time()

n_job = 0

def get(path):
	global n_job
	n_job += 1
	s = socket.socket()
	s.setblocking(False)	# non blocking socket, never waits till succeed
	try:
		s.connect(('www.hdwallpapers.in', PORT))
	except BlockingIOError:
		pass

	callback = lambda: connected(s, path)	
	# fileobj, events, data
	selector.register(s.fileno(), EVENT_WRITE, callback)

def connected(s, path):
	selector.unregister(s.fileno())
	request = 'GET %s HTTP/1.0\r\n\r\n' % path
	s.send(request.encode())

	buf = []
	callback = lambda: readable(s, buf)
	selector.register(s.fileno(), EVENT_READ, callback)

def readable(s, buf):
	global n_job
	selector.unregister(s.fileno())
	chunk = s.recv(BUF_SIZE)
	if chunk:
		buf.append(chunk)
		callback = lambda: readable(s, buf)
		selector.register(s.fileno(), EVENT_READ, callback)
	else:
		res = (b''.join(buf)).decode()
		print(res.split('\n')[0])
		n_job -= 1

get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')

# event loop
while n_job:
	events = selector.select()
	# key, mask = event (EVENT_WRITE)
	for key, mask in events:
		callback_func = key.data
		callback_func()

print('%.2f seconds' % (time.time() - start))
