#
# Visual encrypt - Encode selected region with visual encrypt algorithm
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

import re
import tkinter

# Print key length to stdout
def print_key_length(r, s):
    if s.get() != "":
        print(s.get())
    else:
        print("1")
    root.quit()

def key_length_changed(*args):
    if not re.match("^-?([0-9])+$", key_length.get()):
        s = re.sub("[^-0-9]", "", key_length.get())
        if re.match("[0-9]+-", s):
            s = s.replace("-", "")
            key_length.set(s)
        else:
            key_length.set(s)
    elif int(key_length.get()) < 1:
        key_length.set("1")

# Create input dialog
root = tkinter.Tk()
root.title('Visual encrypt / decrypt')
root.protocol("WM_DELETE_WINDOW", (lambda r=root: r.quit()))
label = tkinter.Label(root, text="XOR key length:")
label.grid(row=0, column=0, padx=5, pady=5)
key_length = tkinter.StringVar()
key_length.set("1")
key_length.trace("w", key_length_changed)
spin = tkinter.Spinbox(root, textvariable=key_length, width=4, from_=1, to=100)
spin.grid(row=0, column=1, padx=5, pady=5)
button = tkinter.Button(root, text='OK', command=(lambda r=root, s=spin: print_key_length(r, s)))
button.grid(row=0, column=2, padx=5, pady=5)
button.focus() # Focus to this widget

# Set callback functions
spin.bind("<Return>", lambda event, r=root, s=spin: print_key_length(r, s))
button.bind("<Return>", lambda event, r=root, s=spin: print_key_length(r, s))

# Adjust window position
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
root.update_idletasks() # Necessary to get width and height of the window
ww = root.winfo_width()
wh = root.winfo_height()
root.geometry('+%d+%d' % ((sw/2) - (ww/2), (sh/2) - (wh/2)))

root.mainloop()
