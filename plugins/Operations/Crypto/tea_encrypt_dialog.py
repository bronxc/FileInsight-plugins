#
# TEA encrypt - Encrypt selected region with TEA (Tiny Encryption Algorithm)
#
# Copyright (c) 2021, Nobutaka Mantani
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
import time
import tkinter
import tkinter.ttk
import tkinter.messagebox

try:
    import pytea
except ImportError:
    exit(-2) # PyTEA is not installed

# Encrypt received data
def encrypt(data, root, combo, entry):
    key = entry.get()

    if combo.get() == "Hex":
        if re.match("^([0-9A-Fa-f]{2})+$", key):
            key = binascii.a2b_hex(key)
        else:
            tkinter.messagebox.showerror("Error:", message="Key is not in hex format.")
            return
    else:
        key = key.encode()

    if len(key) != 16:
        tkinter.messagebox.showerror("Error:", message="Key length must be 16 bytes.")
        return

    try:
        cipher = pytea.TEA(key)
        e = cipher.encrypt(data)
    except:
        root.quit()
        exit(1) # Not decrypted

    sys.stdout.buffer.write(e)
    root.quit()
    exit(0) # Decrypted successfully

# Receive data
data = sys.stdin.buffer.read()

# Create input dialog
root = tkinter.Tk()
root.title("TEA encrypt")
root.protocol("WM_DELETE_WINDOW", (lambda root=root: root.quit()))

label = tkinter.Label(root, text="Key:")
label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

combo = tkinter.ttk.Combobox(root, width=5, state="readonly")
combo["values"] = ("Text", "Hex")
combo.current(0)
combo.grid(row=0, column=1, padx=5, pady=5)

entry = tkinter.Entry(width=40)
entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

button = tkinter.Button(root, text="OK", command=(lambda data=data, root=root, combo=combo, entry=entry: encrypt(data, root, combo, entry)))
button.grid(row=2, column=0, padx=5, pady=5, columnspan=3)

# Adjust window position
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.update_idletasks() # Necessary to get width and height of the window
ww = root.winfo_width()
wh = root.winfo_height()
root.geometry('+%d+%d' % ((sw/2) - (ww/2), (sh/2) - (wh/2)))

root.mainloop()
exit(1) # Not decrypted
