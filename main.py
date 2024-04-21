import ttkbootstrap as tb
import tkinter as tk
from parser import SciDataVizParser
from lexer import SciDataVizLexer


class Terminal():
    def __init__(self, root) -> None:
        self.terminal = tk.Text(root)
        self.scrollbar = tb.Scrollbar(root, orient=tk.VERTICAL, bootstyle = 'danger-round')
        self.scrollbar.config(command=self.terminal.yview)
        self.terminal.config(yscrollcommand=self.scrollbar.set)
        self.stack = []
        self.stackindex = 0
        self.lexer = SciDataVizLexer()
        self.parser = SciDataVizParser(self.terminal)
        self.printbasename()
        self.bindKeys()

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
        if command != 'clear':
            self.terminal.insert("end", "\n")
        self.printbasename()
        self.terminal.mark_set("insert", 'end')
        self.terminal.see("end")
        return "break"
    def onBackspace(self,event):
        end_index = self.terminal.index("end-1c")
        last_line = end_index.split(".")[0]
        start_end_line = f"{last_line}.0"
        end_end_line = f"{last_line}.end"
        text = self.terminal.get(start_end_line, end_end_line)
        if text == "SciDataViz>":
            return "break"
        selection = self.terminal.tag_ranges(tk.SEL)
        if selection:
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
    def bindKeys(self):
        self.terminal.bind("<Return>", self.onReturn)
        self.terminal.bind("<BackSpace>",self.onBackspace)
        self.terminal.bind("<Button-1>", self.onClick)
        self.terminal.bind("<Down>", self.onArrowDown)
        self.terminal.bind("<Up>", self.onArrowUp)
        self.terminal.bind('<ButtonPress-1>', self.on_button_press)
        self.terminal.bind('<ButtonRelease-1>', self.on_button_release)
    def pack(self):
        self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
root = tb.Window(themename='superhero', title='SciDataViz Terminal')
frame = tb.Frame(root, bootstyle='danger')
terminal = Terminal(frame)
terminal.pack()
frame.pack()
root.mainloop()

