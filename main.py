import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from view_table import TableView
from Terminal import Terminal
from Text_editor import Texteditor
from workspace import WorkSpace
from VisualizationLab import VisualizationLab
from suite import DataFrame
from suite import DashBordFrame
from tkinter import filedialog
from tkinter import messagebox
import re
import os


class mainApp():
    def __init__(self) -> None:
        self.root =  tb.Window(themename='superhero', title='SciDataViz')
        self.root.geometry('1400x800')
        self.defaultnotebookFrameDisplayed = True
        self.dfs = {}
        self.textareas = []
        self.titles = []
        self.plots ={}
        self.remove_files("plots")
        self.createWidgets()
        self.bindKeys()

    def createWidgets(self):
        self.TerminalFrame = tb.Frame(self.root)
        self.WorkspaceFrame = tb.Frame(self.root, bootstyle = SECONDARY)
        self.DashboardGenerator = tb.Notebook(self.root, height=300, width=400)
        self.VisualationFrame = tb.Frame(self.DashboardGenerator)
        self.visLab = VisualizationLab(self.VisualationFrame, self.dfs, self.plots)
        self.Dashboard = DashBordFrame(self.DashboardGenerator, self.plots)
        self.Dashboard.pack()
        self.EditingFrame = DataFrame(self.DashboardGenerator, self.dfs)
        self.DashboardGenerator.add(self.EditingFrame.Dwidget, text="Editing Lab")
        self.DashboardGenerator.add(self.VisualationFrame, text="Visualization Lab")
        self.DashboardGenerator.add(self.Dashboard.Dashbordwidget, text = "Dashboard")
        self.DashboardGenerator.bind("<<NotebookTabChanged>>", self.on_tab_change)
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
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
    def save(self, event):
        current_tab = self.notebook.select()
        current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
        if any (re.match(r"(.!notebook\d*)?.!frame\d*.!text", child) for child in map(str, current_frame.winfo_children())):
            for child in current_frame.winfo_children():
                if isinstance(child, tb.Text):
                    for texteditor in self.textareas:
                        if texteditor.textarea == child:
                            texteditor.save(event)
                            if texteditor.file:
                                self.notebook.tab(current_tab, text=os.path.basename(texteditor.file))

    def run(self, event):
        current_tab = self.notebook.select()
        current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
        if any (re.match(r"(.!notebook\d*)?.!frame\d*.!text", child) for child in map(str, current_frame.winfo_children())):
            for child in current_frame.winfo_children():
                if isinstance(child, tb.Text):
                    for texteditor in self.textareas:
                        if texteditor.textarea == child:
                            text = texteditor.selectedTedxt
                            if text:
                                self.terminal.removeCommand()
                                self.terminal.terminal.insert("end", f"{text}\n")
                                commands = text.splitlines()
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
    
    def on_tab_change(self, event):
        self.visLab.dfs = self.dfs
        self.visLab.update_frames()
        self.visLab.dataframesCombobox['values'] = list(self.dfs.keys())
        if len(self.dfs) > 0:
            self.visLab.dataframesCombobox.set(list(self.dfs.keys())[0])
            self.visLab.df = self.dfs[self.visLab.dataframesCombobox.get()]
            self.visLab.onDataframeSelect(event)
        if len(self.plots)>0:
            self.Dashboard.show()
    def removeCurrentTab(self, event):
        current_tab = self.notebook.select()
        current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
        if any (re.match(r".!frame\d+.!label", child ) for child in map(str, current_frame.winfo_children())):
            return "break"
        if any (re.match(r"(.!notebook\d*)?.!frame\d*.!text", child) for child in map(str, current_frame.winfo_children())):
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
                                            self.textareas.remove(texteditor)
                                        else:
                                            self.textareas.remove(texteditor)
                                            return "break"
                                break
        self.notebook.forget(current_tab)
        current_tab = self.notebook.select()
        if not current_tab:
            self.notebook.add(self.defaultnotebookFrame, text="Welcome Again")
            self.notebook.select(self.defaultnotebookFrame)
        return "break"

    def remove_files(self,directory):
        try:
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)
        except FileNotFoundError:
            os.mkdir("plots")


    def on_exit(self):
        current_tab = self.notebook.select()
        while current_tab:
            current_frame:tk.Frame = self.notebook.nametowidget(current_tab)
            if any (re.match(r"(.!notebook\d*)?.!frame\d*.!text", child) for child in map(str, current_frame.winfo_children())):
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
                                    break
            self.notebook.forget(current_tab)
            current_tab = self.notebook.select()
        self.root.destroy()


    def pack(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1,weight=1)
        self.notebook.grid(row=0, column=1, sticky="nsew")
        self.TerminalFrame.grid(row=1, column=1, sticky="nsew")
        self.DashboardGenerator.grid(row=0, column=0, sticky="news")
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
