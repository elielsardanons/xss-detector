from utils import randomString
from inject import inputReflected, injectQueryString, injectBodyParam, injectPayloads
from urlrequest import URLRequest
from termcolors import TermColors

def searchForXSS(url, method, body=None):
	allReflectedBodyParams = []
	allReflectedParams = []
	detectedXSS = []

	u = URLRequest(url, body=body, method=method)

	# Get all the query strings and body params that could be vulnerable.
	allReflectedQueryParams = inputReflected(u, u.query_string.keys(), randomString(), injectQueryString)

	if u.method == "POST":
		allReflectedBodyParams = inputReflected(u, u.parsed_body.keys(), randomString(), injectBodyParam)

	# Show the found params that could be vulnerable.
	for reflectedParam in allReflectedQueryParams:
		print(f"{TermColors.YELLOW}{reflectedParam}{TermColors.ENDC} could be vulnerable because its value was reflected.")

	for reflectedBodyParam in allReflectedBodyParams:
		print(f"{TermColors.YELLOW}{reflectedBodyParam}{TermColors.ENDC} body param could be vulnerable because its value was reflected.")


	# start injecting different payloads in found injectable params.
	for reflectedQueryParam in allReflectedQueryParams:
		found = injectPayloads(u, reflectedParam, injectQueryString)
		if found:
			print(f"{TermColors.GREEN}{u.original_url}{TermColors.ENDC} is vulnerable to XSS! query param {TermColors.BLUE}{reflectedParam}{TermColors.ENDC} is injectable")
			detectedXSS.append(reflectedQueryParam)

	for reflectedBodyParam in allReflectedBodyParams:
		found = injectPayloads(u, reflectedParam, injectBodyParam) 
		if found:
			print(f"{TermColors.GREEN}{u.original_url}{TermColors.ENDC} is vulnerable to XSS! body param {TermColors.BLUE}{reflectedParam}{TermColors.ENDC} is injectable")
			detectedXSS.append(reflectedQueryParam)

	return detectedXSS
