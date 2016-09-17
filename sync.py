import socket
import time

PORT = 80
BUF_SIZE = 1000

start = time.time()

def get(path):
	s = socket.socket()
	s.connect(('www.hdwallpapers.in', PORT))

	request = 'GET %s HTTP/1.0\r\n\r\n' % path
	s.send(request.encode())
	
	buf = []

	while True:
		chunk = s.recv(BUF_SIZE)  # blocking, EVENT_READ
		if chunk:
			buf.append(chunk)
		else:
			res = b''.join(buf).decode()
			print(res.split('\n')[0])
			return

get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')
get('/walls/huge_tiger_ride-wide.jpg')

print('%.2f seconds' % (time.time() - start))