#
# YARA scan - Scan selected region (the whole file if not selected) with YARA
#
# Copyright (c) 2020, Nobutaka Mantani
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import binascii
import re
import string
import sys
import yara

def is_printable(s):
    """
    Return True if 's' is printable string
    """
    try:
        return all(c in string.printable.encode() for c in s)
    except TypeError:
        return False

try:
    import yara
except ImportError:
    exit(-1)

scanned_filepath = sys.argv[1]
rule_filepath = sys.argv[2]
offset = int(sys.argv[3])

try:
    with open(scanned_filepath, "rb") as f:
        data = f.read()
except Exception as e:
    print("Error: Cannot open file")
    print(e)
    exit(-2)

try:
    with open(rule_filepath, "rb") as f:
        rule = f.read()
    y = yara.compile(source=rule.decode())
except Exception as e:
    print("Error: invalid YARA rule")
    print(e)
    exit(-2)

try:
    match = y.match(data=data)
except Exception as e:
    print("Error: YARA scan failed")
    print(e)
    exit(-2)

if len(match) == 0:
    exit(0) # No YARA rule matched

for m in match:
    for i in range(0, len(m.strings)):
        if is_printable(m.strings[i][2]):
            print("Offset: 0x%x size: %s rule: %s tag: %s identifier: %s matched: %s" % (offset + m.strings[i][0], len(m.strings[i][2]), m.rule, " ".join(m.tags), m.strings[i][1], re.sub("[\r\n\v\f]", "", m.strings[i][2].decode())))
        else:
            print("Offset: 0x%x size: %s rule: %s tag: %s identifier: %s matched: %s (hex)" % (offset + m.strings[i][0], len(m.strings[i][2]), m.rule, " ".join(m.tags), m.strings[i][1], binascii.hexlify(m.strings[i][2]).decode()))

exit(1) # YARA rule matched
