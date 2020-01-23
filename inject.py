import copy

def inject_query_string(url_request, name, value):
	url_request_modified = copy.deepcopy(url_request)
	url_request_modified.query_string[name].clear()
	url_request_modified.query_string[name].append(value)
	return url_request_modified

def inject_body_param(url_request, name, value):
	url_request_modified = copy.deepcopy(url_request)
	url_request_modified.parsed_body[name].clear()
	url_request_modified.parsed_body[name].append(value)
	return url_request_modified

def input_reflected(url_request, params, injectedValue, insertionPoint = inject_query_string):
	reflectedInput = []
	for query_param in params:
		http_response = insertionPoint(url_request, query_param, injectedValue).run()
		html_response = http_response.content
		if html_response.find(bytearray(injectedValue.encode('UTF-8'))) != -1:
			reflectedInput.append(query_param)

	return reflectedInput


def load_xss_payloads():
	payloads = open("payloads.xss", "r")
	allPayloads = payloads.readlines()
	payloads.close()
	return allPayloads

def inject_payloads(url_request, query_param, insertionPoint):
	payloads = load_xss_payloads()

	for payload in payloads:
		result = input_reflected(url_request, [query_param], payload, insertionPoint)
		if len(result) > 0:
			return True
	return False



