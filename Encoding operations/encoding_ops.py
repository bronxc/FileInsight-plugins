#
# Encoding operations - Various encoding operations
#
# Copyright (c) 2018, Nobutaka Mantani
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

import base64
import quopri
import string
import subprocess

def binary_data_to_hex_text(fi):
    """
    Convert binary data of selected region into hex text
    """
    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()

    if (length > 0):
        buf = list(fi.getDocument())
        newbuf = []

        for i in range(0, length):
            j = offset + i
            newbuf.append("%02x" % ord(buf[j]))

        fi.newDocument("New file", 1)
        fi.setDocument("".join(newbuf))

        print "Converted binary data from offset %s to %s (%s bytes) into hex text." % (hex(offset), hex(offset + length - 1), length)

def hex_text_to_binary_data(fi):
    """
    Convert hex text of selected region into binary data
    """
    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()
    string = list(fi.getSelection())

    hexchars = list("0123456789abcdefABCDEF")

    if (length >= 2):
        buf = []
        for i in range(0, len(string)):
            if string[i] in hexchars:
                buf.append(string[i])

        if len(buf) < 2:
            return

        newbuf = []
        i = 0
        while (i < len(buf) - 1):
            newbuf.append(chr(int(buf[i] + buf[i+1], 16)))
            i += 2
        fi.newDocument("New file", 1)
        fi.setDocument("".join(newbuf))

        print "Converted hex text from offset %s to %s (%s bytes) into binary data (non-hex characters are skipped)." % (hex(offset), hex(offset + length - 1), length)

def custom_base64_decode(fi):
    """
    Decode selected region with custom base64 table
    """
    standard_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()

    if (length > 0):
        # Do not show command prompt window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Execute dialog.py to show GUI
        # GUI portion is moved to dialog.py to avoid hangup of FileInsight
        p = subprocess.Popen(["python", "custom_base64_decode_dialog.py"], startupinfo=startupinfo, stdout=subprocess.PIPE)

        # Get base64 table input
        stdout_data, stderr_data = p.communicate()
        custom_table = stdout_data.rstrip()
        custom_table_length = len(custom_table)

        if (custom_table_length > 0):
            if (custom_table_length != 65):
                print "Error: base64 table must be 65 characters (including padding)."
            else:
                data = fi.getSelection()
                orig = list(fi.getDocument())
                orig_len = len(orig)

                trans = string.maketrans(custom_table, standard_table)
                encoded = list(base64.b64decode(data.translate(trans)))
                final_size = len(encoded)

                newdata = orig[:offset]
                newdata.extend(encoded)
                newdata.extend(orig[offset + length:])

                fi.newDocument("New file", 1)
                fi.setDocument("".join(newdata))
                fi.setBookmark(offset, final_size, hex(offset), "#c8ffff")

                if (length == 1):
                    print "Decoded one byte with custom base64 table from offset %s to %s." % (hex(offset), hex(offset))
                else:
                    print "Decoded %s bytes with custom base64 table from offset %s to %s." % (length, hex(offset), hex(offset + length - 1))

def custom_base64_encode(fi):
    """
    Encode selected region with custom base64 table
    """
    standard_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()

    if (length > 0):
        # Do not show command prompt window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Execute dialog.py to show GUI
        # GUI portion is moved to dialog.py to avoid hangup of FileInsight
        p = subprocess.Popen(["python", "custom_base64_encode_dialog.py"], startupinfo=startupinfo, stdout=subprocess.PIPE)

        # Get base64 table input
        stdout_data, stderr_data = p.communicate()
        custom_table = stdout_data.rstrip()
        custom_table_length = len(custom_table)

        if (custom_table_length > 0):
            if (custom_table_length != 65):
                print "Error: base64 table must be 65 characters (including padding)."
            else:
                data = fi.getSelection()
                orig = list(fi.getDocument())
                orig_len = len(orig)

                trans = string.maketrans(standard_table, custom_table)
                encoded = list(base64.b64encode(data).translate(trans))
                final_size = len(encoded)

                newdata = orig[:offset]
                newdata.extend(encoded)
                newdata.extend(orig[offset + length:])

                fi.newDocument("New file", 1)
                fi.setDocument("".join(newdata))
                fi.setBookmark(offset, final_size, hex(offset), "#c8ffff")

                if (length == 1):
                    print "Encoded one byte with custom base64 table from offset %s to %s." % (hex(offset), hex(offset))
                else:
                    print "Encoded %s bytes with custom base64 table from offset %s to %s." % (length, hex(offset), hex(offset + length - 1))

def rot13(fi):
    """
    Rotate alphabet characters in selected region
    """
    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()

    if (length > 0):
        buf = list(fi.getDocument())
        data = fi.getSelection()

        # Do not show command prompt window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Execute rot13_dialog.py to show GUI
        # GUI portion is moved to rot13_dialog.py to avoid hangup of FileInsight
        p = subprocess.Popen(["python", "rot13_dialog.py"], startupinfo=startupinfo, stdout=subprocess.PIPE)

        # Get amount input
        stdout_data, stderr_data = p.communicate()
        amount = stdout_data.rstrip()
        if len(amount) > 0:
            amount = int(amount)

            if amount < 0:
                amount = 26 - (abs(amount) % 26)
            elif amount == 0:
                return
            else:
                amount = amount % 26
        else:
            return

        # Create a dictionary for rotation
        d = {}
        for c in (0x41, 0x61): # "A" and "a"
            for i in range(26):
                d[chr(i + c)] = chr((i + amount) % 26 + c)

        for i in range(0, length):
            buf[offset + i] = d.get(data[i], data[i])

        fi.newDocument("New file", 1)
        fi.setDocument("".join(buf))
        fi.setBookmark(offset, length, hex(offset), "#c8ffff")

        if (length == 1):
            print "Decoded one byte from offset %s to %s." % (hex(offset), hex(offset))
        else:
            print "Decoded %s bytes from offset %s to %s." % (length, hex(offset), hex(offset + length - 1))
        print "Added a bookmark to decoded region."

def from_quoted_printable(fi):
    """
    Decode selected region as quoted printable text
    """
    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()

    if (length > 0):
        data = fi.getSelection()
        orig = list(fi.getDocument())
        orig_len = len(orig)

        decoded = list(quopri.decodestring(data))
        final_size = len(decoded)

        newdata = orig[:offset]
        newdata.extend(decoded)
        newdata.extend(orig[offset + length:])

        fi.newDocument("New file", 1)
        fi.setDocument("".join(newdata))
        fi.setBookmark(offset, final_size, hex(offset), "#c8ffff")

        if (length == 1):
            print "Decoded one byte quoted printable text from offset %s to %s." % (hex(offset), hex(offset))
        else:
            print "Decoded %s bytes quoted printable text from offset %s to %s." % (length, hex(offset), hex(offset + length - 1))

def to_quoted_printable(fi):
    """
    Encode selected region into quoted printable text
    """
    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()

    if (length > 0):
        data = fi.getSelection()
        orig = list(fi.getDocument())
        orig_len = len(orig)

        encoded = list(quopri.encodestring(data))
        final_size = len(encoded)

        newdata = orig[:offset]
        newdata.extend(encoded)
        newdata.extend(orig[offset + length:])

        fi.newDocument("New file", 1)
        fi.setDocument("".join(newdata))
        fi.setBookmark(offset, final_size, hex(offset), "#c8ffff")

        if (length == 1):
            print "Encoded one byte into quoted printable text from offset %s to %s." % (hex(offset), hex(offset))
        else:
            print "Encoded %s bytes into quoted printable text from offset %s to %s." % (length, hex(offset), hex(offset + length - 1))

def binary_data_to_binary_text(fi):
    """
    Convert binary data of selected region into binary text
    """
    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()

    if (length > 0):
        buf = list(fi.getDocument())
        newbuf = []

        for i in range(0, length):
            j = offset + i
            newbuf.append("{0:b}".format(ord(buf[j])).zfill(8))

        fi.newDocument("New file", 1)
        fi.setDocument("".join(newbuf))

        print "Converted binary from offset %s to %s (%s bytes) into binary text." % (hex(offset), hex(offset + length - 1), length)

def binary_text_to_binary_data(fi):
    """
    Convert binary text of selected region into binary data
    """
    offset = fi.getSelectionOffset()
    length = fi.getSelectionLength()
    string = list(fi.getSelection())

    binchars = list("01")

    if (length >= 8):
        buf = []
        for i in range(0, len(string)):
            if string[i] in binchars:
                buf.append(string[i])

        if len(buf) < 8:
            return

        newbuf = []
        i = 0
        while (i < len(buf) - 7):
            newbuf.append(chr(int("".join(buf[i:i+8]), 2)))
            i += 8
        fi.newDocument("New file", 1)
        fi.setDocument("".join(newbuf))

        print "Converted binary text from offset %s to %s (%s bytes) into binary data." % (hex(offset), hex(offset + length - 1), length)

