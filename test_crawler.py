import unittest
import threading
from http.server import CGIHTTPRequestHandler, HTTPServer
from concurrent.futures import ThreadPoolExecutor

from xsshelper import search_for_xss
from crawler import Crawler
from urlrequest import URLRequest

class CrawlerTest(unittest.TestCase):
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
	
	def test_crawler(self):
		pool = ThreadPoolExecutor(5)
		crawler = Crawler(URLRequest("http://localhost:8123/vuln-site/something.py"), search_for_xss, pool)
		crawler.start()

		self.assertEqual(crawler.func_result[1][0]["url"].original_url, "http://localhost:8123/vuln-site/index.py?q=eliel")
		self.assertEqual(crawler.func_result[1][0]["param"], "q")

	def teardown(self):
		self.daemon.stop()
	
if __name__ == '__main__':
	unittest.main()
