from urllib.parse import urlparse, parse_qs, urlencode
import requests

from utils import join_query_string

class URLRequest():

	def __init__(self, url, body=None, method="GET"):
		self.method = method
		self.original_url = url
		self.body = body
		self.parsed_url = urlparse(url)
		self.query_string = parse_qs(self.parsed_url.query)
		self.response = None
		if body:
			self.parsed_body = parse_qs(self.body)

	def run(self):
		if self.method == "GET":
			self.response = requests.get(self.__full_url())
		elif self.method == "POST":
			self.response = requests.post(self.__full_url(), data=self.body)
		return self.response

	def __full_url(self):
		return self.parsed_url.scheme + "://" + self.parsed_url.netloc + self.parsed_url.path + "?" + join_query_string(self.query_string) + self.parsed_url.fragment

	def __str__(self):
		return self.__full_url()
