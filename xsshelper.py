from db import DB
from utils import random_string
from inject import input_reflected, inject_query_string, inject_body_param, inject_payloads
from urlrequest import URLRequest
from termcolors import TermColors

def store_xss_result(detectedXSS, dbpath):
	db = DB(dbpath)
	for xss in detectedXSS:
		db.store_xss(str(xss["url"]), xss["param"])


def search_for_xss(url):
	print(f"Serching for XSSs in {TermColors.GREEN}{url.original_url}{TermColors.ENDC}")
	allReflectedBodyParams = []
	allReflectedParams = []
	detectedXSS = []

	# Get all the query strings and body params that could be vulnerable.
	allReflectedQueryParams = input_reflected(url, url.query_string.keys(), random_string(), inject_query_string)

	if url.method == "POST":
		allReflectedBodyParams = input_reflected(url, url.parsed_body.keys(), random_string(), inject_body_param)

	# Show the found params that could be vulnerable.
	for reflectedParam in allReflectedQueryParams:
		print(f"{TermColors.YELLOW}{reflectedParam}{TermColors.ENDC} could be vulnerable because its value was reflected.")

	for reflectedBodyParam in allReflectedBodyParams:
		print(f"{TermColors.YELLOW}{reflectedBodyParam}{TermColors.ENDC} body param could be vulnerable because its value was reflected.")


	# start injecting different payloads in found injectable params.
	for reflectedQueryParam in allReflectedQueryParams:
		found = inject_payloads(url, reflectedParam, inject_query_string)
		if found:
			print(f"{TermColors.GREEN}{url.original_url}{TermColors.ENDC} is vulnerable to XSS! query param {TermColors.BLUE}{reflectedParam}{TermColors.ENDC} is injectable")
			detectedXSS.append({"url":url, "param":reflectedQueryParam})


	for reflectedBodyParam in allReflectedBodyParams:
		found = inject_payloads(url, reflectedParam, inject_body_param) 
		if found:
			print(f"{TermColors.GREEN}{url.original_url}{TermColors.ENDC} is vulnerable to XSS! body param {TermColors.BLUE}{reflectedParam}{TermColors.ENDC} is injectable")
			detectedXSS.append({"url":url, "param":reflectedBodyParam})

	return detectedXSS
