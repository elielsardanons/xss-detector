#!/usr/bin/env python3

import argparse
from concurrent.futures import ThreadPoolExecutor

from xsshelper import search_for_xss, store_xss_result
from crawler import Crawler
from urlrequest import URLRequest

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Search for Cross-site scripting')
	parser.add_argument('--url', help='The url to search for XSS (http://victim.com/path?q=help)')
	parser.add_argument('--body', help='The application/x-www-form-urlencoded body content to send (\'param1=value1&param2=value2\')')
	parser.add_argument('--method', help='request method \'GET\' or \'POST\' (defaults to "GET")', default='GET')
	parser.add_argument('--threads', help='Number of threads to use while crawling the site', default=5)
	parser.add_argument('--db', help='sqlite3 database name. (defaults to \'xss.db\')', default="xss.db")

	args = parser.parse_args()

	# Initialize thread pool
	thread_pool = ThreadPoolExecutor(max_workers=int(args.threads))

	# Start crawling and scanning the other found URLs
	crawler = Crawler(URLRequest(url = args.url, method = args.method, body = args.body), search_for_xss, thread_pool)
	crawler.start()

	for r in crawler.func_result:
		store_xss_result(r, args.db)

