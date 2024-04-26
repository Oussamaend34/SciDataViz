import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from view_table import TableView
from Terminal import Terminal
from Text_editor import Texteditor
from workspace import WorkSpace
from tkinter import filedialog
from tkinter import messagebox
import re
import os

class mainApp():
    def __init__(self) -> None:
        self.root =  tb.Window(themename='superhero', title='SciDataViz')
        self.root.geometry('1200x800')
        self.defaultnotebookFrameDisplayed = True
        self.textareas = []
        self.createWidgets()
        self.bindKeys()

    def createWidgets(self):
        self.TerminalFrame = tb.Frame(self.root)
        self.WorkspaceFrame = tb.Frame(self.root, bootstyle = SECONDARY)
        self.emptyFrame = tb.Frame(self.root, bootstyle = DANGER)
        self.notebook = tb.Notebook(self.root, height=300, width=400)
        self.defaultnotebookFrame = self.creatnotebookFrame()
        self.workspace = WorkSpace(self.WorkspaceFrame)
        self.terminal = Terminal(self.TerminalFrame, self.notebook, self.workspace)
        self.notebook.add(self.defaultnotebookFrame, text="Welcome")
    def bindKeys(self):
        self.root.bind("<Command-q>", self.quit)
        self.root.bind("<Command-y>", self.removeCurrentTab)
        self.root.bind("<Command-n>", lambda e: self.addNewTab())
        self.root.bind("<Command-o>", lambda e: self.addNewTab(filedialog.askopenfilename()))
        self.root.bind("<Command-s>", lambda e: self.save(e))
        self.root.bind("<Shift-Return>", self.run)

    def save(self, event):
        current_tab = self.notebook.select()
        current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
        if any (re.match(r"(.!notebook)?.!frame\d*.!text", child) for child in map(str, current_frame.winfo_children())):
            for child in current_frame.winfo_children():
                if isinstance(child, tb.Text):
                    for texteditor in self.textareas:
                        if texteditor.textarea == child:
                            texteditor.save(event)
                        self.notebook.tab(current_tab, text=os.path.basename(texteditor.file))

    def run(self, event):
        current_tab = self.notebook.select()
        current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
        if any (re.match(r"(.!notebook)?.!frame\d*.!text", child) for child in map(str, current_frame.winfo_children())):
            for child in current_frame.winfo_children():
                if isinstance(child, tb.Text):
                    for texteditor in self.textareas:
                        if texteditor.textarea == child:
                            text = texteditor.selectedTedxt
                            if text:
                                self.terminal.removeCommand()
                                self.terminal.terminal.insert("end", f"{text}\n")
                                commands = text.splitlines()
                                # self.terminal.run(text)
                                for command in commands:
                                    self.terminal.run(command)
                                self.terminal.printbasename()
        return "break"

    def addNewTable(self, table: TableView):
        currentab = self.notebook.select()
        if currentab == self.defaultnotebookFrame:
            self.notebook.forget(currentab)
        self.notebook.add(table.frame, text=table.name)
    def addNewTab(self, file = None):
        current_tab = self.notebook.select()
        current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
        if any (re.match(r".!frame\d+.!label", child ) for child in map(str, current_frame.winfo_children())):
            self.notebook.forget(current_tab)
        new_tab = tb.Frame(self.notebook)
        texteditor = Texteditor(new_tab, file)
        self.textareas.append(texteditor)
        if file :
            title = os.path.basename(file)
            with open(file, 'r') as file:
                text = file.read()
                texteditor.insert(text)
        else:
            title = "Untitled"
        self.notebook.add(new_tab, text=title)
        self.notebook.select(new_tab)
    def creatnotebookFrame(self):
        notebookFrame = tb.Frame()
        lable = tb.Label(notebookFrame, text="To create a New Tab press Command N", bootstyle="info")
        lable.pack(pady=20)
        lable2 = tb.Label(notebookFrame, text="To remove the current Tab press Command O", bootstyle="info")
        lable2.pack(pady=20)
        return notebookFrame

    def removeCurrentTab(self, event):
        current_tab = self.notebook.select()
        current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
        if any (re.match(r".!frame\d+.!label", child ) for child in map(str, current_frame.winfo_children())):
            return "break"
        if any (re.match(r"(.!notebook)?.!frame\d*.!text", child) for child in map(str, current_frame.winfo_children())):
            response = messagebox.askyesnocancel("Save", "Do you want to save the file before closing?")
            if response == None:
                return "break"
            if response == True:
                for child in current_frame.winfo_children():
                    if isinstance(child, tb.Text):
                        for texteditor in self.textareas:
                            if texteditor.textarea == child:
                                text = texteditor.getAllText()
                                if text:
                                    if texteditor.file:
                                        with open(texteditor.file, 'w') as file:
                                            file.write(text)
                                    else:
                                        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
                                        if file_path:
                                            with open(file_path, 'w') as file:
                                                file.write(text)
                                            texteditor.file = file_path
                                        else:
                                            return "break"
        self.notebook.forget(current_tab)
        current_tab = self.notebook.select()
        if not current_tab:
            self.notebook.add(self.defaultnotebookFrame, text="Welcome Again")
            self.notebook.select(self.defaultnotebookFrame)
        return "break"

    def pack(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1,weight=1)
        self.notebook.grid(row=0, column=1, sticky="nsew")
        self.TerminalFrame.grid(row=1, column=1, sticky="nsew")
        self.emptyFrame.grid(row = 0, column=0, sticky = "news")
        self.WorkspaceFrame.grid(row=1, column=0, sticky="news")

    def mainloop(self):
        self.root.mainloop()
    def quit(self, event):
        self.root.destroy()
        return "break"

if __name__ == "__main__":
    app = mainApp()
    app.pack()
    app.mainloop()
