#!/usr/bin/env python3

import getpass
import sys
import hashlib
import urllib.request

RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

while True:

	try:
		p = getpass.getpass(prompt='Password to test (or blank to exit): ')
	except (EOFError, KeyboardInterrupt): # trap ctrl+d, ctrl+c
		print() # newline
		sys.exit() # bail

	p = p.strip()
	if not p: sys.exit() # blank input (user exit intent), bail

	h = hashlib.sha1(p.encode()).hexdigest().upper()
	prefix, suffix = h[:5], h[5:]

	url = 'https://api.pwnedpasswords.com/range/' + prefix
	req = urllib.request.Request(url)
	req.add_header('User-Agent', 'Python-Pwnedpasswords-Check')
	res = urllib.request.urlopen(req)
	content = res.read().decode()

	match = [l for l in content.split() if suffix in l]
	if match:
		occurrences = match[0].split(':')[1]
		print(f'{RED}{occurrences} occurrences{ENDC}')
	else:
		print(f'{GREEN}No occurrences{ENDC}')

	print() # spacer
