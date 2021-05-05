#!/usr/bin/env node

/*
 * pwnedpasswords_check.js
 * Interactive console session for querying the Pwned Passwords service
 * Copyright (C) 2021 Scott Brown
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 */

const getpass = require('getpass');
const crypto = require('crypto');
const fetch = require('node-fetch');

const RED = '\x1b[91m';
const GREEN = '\x1b[92m';
const ENDC = '\x1b[0m';


async function pwnedpasswords_check(p) {

	let h = crypto.createHash('sha1')
			.update(p)
			.digest('hex')
			.toUpperCase()

	let prefix = h.substring(0,5), suffix = h.substring(5);

	const url = 'https://api.pwnedpasswords.com/range/' + prefix;
	const response = await fetch(url, {"headers": {"User-Agent":"Node-Pwnedpasswords-Check"}});
	const content = await response.text();

	let match = content.split('\r\n')
			.filter(x => x.startsWith(suffix));

	return match.length ? Number(match[0].split(':')[1]) : 0;

}

function prompt() {

	getpass.getPass({"prompt":"Password to test (or blank to exit)"},
		async function (err, p) {

			if ( err ) process.exit(0); // error, bail

			p = p.trim();
			if ( ! p.length ) process.exit(0); // blank input (user exit intent)

			let occurrences = await pwnedpasswords_check(p);

			if ( occurrences ) {
				console.log(`${RED}${occurrences} occurrences${ENDC}`);
			} else {
				console.log(`${GREEN}no occurrences${ENDC}`);
			}

			console.log(); // spacer

			prompt();

		}
	);

}

if ( require.main === module ) {
	prompt();
}

module.exports = { pwnedpasswords_check };
