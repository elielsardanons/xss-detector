import random
import string

def randomString(length=12):
	chars = string.ascii_lowercase
	return ''.join(random.choice(chars) for i in range(length))

def joinQueryString(qs):
	fullQueryString = []
	for paramName in qs.keys():
		for paramValue in qs[paramName]:
			fullQueryString.append(paramName+"="+paramValue)
	return "&".join(fullQueryString)


