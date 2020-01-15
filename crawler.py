import requests
import re
from urllib.parse import urlparse

class Crawler(object):
	def __init__(self, url, method, body, func, func_thread_pool):
		self.original_url = url
		self.original_method = method
		self.original_body = body
		self.parsed_original_url = urlparse(self.original_url)
		self.visited = set(url)
		self.func = func
		self.func_thread_pool = func_thread_pool
		self.futures = []

	def get_html(self, url):
		try:
			html = requests.get(url)
		except Exception as e:
			return ""
		return html.content.decode('UTF-8')    

	def get_links(self, url):
		html = self.get_html(url)
		base = f"{self.parsed_original_url.scheme}://{self.parsed_original_url.netloc}"
		links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
		for i, link in enumerate(links):
			parsed_link = urlparse(link)
			if not parsed_link.netloc:
				links[i] = base + link
			elif not parsed_link.scheme and parsed_link.netloc:
				# complete links like //victim.com/test?param=value
				links[i] = self.parsed_original_url.scheme + ":" + link

		return set(filter(lambda x: 'mailto' not in x, links))

	def crawl(self, url):
		for link in self.get_links(url):
			try:
				if link in self.visited:
					continue
				if urlparse(link).netloc != self.parsed_original_url.netloc:
					# Only follow links with the same original link domain.
					continue
				self.visited.add(link)
				# search for injectable params in the given URL.
				self.futures.append(self.func_thread_pool.submit(self.func, link))
				self.crawl(link)
			except Exception:
				print(f"We where unable to follow link: {link}")

	def start(self):
		self.crawl(self.original_url)

