#
# RC6 decrypt - Decrypt selected region with RC6
#
# Copyright (c) 2023, Nobutaka Mantani
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
import sys
import tkinter
import tkinter.ttk
import tkinter.messagebox

sys.path.append("./lib")
import block_cipher

try:
    import refinery.units.crypto.cipher.rc6
except ImportError:
    exit(-2) # Binary Refinery is not installed

class RC6DecryptDialog(block_cipher.BlockCipherDialog):
    def process(self, **kwargs):
        rc6_key_size = (16, 24, 32)

        mode = self.combo_mode.get()
        key_size = rc6_key_size[self.combo_key_length.current()]
        segment_size = key_size * 8
        key_type = self.combo_key_type.get()
        key = self.entry_key.get()
        iv_type = self.combo_iv_type.get()
        iv = self.entry_iv.get()

        if key_type == "Hex":
            if re.match("^([0-9A-Fa-f]{2})+$", key):
                key = binascii.a2b_hex(key)
            else:
                tkinter.messagebox.showerror("Error:", message="Key is not in hex format.")
                return
        else:
            key = key.encode()

        if mode in ["CBC", "CFB", "OFB", "CTR"] and iv_type == "Hex":
            if re.match("^([0-9A-Fa-f]{2})+$", iv):
                iv = binascii.a2b_hex(iv)
            else:
                tkinter.messagebox.showerror("Error:", message="IV is not in hex format.")
                return
        else:
            iv = iv.encode()

        if len(key) != key_size:
            tkinter.messagebox.showerror("Error:", message="Key size must be %d bytes." % key_size)
            return

        if mode in ["CBC", "CFB", "OFB", "CTR"] and len(iv) != 16: # 128 bits
            tkinter.messagebox.showerror("Error:", message="IV size must be 16 bytes.")
            return

        try:
            if mode in ["CBC", "OFB", "CTR"]:
                cipher = refinery.units.crypto.cipher.rc6.rc6(key=key, iv=iv, mode=mode)
            elif mode == "CFB":
                cipher = refinery.units.crypto.cipher.rc6.rc6(key=key, iv=iv, mode=mode, segment_size=segment_size)
            elif mode == "ECB":
                cipher = refinery.units.crypto.cipher.rc6.rc6(key=key, mode=mode)

            plaintext = cipher.process(data=self.data)
        except Exception as e:
            tkinter.messagebox.showerror("Error:", message=e)
            self.root.quit()
            exit(1) # Not decrypted

        sys.stdout.buffer.write(plaintext)
        self.root.quit()
        exit(0) # Decrypted successfully

if __name__ == "__main__":
    # Receive data
    data = sys.stdin.buffer.read()

    dialog = RC6DecryptDialog(title="RC6 decrypt", data=data, use_key_length=True)
    dialog.show()
    exit(1) # Not decrypted
