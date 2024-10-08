#
# Mode setting dialog for "Null-preserving XOR" plugin
#
# Copyright (c) 2022, Nobutaka Mantani
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
import dialog_base

class NullPreservingXORDialog(dialog_base.DialogBase):
    def __init__(self, **kwargs):
        super().__init__(title=kwargs["title"])

        self.label_key_type = tkinter.Label(self.root, text="XOR key type:")
        self.label_key_type.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.combo_key_type = tkinter.ttk.Combobox(self.root, width=5, state="readonly")
        self.combo_key_type["values"] = ("Text", "Hex")
        self.combo_key_type.current(1)
        self.combo_key_type.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.label_key = tkinter.Label(self.root, text="XOR key:")
        self.label_key.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.key = tkinter.StringVar()
        self.key.trace("w", lambda *_: self.entry_key_changed())
        self.entry_key = tkinter.Entry(textvariable=self.key, width=32)
        self.entry_key.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.entry_key.focus() # Focus to this widget

        self.label_use_next_xor_key_byte = tkinter.Label(self.root, text="Use next XOR key byte when skipping\nXOR operation (for multibyte XOR key):", justify="left")
        self.label_use_next_xor_key_byte.grid(row=1, column=0, padx=5, pady=5, sticky="w", columnspan=3)
        self.bool_use_next_xor_key_byte = tkinter.BooleanVar()
        self.bool_use_next_xor_key_byte.set(True)
        self.check_use_next_xor_key_byte = tkinter.Checkbutton(self.root, variable=self.bool_use_next_xor_key_byte, text="", onvalue=True, offvalue=False, command=(lambda: None))
        self.check_use_next_xor_key_byte.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.button = tkinter.Button(self.root, text="OK", command=(lambda: self.process()))
        self.button.grid(row=2, column=0, padx=5, pady=5, columnspan=4)

        # Set callback functions
        self.combo_key_type.bind('<<ComboboxSelected>>', lambda event: self.entry_key_changed())

        for x in (self.combo_key_type, self.entry_key, self.check_use_next_xor_key_byte, self.button):
            x.bind("<Return>", lambda event: self.process())

    def process(self):
        if self.combo_key_type.get() == "Hex":
            key = self.entry_key.get()
            next = self.bool_use_next_xor_key_byte.get()
            if re.match("^([0-9A-Fa-f]{2})+$", key):
                print(f"{key}\t{next}")
                self.root.quit()
            else:
                tkinter.messagebox.showerror("Error:", message="Key is not in hex format.")
                return
        else:
            key = binascii.b2a_hex(self.entry_key.get().encode())
            next = self.bool_use_next_xor_key_byte.get()
            print(f"{key.decode()}\t{next}")
            self.root.quit()

    def entry_key_changed(self):
        if self.combo_key_type.get() == "Hex":
            self.key.set(re.sub("[^0-9A-Fa-f]", "", self.key.get()))

if __name__ == "__main__":
    dialog = NullPreservingXORDialog(title="Null-preserving XOR")
    dialog.show()
