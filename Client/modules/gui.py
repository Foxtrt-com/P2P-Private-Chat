# /modules/gui.py
"""
Tkinter gui class
"""

import tkinter as tk
from tkinter import *
import sv_ttk


class GUI(tk.Tk):
    def __init__(self, theme):
        super().__init__()

        if theme == "Light":
            sv_ttk.set_theme("light")
        else:
            sv_ttk.set_theme("dark")

        self.title('P2P Private Chat')
        self.geometry('800x600')
        self.minsize(800, 600)

        # listbox+scrollbar for peers
        # listbox+scrollbar for messages
        # input and button to send

        t_frame = Frame(self)
        t_frame.pack(side=TOP, anchor=N, fill=BOTH, expand=1)

        myscroll = Scrollbar(t_frame)
        myscroll.pack(side=RIGHT, fill=Y)

        mylist = Listbox(t_frame, yscrollcommand=myscroll.set)
        for line in range(1, 100):
            mylist.insert(END, "Number " + str(line))
        mylist.pack(side=LEFT, fill=BOTH)

        myscroll.config(command=mylist.yview)

        myscroll = Scrollbar(t_frame)
        myscroll.pack(side=RIGHT, fill=Y)

        mylist = Listbox(t_frame, yscrollcommand=myscroll.set)
        for line in range(1, 100):
            mylist.insert(END, "Number " + str(line))
        mylist.pack(side=LEFT, fill=BOTH)

        myscroll.config(command=mylist.yview)

        b_frame = Frame(self)
        b_frame.pack(side=BOTTOM, anchor=S, fill=BOTH, expand=1)

        user_in = Entry(b_frame)
        user_in.pack(side=LEFT, fill=BOTH)

        btn = Button(b_frame, text="Send")
        btn.pack(side=LEFT, fill=BOTH)
