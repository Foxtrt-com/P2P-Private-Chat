# /modules/gui.py
"""
Tkinter gui class
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import sv_ttk


class GUI(tk.Tk):
    def __init__(self, parent, config):
        super().__init__()

        self.config = config

        if self.config.theme == "Light":
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")

        self.parent = parent
        self.title('P2P Private Chat')
        self.geometry('800x600')
        self.minsize(800, 600)

        # listbox+scrollbar for peers
        # listbox+scrollbar for messages
        # input and button to send

        self.frame = ttk.Frame(self)
        self.frame.pack(anchor=N, expand=1, fill=BOTH)

        self.peer_scroll = ttk.Scrollbar(self.frame)
        self.peer_scroll.grid(column=3, row=0, rowspan=6, sticky=NSEW)

        self.peer_list = tk.Listbox(self.frame, yscrollcommand=self.peer_scroll.set)
        self.peer_list.grid(column=0, row=0, columnspan=3, rowspan=6, sticky=NSEW)

        self.peer_scroll.config(command=self.peer_list.yview)

        self.message_scroll = ttk.Scrollbar(self.frame)
        self.message_scroll.grid(column=13, row=0, rowspan=5, sticky=NSEW)

        self.message_list = tk.Listbox(self.frame, yscrollcommand=self.message_scroll.set)
        self.message_list.grid(column=4, row=0, columnspan=9, rowspan=5, sticky=NSEW)

        self.message_scroll.config(command=self.message_list.yview)

        self.entry = ttk.Entry(self.frame)
        self.entry.grid(column=4, row=5, columnspan=7, sticky=EW)

        self.button = ttk.Button(self.frame, text="Send", command=self.send_msg)
        self.button.grid(column=11, row=5, columnspan=3, sticky=EW)

        for i in range(14):
            self.frame.columnconfigure(i, weight=1)
        for i in range(6):
            self.frame.rowconfigure(i, weight=1)

    def send_msg(self):
        message = self.entry.get()
        self.parent.send(message)
        self.message_list.insert(END, f"{self.config.display_name}: {message}")
        self.entry.delete(first=0, last=END)

