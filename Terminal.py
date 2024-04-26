import ttkbootstrap as tb
import tkinter as tk
from parser import SciDataVizParser
from lexer import SciDataVizLexer
from error import Error
from view_table import TableView
import pandas as pd

class Terminal():
    def __init__(self, root, notebook, workspace) -> None:
        self.terminal = tk.Text(root)
        self.notebook = notebook
        self.workspace = workspace
        self.stack = []
        self.stackindex = 0
        self.lexer = SciDataVizLexer()
        self.parser = SciDataVizParser(self.terminal, self.notebook, self.workspace)
        self.terminal.tag_config("error", foreground="#e85651")
        self.TerminalScrollbarY =tb.Scrollbar(root,command=self.terminal.yview, orient=tk.VERTICAL, bootstyle = 'primary-round')
        self.TerminalScrollbarY.config(command=self.terminal.yview)
        self.terminal.config(yscrollcommand=self.TerminalScrollbarY.set)
        self.printbasename()
        self.bindKeys()
        self.TerminalScrollbarY.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal.pack(fill=tk.BOTH, expand=True)

    def printbasename(self):
        self.terminal.insert("end", "SciDataViz>")

    def onReturn(self, event):
        command = self.terminal.get("1.0","end").splitlines()[-1].strip()
        command = command[11:]
        if len(self.stack) == 0:
            self.stack.insert(0,command)
        elif len(self.stack) >=1 and command != self.stack[0]:
            self.stack.insert(0,command)
        self.index = 0
        if command != '':
            result = self.parser.parse(self.lexer.tokenize(command))
            if not isinstance(result,type(None)):
                self.terminal.insert("end",f"\n{result}")
            if isinstance(result, Error):

                self.terminal.tag_add("error", "end-1l", "end-1c")
        if command != 'clear':
            self.terminal.insert("end", "\n")
        self.printbasename()
        self.terminal.mark_set("insert", 'end')
        self.terminal.see("end")
        return "break"


    def removeCommand(self):
        end_index = self.terminal.index("end-1c")
        last_line = end_index.split(".")[0]
        start_end_line = f"{last_line}.11"
        end_end_line = f"{last_line}.end"
        self.terminal.delete(start_end_line, end_end_line)
    def run(self, command):
        if len(self.stack) == 0:
            self.stack.insert(0,command)
        elif len(self.stack) >=1 and command != self.stack[0]:
            self.stack.insert(0,command)
        self.index = 0
        if command != '':
            result = self.parser.parse(self.lexer.tokenize(command))
            if not isinstance(result,type(None)):
                self.terminal.insert("end",f"{result}\n")
        
        self.terminal.mark_set("insert", 'end')
        self.terminal.see("end")
    def onBackspace(self,event):
        end_index = self.terminal.index("end-1c")
        last_line = end_index.split(".")[0]
        start_end_line = f"{last_line}.0"
        end_end_line = f"insert"
        text = self.terminal.get(start_end_line, end_end_line)
        if text == "SciDataViz>":
            return "break"
        selection = self.terminal.tag_ranges(tk.SEL)
        if selection:
            self.terminal.delete(f"{tk.INSERT}-1c",tk.INSERT)
            return "break"


    def onArrowLeft(self,event):
        end_index = self.terminal.index("end-1c")
        last_line = end_index.split(".")[0]
        start_end_line = f"{last_line}.0"
        end_end_line = f"insert"
        text = self.terminal.get(start_end_line, end_end_line)
        if text == "SciDataViz>":
            return "break"
    def onClick(self,event):
        self.terminal.focus_set()
        return "break"
    def onArrowUp(self,event):
        end_index = self.terminal.index("end-1c")
        last_line = end_index.split(".")[0]
        start_end_line = f"{last_line}.11"
        end_end_line = f"{last_line}.end"
        self.terminal.delete(start_end_line, end_end_line)
        try:
            self.terminal.insert("end",f"{self.stack[self.index]}")
            self.index += 1
        except:
            pass
        return "break"
    def onArrowDown(self, event):
        end_index = self.terminal.index("end-1c")
        last_line = end_index.split(".")[0]
        start_end_line = f"{last_line}.11"
        end_end_line = f"{last_line}.end"
        self.terminal.delete(start_end_line, end_end_line)
        try:
            self.terminal.insert("end",f"{self.stack[self.index-1]}")
            self.index = self.index - 1
        except:
            pass
        return "break"
    def on_button_press(self, event):
        # Store the current cursor position
        self.cursor_position = self.terminal.index(tk.INSERT)
    
    def on_button_release(self, event):
        # Restore the cursor position to the stored position
        if self.cursor_position:
            self.terminal.mark_set(tk.INSERT, self.cursor_position)
    def onCommandC(self, event):
        self.terminal.clipboard_clear()
        self.terminal.clipboard_append(self.terminal.selection_get())
        return "break"
    def onCommandV(self, event):
        self.terminal.insert(tk.INSERT, self.terminal.clipboard_get())
        return "break"
    def printAssign(self, event):
        self.terminal.insert(tk.INSERT, " <- ")
        return "break"
    def bindKeys(self):
        self.terminal.bind("<Return>", self.onReturn)
        self.terminal.bind("<BackSpace>",self.onBackspace)
        self.terminal.bind("<Button-1>", self.onClick)
        self.terminal.bind("<Down>", self.onArrowDown)
        self.terminal.bind("<Up>", self.onArrowUp)
        self.terminal.bind("<Left>", self.onArrowLeft)
        self.terminal.bind('<ButtonPress-1>', self.on_button_press)
        self.terminal.bind('<ButtonRelease-1>', self.on_button_release)
        self.terminal.bind('<Command-Left>', lambda event: 'break')
        self.terminal.bind('<Command-Right>', lambda event: 'break')
        self.terminal.bind('<Command-Up>', lambda event: 'break')
        self.terminal.bind('<Command-Down>', lambda event: 'break')
        self.terminal.bind('<Command-a>', lambda event: 'break')
        self.terminal.bind('<Command-c>', self.onCommandC)
        self.terminal.bind('<Command-v>', self.onCommandV)
        self.terminal.bind('<Command-x>', self.onCommandC)
        self.terminal.bind('<Command-minus>', self.printAssign)

if __name__ == "__main__":
    root = tb.Window(themename='superhero', title='SciDataViz Terminal')
    frame = tb.Frame(root, bootstyle='danger')
    terminal = Terminal(frame)
    terminal.pack()
    frame.pack()
    root.mainloop()