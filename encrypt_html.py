#!/usr/bin/env python3

# encrypt_html.py --- Encrypt an HTML file.
# Copyright (C) 2012  Kenny Chan
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import subprocess
import re

usage = """
Usage: encrypt_html.py password [prompt] < input.html > output.html

The HTML page will be encrypted using AES-256-CBC, using the provided password.

The file requires OpenSSL to be installed. The generated web page uses CryptoJS
to decrypt the content.
"""

def write_head(prompt):
    print("""<!DOCTYPE html>
        <html>
        <head>
            <title>Encrypted document.</title>
            <meta charset="utf-8" />
            <script src="https://crypto-js.googlecode.com/svn/tags/3.0.2/build/rollups/aes.js"></script>
            <script>
            function dd() {
                var pp=document.getElementById("p").value;
                var ee=document.getElementById("e").innerHTML;
                var d = CryptoJS.AES.decrypt(ee,pp);
                var w = window.open();
                var dc = w.document;
                dc.open("text/html");
                dc.write(d.toString(CryptoJS.enc.Utf8))
                dc.close();
            }
            </script>
        </head>
        <body>
            <h1>Encrypted document</h1>
            <p>""", prompt, """</p>
            <form>
                <input type="password" id="p" />
                <input type="button" value="decrypt" onclick="dd();" />
            </form>
            <!-- Encrypted content: Do not modify starting from this line -->
            <div style="display:none;" id="e">""")

def write_tail():
    print("""
            </div>
        </body>
        </html>
    """);

def encrypt(password):
    escaped_password = re.sub(r'[\\"]', r'\\\1', password)
    sys.stdout.flush()
    subprocess.call(['openssl', 'enc', '-aes-256-cbc', '-a',
                     '-pass', 'pass:' + password])

def main(argv):
    if len(argv) <= 1:
        print(usage, file=sys.stderr)
    else:
        try:
            prompt = argv[2]
        except IndexError:
            prompt = 'Please enter password to continue:'
        write_head(prompt)
        encrypt(argv[1])
        write_tail()

if __name__ == '__main__':
    main(sys.argv)

