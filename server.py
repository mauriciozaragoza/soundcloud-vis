import soundcloud
from collections import Counter
import BaseHTTPServer
import SocketServer
import time
import json
import urllib
from pymongo import MongoClient
from bson import json_util
import datetime
import urlparse

client = MongoClient()
db = client.soundmongers
results = db.results

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
		params =  urlparse.urlparse(s.path)
		print s.path
		qs = urlparse.parse_qs(params.query)
		genre = qs["genre"][0] if "genre" in qs else ''
		n = int(qs["n"][0])
		result = json.dumps(getSongs(n, genre.lower()), default=json_util.default)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write(result)

def getSongs(n, genre):
	client = soundcloud.Client(client_id = "1fb9f95527afeacbe1b8be1971b4f6f8")

	if genre == '':
		tracks = client.get('/tracks', limit=n, order='created_at')
	else:
		tracks = client.get('/tracks', limit=n, order='created_at', genres=genre)

	result = []
	d = datetime.datetime.utcnow()

	cache = results.find({"genre": genre, "date": {"$gt": d - datetime.timedelta(minutes=1) }})

	if cache.count() >= n:
		print "CACHED FOR" + str(d)

		for track in cache:
			result.append(track)
	else:
		for track in tracks:
			track = {'id': track.id, 'genre': genre.lower(), 'realgenre': track.genre, 'date': d, 'url': "https://w.soundcloud.com/player/?url=" + urllib.quote_plus(track.uri, safe='/') + "&amp;auto_play=true&amp;hide_related=true&amp;show_comments=false&amp;show_user=false&amp;show_reposts=false&amp;visual=false&amp;single_active=false"}

			result.append(track)
	
		results.insert(result)

	return result[:n]


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

