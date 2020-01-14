import unittest
from utils import joinQueryString, randomString

class UtilsTest(unittest.TestCase):
	
	def test_joinQueryString(self):
		self.assertEqual(joinQueryString({'param1':['value1'], 'param2':['value2']}), 'param1=value1&param2=value2')

	def test_randomString(self):
		for i in range(100):
			self.assertNotEqual(randomString(), randomString())


if __name__ == '__main__':
	unittest.main()
