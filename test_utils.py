import unittest
from utils import join_query_string, random_string

class UtilsTest(unittest.TestCase):
	
	def test_join_query_string(self):
		self.assertEqual(join_query_string({'param1':['value1'], 'param2':['value2']}), 'param1=value1&param2=value2')

	def test_random_string(self):
		for i in range(100):
			self.assertNotEqual(random_string(), random_string())


if __name__ == '__main__':
	unittest.main()
