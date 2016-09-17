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

class Future:
	def __init__(self):
		self.callbacks = []

	def resolve(self):
		for fn in self.callbacks:
			fn()

class Task:
	def __init__(self, coroutine):
		self.coroutine = coroutine
		self.step()

	def step(self):
		try:
			future = next(self.coroutine)
		except StopIteration:
			return
		future.callbacks.append(self.step)

def get(path):
	global n_job
	n_job += 1
	s = socket.socket()
	s.setblocking(False)	# non blocking socket, never waits till succeed
	try:
		s.connect(('www.hdwallpapers.in', PORT))
	except:
		pass

	f = Future()
	selector.register(s.fileno(), EVENT_WRITE, f)
	yield f
	selector.unregister(s.fileno())

	request = 'GET %s HTTP/1.0\r\n\r\n' % path
	s.send(request.encode())

	buf = []

	while True:
		f = Future()
		selector.register(s.fileno(), EVENT_READ, f)
		yield f
		selector.unregister(s.fileno())

		chunk = s.recv(BUF_SIZE)
		if chunk:
			buf.append(chunk)
			f = Future()
			selector.register(s.fileno(), EVENT_READ, f)
			yield f
			selector.unregister(s.fileno())
		else:
			res = (b''.join(buf)).decode()
			print(res.split('\n')[0])
			n_job -= 1
			return

Task(get('/walls/huge_tiger_ride-wide.jpg'))
Task(get('/walls/huge_tiger_ride-wide.jpg'))

# event loop
while n_job:
	events = selector.select()
	# key, mask = event (EVENT_WRITE)
	for key, mask in events:
		future = key.data
		future.resolve()

print('%.2f seconds' % (time.time() - start))
