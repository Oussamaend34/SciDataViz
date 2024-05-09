import ttkbootstrap as tb
import tkinter as tk
from tkinter import filedialog
import os

class Texteditor():
    def __init__(self, root, file = None) -> None:
        self.root = root
        self.textarea = tb.Text(root)
        self.scrollbar = tb.Scrollbar(root, orient=tk.VERTICAL, bootstyle = 'primary-round')
        self.scrollbar.config(command=self.textarea.yview)
        self.textarea.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.textarea.pack(fill="both", expand=True)
        self.file = file
        self.selectedTedxt = None
        self.textarea.bind("<Shift-Return>", self.run)

    def run(self, event):
        self.selectedTedxt = None
        text = self.getSelectedText()
        if text:
            self.selectedTedxt = text
            selected_first = self.textarea.index(tk.SEL_FIRST)
            selected_last = self.textarea.index(tk.SEL_LAST)
            self.textarea.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.textarea.insert(selected_first, text)

    def insert(self, text):
        self.textarea.insert(tk.END, text)
        self.textarea.see(tk.END)
    def getAllText(self):
        return self.textarea.get("1.0", tk.END)
    def getSelectedText(self):
        return self.textarea.get(tk.SEL_FIRST, tk.SEL_LAST)
    def save(self, event):
        if self.file:
            with open(self.file, 'w') as file:
                text = self.getAllText()
                file.write(text)
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                with open(file_path, 'w') as file:
                    text = self.getAllText()
                    file.write(text)
                self.file = file_path
    def saveAs(self, event):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                text = self.getAllText()
                file.write(text)
            self.file = file_path
if __name__ == "__main__":
    root = tb.Window(title='SciDataViz Terminal', themename='superhero')
    root.geometry('580x250')
    texteditor = Texteditor(root)
    root.mainloop()


