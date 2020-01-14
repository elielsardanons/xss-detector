import copy

def injectQueryString(url_request, name, value):
	url_request_modified = copy.deepcopy(url_request)
	url_request_modified.query_string[name].clear()
	url_request_modified.query_string[name].append(value)
	return url_request_modified

def injectBodyParam(url_request, name, value):
	url_request_modified = copy.deepcopy(url_request)
	url_request_modified.parsed_body[name].clear()
	url_request_modified.parsed_body[name].append(value)
	return url_request_modified

def inputReflected(url_request, params, injectedValue, insertionPoint = injectQueryString):
	reflectedInput = []
	for query_param in params:
		html_response = insertionPoint(url_request, query_param, injectedValue).run().content
		if html_response.find(bytearray(injectedValue.encode('UTF-8'))) != -1:
			reflectedInput.append(query_param)

	return reflectedInput


def loadXSSPayloads():
	payloads = open("payloads.xss", "r")
	allPayloads = payloads.readlines()
	payloads.close()
	return allPayloads

def injectPayloads(url_request, query_param, insertionPoint):
	payloads = loadXSSPayloads()

	for payload in payloads:
		result = inputReflected(url_request, [query_param], payload, insertionPoint)
		if len(result) > 0:
			return True
	return False



