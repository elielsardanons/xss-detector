#!/usr/bin/env python3

import argparse
from xsshelper import searchForXSS

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--url', help='The url to search for XSS (http://victim.com/path?q=help)')
	parser.add_argument('--body', help='The application/x-www-form-urlencoded body content to send (\'param1=value1&param2=value2\')')
	parser.add_argument('--method', help='request method \'GET\' or \'POST\' (defaults to "GET")', default='GET')
	parser.add_argument('--threads', help='Number of threads to use while crawling the site', default=5)

	args = parser.parse_args()

	searchForXSS(args.url, args.method, args.body)

