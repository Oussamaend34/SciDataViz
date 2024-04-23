import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk
import pandas as pd


class TableView():
    def __init__(self, root, dataframe, name = "Untiteled") -> None:
        self.name = name
        self.dframe = dataframe
        self.root = root
        self.frame = tk.Frame(self.root)
        self.createTable()
        # Bind the <Configure> event to the resize event handler
        self.frame.bind("<Configure>", self.resize_event)
        
    def createTable(self):
        # Initial padding value
        self.padding = 5
        self.tree = tb.Treeview(self.frame, columns=list(self.dframe.columns), show="headings", bootstyle='info', padding=self.padding)
        for col in self.dframe.columns:
            self.tree.heading(col, text=col)
        for index, row in self.dframe.iterrows():
            self.tree.insert("", "end", values=list(row))
        self.vsb = tb.Scrollbar(self.frame, orient="vertical", command=self.tree.yview, bootstyle = 'primary-round')
        self.tree.configure(yscrollcommand=self.vsb.set)
        self.hsb = tb.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview, bootstyle = 'primary-round')
        self.tree.configure(xscrollcommand=self.hsb.set)
        self.vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.hsb.pack(side="bottom", fill="x")

    def resize_event(self, event):
        # Calculate new padding based on the height of the Treeview widget
        new_padding = max(1, self.tree.winfo_height() // 50)
        # Update the padding if it has changed
        if new_padding != self.padding:
            self.padding = new_padding
            self.tree.configure(padding=self.padding)

def close_current_tab(notebook):
    current_tab = notebook.select()
    if current_tab:
        notebook.forget(current_tab)
    return "break"
def add_new_tab(notebook, name = "Untitled"):
    new_tab = tk.Frame(notebook)
    text = tk.Text(new_tab)
    text.pack(fill="both", expand=True)
    notebook.add(new_tab, text=name)
    notebook.select(new_tab)
    
if __name__ == "__main__":
    root = tb.Window(title='SciDataViz Terminal', themename='superhero')
    root.geometry('580x250')

    # Create a custom Notebook with active tab color
    notebook = tb.Notebook(root)  # Change the active tab color to orange

    # Get the tab objects
    iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    fromage = pd.read_csv('fromage.txt', sep='\t')

    # Create TableView instances and add them to the Notebook
    tableIris = TableView(notebook, iris)
    tableFromage = TableView(notebook, fromage)
    notebook.add(tableFromage.frame, text="Fromage")
    notebook.add(tableIris.frame, text="Iris")
    root.bind("<Command-y>", lambda event: close_current_tab(notebook))
    root.bind("<Command-n>", lambda event: add_new_tab(notebook))

    root.mainloop()
