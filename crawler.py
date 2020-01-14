import requests    
import re    
from urllib.parse import urlparse    

class XSSCrawler(object):    
	def __init__(self, url):
		self.url = url
		self.domain = urlparse(url).netloc
		self.visited = set()

	def get_html(self, url):
		try:
			html = requests.get(url)
		except Exception as e:
			return ""
		return html.content.decode('UTF-8')    

	def get_links(self, url):
		html = self.get_html(url)
		parsed = urlparse(url)
		base = f"{parsed.scheme}://{parsed.netloc}"
		links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
		for i, link in enumerate(links):
			link_domain = urlparse(link).netloc
			print(f"link_domain = {link_domain} [{link}]")
			if not link_domain:
				link_with_base = base + link
				links[i] = link_with_base
			elif link_domain != self.domain:
				del links[i]

		return set(filter(lambda x: 'mailto' not in x, links))

	def crawl(self, url):
		for link in self.get_links(url):
			if link in self.visited:
				continue
			print(link)
			self.visited.add(link)
			self.crawl(link)

	def start(self):
		self.crawl(self.url)

if __name__ == "__main__":                           
	crawler = XSSCrawler("https://despegar.com")        
	crawler.start()
