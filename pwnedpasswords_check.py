#!/usr/bin/env python3


"""
pwnedpasswords_check.py
Interactive console session for querying the Pwned Passwords service
Copyright (C) 2024 Scott Brown

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import getpass
import hashlib
import requests


RED = "\033[91m"
GREEN = "\033[92m"
ENDC = "\033[0m"


def pwnedpasswords_check(p):
    """Query Pwned Passwords for one password"""

    h = hashlib.sha1(p.encode()).hexdigest().upper()
    prefix, suffix = h[:5], h[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(
        url, headers={"User-Agent": "Python-Pwnedpasswords-Check"}, timeout=20
    )
    content = res.text

    match = list(filter(lambda x: suffix in x, content.split()))

    return int(match[0].split(":")[1]) if match else 0


def prompt():
    """Interactive query loop"""

    while True:

        try:
            p = getpass.getpass(prompt="Password to test (or blank to exit): ")
        except (EOFError, KeyboardInterrupt):  # trap ctrl+d, ctrl+c
            print()  # newline
            return  # bail

        p = p.strip()
        if not p:  # blank input (user exit intent)
            return  # bail

        occurrences = pwnedpasswords_check(p)

        if occurrences:
            print(f"{RED}{occurrences} occurrences{ENDC}")
        else:
            print(f"{GREEN}No occurrences{ENDC}")

        print()  # spacer


if __name__ == "__main__":

    # Entry point
    prompt()
