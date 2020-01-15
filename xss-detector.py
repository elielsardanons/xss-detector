#!/usr/bin/env python3

import argparse
from concurrent.futures import ThreadPoolExecutor

from xsshelper import search_for_xss
from crawler import Crawler

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--url', help='The url to search for XSS (http://victim.com/path?q=help)')
	parser.add_argument('--body', help='The application/x-www-form-urlencoded body content to send (\'param1=value1&param2=value2\')')
	parser.add_argument('--method', help='request method \'GET\' or \'POST\' (defaults to "GET")', default='GET')
	parser.add_argument('--threads', help='Number of threads to use while crawling the site', default=5)

	args = parser.parse_args()

	# Scan the first given URL
	search_for_xss(args.url, args.method, args.body)

	# Initialize thread pool
	executor = ThreadPoolExecutor(max_workers=args.threads)

	# Start crawling and scanning the other found URLs
	crawler = Crawler(args.url, args.method, args.body, search_for_xss, executor)
	crawler.start()

	# wait till every xss detection function is done.
	for future in crawler.futures:
		future.result()


