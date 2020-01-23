import requests
import re
from urllib.parse import urlparse
from lxml import html

from urlrequest import URLRequest
from utils import random_string, join_query_string

class Crawler():
	def __init__(self, urlrequest, func, func_thread_pool):
		self.urlrequest = urlrequest
		self.visited = set()
		self.func = func
		self.func_thread_pool = func_thread_pool
		self.func_thread_pool_result = []
		self.func_result = []

	def __get_urlrequest_from_form(self, basepath, form):
		body = None

		# Get form action URL
		action_url = urlparse(form.action)
		if not action_url.netloc:
			formurl = basepath + form.action

		# Retrieve form inputs.
		inputs = {}
		for i in form.inputs:
			if i.type == 'text':
				inputs[i.name] = [i.name+"_testvalue_1"]

		# Generate final URL request.
		if form.method == 'POST':
			body = join_query_string(inputs)
		else:
			formurl = formurl + '?' + join_query_string(inputs)

		return URLRequest(url = formurl, method=form.method, body=body)

	def get_urls(self, urlrequest):
		links = []
		try:
			httpresponse = urlrequest.run()
			htmlcontent = httpresponse.content.decode('UTF-8')
			xhtml = html.fromstring(htmlcontent)
			base = f"{self.urlrequest.parsed_url.scheme}://{self.urlrequest.parsed_url.netloc}"

			# Search for <a href="" />
			for (element, attr, link, pos) in xhtml.iterlinks():
				parsed_link = urlparse(link)
				if not parsed_link.netloc:
					links.append(URLRequest(base + link))
				elif not parsed_link.scheme and parsed_link.netloc:
					links.append(URLRequest(self.urlrequest.parsed_url.scheme + ":" + link))

			# Search for <form />
			for form in xhtml.xpath('//form'):
				links.append(self.__get_urlrequest_from_form(base + self.urlrequest.parsed_url.path, form))

		except Exception as e:
			print(e)
		finally:
			return links

	def crawl(self, urlrequest):
		for url in self.get_urls(urlrequest):
			try:
				if url.original_url in self.visited:
					continue
				if url.parsed_url.netloc != self.urlrequest.parsed_url.netloc:
					# Only follow links with the same original link domain.
					continue
				self.visited.add(url.original_url)
				# search for injectable params in the given URL.
				self.func_thread_pool_result.append(self.func_thread_pool.submit(self.func, url))
				self.crawl(url)
			except Exception as e:
				print(f"We where unable to follow link: {url.original_url}")
				print(e)

	def start(self):
		self.func_thread_pool_result.append(self.func_thread_pool.submit(self.func, self.urlrequest))
		self.crawl(self.urlrequest)
		for r in self.func_thread_pool_result:
			self.func_result.append(r.result())

