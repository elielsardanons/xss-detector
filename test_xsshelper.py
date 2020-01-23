import unittest
import threading
from http.server import CGIHTTPRequestHandler, HTTPServer

from xsshelper import search_for_xss
from urlrequest import URLRequest

class XSSHelperTest(unittest.TestCase):
	daemon = None

	def setUp(self):
		self.daemon = threading.Thread(name='daemon_server', target=self.start_http_server)
		self.daemon.setDaemon(True)
		self.daemon.start()

	def start_http_server(self):
		handler = CGIHTTPRequestHandler
		handler.cgi_directories = ['/vuln-site']  # this is the default
		server = HTTPServer(('localhost', 8123), handler)
		server.serve_forever()
	
	def test_search_for_xss(self):
		r = search_for_xss(URLRequest("http://localhost:8123/vuln-site/index.py?q=hola"))
		self.assertEqual(r[0]["url"].original_url, "http://localhost:8123/vuln-site/index.py?q=hola")
		self.assertEqual(r[0]["param"], "q")

	def teardown(self):
		self.daemon.stop()
	
if __name__ == '__main__':
	unittest.main()
