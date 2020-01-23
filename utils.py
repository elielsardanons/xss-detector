import random
import string

def random_string(length=12):
	chars = string.ascii_lowercase
	return ''.join(random.choice(chars) for i in range(length))

def join_query_string(qs):
	fullQueryString = []
	for paramName in qs.keys():
		for paramValue in qs[paramName]:
			fullQueryString.append(paramName+"="+paramValue)
	return "&".join(fullQueryString)


