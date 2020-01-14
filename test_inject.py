import unittest
from urlrequest import URLRequest
from inject import *

class InjectTest(unittest.TestCase):
	
	def test_injectBodyParam(self):
		u = URLRequest('http://www.google.com', body='param1=value1&param2=value2', method='POST')
		self.assertEqual(injectBodyParam(u, 'param2', 'test').parsed_body['param2'], ['test'])

	def test_injectQueryString(self):
		u = URLRequest('http://www.google.com?param1=value1&param2=value2')
		self.assertEqual(injectQueryString(u, 'param2', 'test').query_string['param2'], ['test'])


if __name__ == '__main__':
	unittest.main()
