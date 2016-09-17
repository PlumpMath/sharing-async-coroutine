from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT = 8080

def gen(path):
	res = ''.join(map(lambda x: path, xrange(10000000)))
	return res

class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(gen(self.path))
		return

server = HTTPServer(('', PORT), MyHandler)

print 'Started httpserver on port ', PORT

try:
	server.serve_forever()
except:
	pass

server.server_close()
