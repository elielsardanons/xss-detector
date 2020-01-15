#!/usr/bin/env python3

import os
import urllib.parse

print('Content-Type: text/html\n\n<h1>Search query</h1><br />')
query_string = os.environ['QUERY_STRING']
SearchParams = [i.split('=') for i in query_string.split('&')] 

for key, value in SearchParams:
	print('<b>'+key+'</b>: '+urllib.parse.unquote(value)+'<br>\n')
