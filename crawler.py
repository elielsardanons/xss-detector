import requests    
import re    
from urllib.parse import urlparse    

class XSSCrawler(object):
	def __init__(self, url):
		self.original_url = url
		self.parsed_original_url = urlparse(self.original_url)
		self.visited = set()

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
			if not urlparse(link).netloc:
				links[i] = base + link

		return set(filter(lambda x: 'mailto' not in x, links))

	def crawl(self, url):
		for link in self.get_links(url):
			if link in self.visited:
				continue
			if urlparse(link).netloc != self.parsed_original_url.netloc:
				# Only follow links with the same original link domain.
				continue
			print(f"Following new link {link}")
			self.visited.add(link)
			self.crawl(link)

	def start(self):
		self.crawl(self.original_url)

if __name__ == "__main__":                           
	crawler = XSSCrawler("https://despegar.com")
	crawler.start()
