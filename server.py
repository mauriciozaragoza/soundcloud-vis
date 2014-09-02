import soundcloud
from collections import Counter
import BaseHTTPServer
import SocketServer
import time
import json

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	def do_GET(s):
		s.send_response(200)
		s.send_header("Access-Control-Allow-Origin", "*");
		s.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin");
		s.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
		path = s.path.split("=")
		n = path[-1]
		result = json.dumps(getSongs(n))
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write(result)

def getSongs(n):
	client = soundcloud.Client(client_id = "1fb9f95527afeacbe1b8be1971b4f6f8")
	tracks = client.get('/tracks', limit=n)
	genres = []
	for track in tracks:
		t = track.genre
		if (not t):
			t = "None"
		genres.append(t.lower().encode('utf-8'))
	return genres


HOST_NAME = "127.0.0.1"
PORT_NUMBER = 9000

server_class = BaseHTTPServer.HTTPServer
httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()
print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)