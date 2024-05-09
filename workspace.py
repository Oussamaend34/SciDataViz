import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from random import randint, choice
from numpy import ndarray
from pandas import DataFrame
import numpy as np


class WorkSpace():
    def __init__(self, root) -> None:
        self.root:tb.Frame   = root
        self.padding = 5
        self.workspace = tb.Treeview(self.root, columns=["Variable", "Value"], show="headings", bootstyle = SECONDARY, padding=self.padding)
        self.workspace.heading("Variable", text="Variable")
        self.workspace.heading("Value", text="Value")
        self.vsb = tb.Scrollbar(self.root, orient="vertical", command=self.workspace.yview, bootstyle = 'primary-round')
        self.workspace.configure(yscrollcommand=self.vsb.set)
        self.hsb = tb.Scrollbar(self.root, orient="horizontal", command=self.workspace.xview, bootstyle = f"{SECONDARY}-{ROUND}")
        self.workspace.configure(xscrollcommand=self.hsb.set)
        self.vsb.pack(side="right", fill="y")
        self.workspace.pack(fill="both", expand=True)
        self.hsb.pack(side="bottom", fill="x")
        self.root.bind("<Configure>", self.resize_event)
    
    def resize_event(self, event):
        new_padding = max(1, self.workspace.winfo_height() // 50)
        if new_padding!= self.padding:
            self.padding = new_padding
            self.workspace.configure(padding=self.padding)

    def addVariable(self, variable, value):
        return self.workspace.insert("", "end", values=[variable, self.valueToStr(value)])

    def changeValue(self, item_id, new_value):
        current_values = self.workspace.item(item_id, 'values')
        current_values = list(current_values)
        current_values[1] = self.valueToStr(new_value)
        self.workspace.item(item_id, values=current_values)
    
    def valueToStr(self, value:ndarray|DataFrame):
        if isinstance(value, ndarray) and len(str((value))) > 10:
            return f"Array of {value.size} elements."
        elif isinstance(value, DataFrame):
            s = 'DataFrame: '
            for column in value.columns:
                s += str(column) + " "
            return s
        else:
            return str(value)

if __name__ == "__main__":
    variables = ["w", "x", "y", "z"]
    root = tb.Window(themename="superhero")
    root.geometry('580x250')
    frame = tb.Frame(root, bootstyle = 'danger')
    workspace = WorkSpace(frame)
    button = tb.Button(root, bootstyle = 'danger', command=lambda : workspace.addVariable(choice(variables), randint(0,10000)))
    button.pack(fill="both", expand=True)
    frame.pack()
    root.mainloop()
