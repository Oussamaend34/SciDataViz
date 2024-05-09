import tkinter as tk
from tkinter import filedialog,ttk,simpledialog,Scrollbar
from ttkbootstrap import Style
import ttkbootstrap as tb 
import pandas as pd 
import json
from PIL import Image, ImageTk
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def create_centered_text_image(text, image_width, image_height, background_color='white', text_color='black'):
    fig, ax = plt.subplots(figsize=(image_width / 100, image_height / 100))
    ax.set_facecolor(background_color)
    ax.text(0.5, 0.5, text, ha='center', va='center', fontsize=image_height/2, color=text_color)
    ax.axis('off')
    output_path = "plots/centered_text_image.png"
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    return output_path

def merge_images_to_pdf(image_paths,title):
    images = [Image.open(path) for path in image_paths]
    num_images = len(images)
    max_cols_per_row = int(np.ceil(np.sqrt(num_images)))
    num_rows = (num_images + max_cols_per_row - 1) // max_cols_per_row
    max_width = max(im.width for im in images)
    max_height = max(im.height for im in images)
    final_width = max_width * max_cols_per_row 
    final_height = max_height * num_rows + max_height//2
    new_im = Image.new('RGB', (final_width, final_height), (255, 255, 255))
    title_text =title
    title_image = create_centered_text_image(title_text, max_width * max_cols_per_row, max_height // 2)
    new_im.paste(Image.open(title_image),(0,0))
    for i, im in enumerate(images):
        row = i // max_cols_per_row
        col = i % max_cols_per_row
        x_offset = col * max_width
        y_offset = row * max_height + max_height//2
        new_im.paste(im, (x_offset, y_offset))
    filepath = filedialog.asksaveasfilename(defaultextension=".pdf")
    if filepath:
        output_path = filepath
    else:
        output_path = f"{title_text}.pdf"
    new_im.save(output_path, "PDF", resolution=100.0)


def convert_type(value, dtype):
    if dtype == 'object':
        return str(value)
    elif 'float' in str(dtype):
        return float(value)
    elif 'int' in str(dtype):
        return int(value)
    else:
        return value 
'''
Creating a class for the tab DataFames:
This class will contain two button , the first one for importing files as dataFrames
and the seconde button will leed to another window where the data Frame can be edited
'''

class ScrollableFrame(tb.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.canvas = tb.Canvas(self)
        self.scrollbar = tb.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tb.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.bind("<Enter>", self._bound_to_mousewheel)
        self.bind("<Leave>", self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")



class DataFrame:
    def __init__(self, rootWidget, dfs):
        self.Dwidget = tb.Frame(rootWidget, bootstyle="secondary")
        self.style = Style()
        self.dfs = dfs
        self.filePaths={}
        self.selectedFrame = tb.StringVar()
        self.chose = tb.Combobox(self.Dwidget, textvariable=self.selectedFrame,state="readonly")
        self.chose.pack()
        self.buttonsFrame = tb.Frame(self.Dwidget, bootstyle="secondary")
        self.buttonsFrame.pack(padx=5,pady=5)
        self.importButton = tb.Button(self.buttonsFrame, text="Import DataFrame", command=self.importDataFrame,width=100,style="info")
        self.importButton.pack(padx=5,pady=5)
        self.editButton = tb.Button(self.buttonsFrame, text="Edit Frame", command=self.editDataFrame, width=100,style="warning")
        self.editButton.pack(padx=5,pady=5)
        self.exportButton = tb.Button(self.buttonsFrame, text="Export DataFrame", command=self.export, width=100,style="success")
        self.exportButton.pack(padx=5,pady=5)
        self.retrieveButton = tb.Button(self.buttonsFrame, text="Remove DataFrame",command=self.removeDataFrame,width=100,style="danger")
        self.retrieveButton.pack(padx=5,pady=5)
        self.buttonsFrame.grid_columnconfigure(0, weight=1)
        self.buttonsFrame.grid_columnconfigure(1, weight=1)
        self.showDataFrames = tb.Treeview(self.Dwidget,columns=["Data_Frame Name","Source File",""], style="primary.Treeview",show="headings")
        self.showDataFrames.pack(padx=5,pady=5,fill="both",expand=True)
        for element in ["Data_Frame Name","Source File",""]:
            self.showDataFrames.heading(element,text=element)
        self.refreshShowingTree()
        verScrollBar = tb.Scrollbar(self.showDataFrames, command=self.showDataFrames.yview)
        verScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.showDataFrames.config(yscrollcommand=verScrollBar.set)
        horsScrollBar = tb.Scrollbar(self.showDataFrames, orient=tk.HORIZONTAL, command=self.showDataFrames.xview)
        horsScrollBar.pack(side=tb.BOTTOM, fill=tb.X)
        self.showDataFrames.config(xscrollcommand=horsScrollBar.set)
    
    def removeDataFrame(self):
        self.dataFrameName=None
        self.getDataFrameNameWindow = tb.Toplevel(self.Dwidget)
        self.getDataFrameNameWindow.title("Poping a DataFrame from Dashbord Generator window")
        self.getDataFrameNameWindow.geometry("400x110")
        self.getDataFrameNameWindow.resizable(False,False)
        self.getDataFrameNameLabel = tb.Label(self.getDataFrameNameWindow,text="Are you sure?")
        self.getDataFrameNameLabel.pack(padx=5,pady=5)
        self.buttonsFrame1=tb.Frame(self.getDataFrameNameWindow)
        self.buttonsFrame1.pack(pady=5)
        self.button1 = tb.Button(self.getDataFrameNameWindow,text="Yes",width=20,command=self.popD)
        self.button1.pack(side="left",padx=5,expand=True)
        self.button2 = tb.Button(self.getDataFrameNameWindow,text="No",width=20)
        self.button2.pack(side="right",padx=5,expand=True)
    def popD(self):
        if self.chose.current() != -1:
            print(self.chose.current())
            self.dfs.pop(self.chose.get())
            self.chose.delete(self.chose.current())
            self.selectedFrame=""
            self.refreshShowingTree()
            self.getDataFrameNameWindow.destroy()
        else:
            print("Warning : You did not chose the dataFrame to delete")

    def refreshShowingTree(self):
        if len(self.showDataFrames.get_children())==0:
            for key,value in self.dfs.items():
                values=[key,self.filePaths[key],""]
                self.showDataFrames.insert("", "end", values=values)
        else:
            for item in self.showDataFrames.get_children():
                self.showDataFrames.delete(item)
            for key,value in self.dfs.items():
                values=[key,self.filePaths[key],""]
                self.showDataFrames.insert("", "end", values=values)

    def OpenFile(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.filePaths[self.dataFrameName]=file_path
                    df = pd.read_csv(file_path)
                    self.dfs[self.dataFrameName] = df
                    self.chose["values"] = list(self.dfs.keys())
                    self.chose.set(self.dataFrameName)
                    self.refreshShowingTree()
                elif file_path.endswith('.xlsx'):
                    self.filePaths[self.dataFrameName]=file_path
                    df = pd.read_excel(file_path)
                    self.dfs[self.dataFrameName] = df
                    self.chose["values"] = list(self.dfs.keys())
                    self.chose.set(self.dataFrameName)
                    self.refreshShowingTree()
            except Exception as e:
                print(e)
    def importDataFrame(self):
        self.dataFrameName=None
        self.getDataFrameNameWindow = tb.Toplevel(self.Dwidget)
        self.getDataFrameNameWindow.title("something")
        self.getDataFrameNameWindow.geometry("400x110")
        self.getDataFrameNameWindow.resizable(False,False)
        self.getDataFrameNameLabel = tb.Label(self.getDataFrameNameWindow,text="Donner Le nom que vou voulez pour la data frame")
        self.getDataFrameNameLabel.pack(padx=5,pady=5)
        self.getDataFrameNameEntry = tb.Entry(self.getDataFrameNameWindow,textvariable="")
        self.getDataFrameNameEntry.pack(padx=5,pady=5)
        self.button1 = tb.Button(self.getDataFrameNameWindow,text="Comfirmer",command=self.saveDataFrameName)
        self.button1.pack(padx=5,pady=5)
    def saveDataFrameName(self):
        self.dataFrameName=self.getDataFrameNameEntry.get()
        self.getDataFrameNameWindow.destroy()
        self.OpenFile()
    def editDataFrame(self):
        if self.selectedFrame.get():
            self.df = self.dfs[self.selectedFrame.get()]
            name = self.selectedFrame.get()
            self.widget = tb.Toplevel(self.Dwidget)
            self.widget.title(f"Edit Data {name}")
            self.widget.geometry("600x700")
            self.widget.resizable(False, False)
            self.DataFrame = tb.Treeview(self.widget, columns=self.df.columns.tolist(), style="primary.Treeview",show="headings")
            self.DataFrame.pack(expand=True, fill="both")
            for col in self.df.columns.tolist():
                self.DataFrame.heading(col, text=col)
            for index, row in self.df.iterrows():
                self.DataFrame.insert("", "end", values=row.tolist())
            self.DataFrame.bind("<<TreeviewSelect>>", self.editRow)
            verScrollBar = tb.Scrollbar(self.DataFrame, command=self.DataFrame.yview)
            verScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
            self.DataFrame.config(yscrollcommand=verScrollBar.set)
            horsScrollBar = tb.Scrollbar(self.DataFrame, orient=tk.HORIZONTAL, command=self.DataFrame.xview)
            horsScrollBar.pack(side=tb.BOTTOM, fill=tb.X)
            self.DataFrame.config(xscrollcommand=horsScrollBar.set)
            self.buttonFrame = tb.Frame(self.widget)
            self.buttonFrame.pack(side="bottom", fill="x")
            cancelButton = tb.Button(self.buttonFrame, text="Cancel", command=self.cancel)
            cancelButton.pack(side="right", expand=True)
            saveButton = tb.Button(self.buttonFrame, text="Save Changes", command=self.save)
            saveButton.pack(side="left", expand=True)
            self.selectedRow = None
            self.EditRowwidget = None
            self.entryList = None

    def cancel(self):
        self.dfs[self.selectedFrame.get()] = self.df
        self.widget.destroy()

    def editRow(self, event):
        if self.DataFrame.focus():
            self.selectedRow = self.DataFrame.focus()
            values = self.DataFrame.item(self.selectedRow, "values")
            self.EditRowwidget = tk.Tk()
            self.EditRowwidget.title("Edit Row")
            self.EditRowwidget.geometry("300x400")
            scrollable_frame = ScrollableFrame(self.EditRowwidget)
            scrollable_frame.pack(fill="both", expand=True)
            self.entryList = []
            for i, value in enumerate(values):
                label = tb.Label(scrollable_frame.scrollable_frame, text=f"{self.DataFrame.heading(i)['text']}:")
                label.grid(row=i, column=0, sticky="nsew", padx=5, pady=5)
                entry = tb.Entry(scrollable_frame.scrollable_frame,width=100)
                entry.insert(0, value)
                entry.grid(row=i, column=1,sticky="nsew", padx=5, pady=5)
                self.entryList.append(entry)
            frame = tb.Frame(self.EditRowwidget)
            frame.pack(fill="x", side="bottom")
            saveButton = tb.Button(frame, text="Save", command=self.saveRow)
            saveButton.pack(fill="x", padx=5, pady=5)

    def saveRow(self):
        new_values = [entry.get() for entry in self.entryList]
        self.DataFrame.item(self.selectedRow, values=new_values)
        self.EditRowwidget.destroy()

    def save(self):
        self.modified = pd.DataFrame(self.dfs[self.selectedFrame.get()])
        df = self.dfs[self.selectedFrame.get()]
        columns= df.dtypes
        rows = self.DataFrame.get_children()
        for i,row in enumerate(rows):
            values = list(self.DataFrame.item(row, "values"))
            new_values = []
            for value ,col in zip(values,columns):
                new_values.append(convert_type(value, col))
            self.modified.loc[i] = new_values
        self.dfs[self.selectedFrame.get()] = self.modified


    def export(self):
        def export_to_csv():
            df = self.dfs[self.selectedFrame.get()]
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                df.to_csv(file_path, index=False)
            widget.destroy()

        def export_to_excel():
            df = self.dfs[self.selectedFrame.get()]
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                df.to_excel(file_path, index=False)
            widget.destroy()

        widget = tb.Toplevel(self.Dwidget)
        widget.title("Export Window")
        widget.geometry("400x100")
        widget.resizable(False,False)
        csv_button = tb.Button(widget, text="Exporter vers CSV", command=export_to_csv,width=50)
        csv_button.pack(pady=5)
        excel_button = tb.Button(widget, text="Exporter vers Excel", command=export_to_excel,width=50)
        excel_button.pack(pady=5)
        

        

        
        
class VisualisationFrame:
    def __init__(self,rootWidget):
        self.widget=tb.Frame(rootWidget,bootstyle="secondary")

class DashBordFrame:
    def __init__(self,rootWidget, plots):
        self.Dashbordwidget=tb.Frame(rootWidget,bootstyle="secondary")
        self.style=Style()
        self.plots = plots
        #TreeView of the vis
        self.visTreeView = tb.Treeview(self.Dashbordwidget,columns=["index","Data_Frame_Name","Plot_Type","X_Label","Y_Label","path"], style="primary.Treeview",show="headings")
        for element in ["index","Data_Frame_Name","Plot_Type","X_Label","Y_Label","path"]:
            self.visTreeView.heading(element,text=element)
        self.show()
        #Treeview scrolbars
        verScrollBar = tb.Scrollbar(self.visTreeView, command=self.visTreeView.yview,style="dark-round")
        verScrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.visTreeView.config(yscrollcommand=verScrollBar.set)
        horsScrollBar = tb.Scrollbar(self.visTreeView, orient=tk.HORIZONTAL, command=self.visTreeView.xview,style="dark-round")
        horsScrollBar.pack(side=tb.BOTTOM, fill=tb.X)
        self.visTreeView.config(xscrollcommand=horsScrollBar.set)
        #Buttons Frame
        self.buttonsFrame = tb.Frame(self.Dashbordwidget,style="primary")
        self.createButon = tb.Button(self.buttonsFrame,text="Create Dashbord",bootstyle="success",command=self.createDash)
        self.deleteVisButon = tb.Button(self.buttonsFrame,text="Delete a Visualisation",bootstyle="danger",command=self.deleteVis)
        self.grid()
    def grid(self):
        self.createButon.grid(row=0,column=1,padx=5,pady=5,sticky="nsew")
        self.deleteVisButon.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")
    
    def pack(self):
        self.visTreeView.pack(fill="both",expand=True)
        self.buttonsFrame.pack(fill="x",side="bottom")

    def show(self):
        if len(self.visTreeView.get_children())==0:
            for key,value in self.plots.items():
                self.visTreeView.insert("", "end", values=value)
        else:
            for item in self.visTreeView.get_children():
                self.visTreeView.delete(item)
            
            for key,value in self.plots.items():
                self.visTreeView.insert("", "end", values=value)

            for col in self.visTreeView["columns"]:
                max_content_width = max([len(str(self.visTreeView.set(item, col))) for item in self.visTreeView.get_children()])
                heading_width = len(self.visTreeView.heading(col)["text"])
                max_width = max(max_content_width, heading_width)
                self.visTreeView.column(col, width=max_width * 10)
    
    def createDash(self):
        
        self.vispaths=[]
        for key,value in self.plots.items():
            self.vispaths.append(self.plots[key][5])
        self.entryValue=None
        self.getDashbordTitle()
    def getDashbordTitle(self):
        self.window = tb.Toplevel(self.Dashbordwidget)
        self.window.title("Dashbord")
        self.frame=tb.Frame(self.window)
        self.frame.pack(fill="both",expand=True)
        self.dashbordTitleLabel = tb.Label(self.frame,text="Give the title of this Dashbord")
        self.dashbordTitleLabel.pack()
        self.dashbordTitleEntry = tb.Entry(self.frame)
        self.dashbordTitleEntry.pack()
        button = tb.Button(self.frame,text="confirm",command=self.getEntryValue)
        button.pack()
        self.window.mainloop()
    def getEntryValue(self):
        self.entryValue = self.dashbordTitleEntry.get()
        merge_images_to_pdf(self.vispaths,self.entryValue)
        self.window.destroy()

        
    def deleteVis(self):
        if self.visTreeView.focus():
            needed = int(self.visTreeView.item(self.visTreeView.focus(),"values")[0])

            key_list = [key for key, value in self.plots.items() if value[0] == int(needed)]
            self.plots.pop(key_list[0])
            self.temporaire={}
            for i, (key, value) in enumerate(self.plots.items(), 1):
                value[0] = i
                self.temporaire[f"{i}"]=value
            self.plots = self.temporaire
            self.show()
class zone1:
    def __init__(self,root):
        self.root=root
        #fixing size of the principal widget
        self.root.geometry("400x400")
        self.root.resizable(False,False)
        self.style= Style()
        self.style.theme_use('flatly')
        #creating a notebook to hold other widgets
        self.notebook = tb.Notebook(root,bootstyle="primary")
        #creating a Frame for importing and showing DataFrames
        self.DataFrames = DataFrame(self.notebook)
        self.notebook.add(self.DataFrames.Dwidget,text="DataFrames")
        #Creating a Frame for creating visualisations ...
        self.Visualisations = VisualisationFrame(self.notebook)
        self.notebook.add(self.Visualisations.widget,text="Visualisations")
        #Creating a Frame for creating Dashbords ...
        self.DashBord = DashBordFrame(self.notebook)
        self.notebook.add(self.DashBord.Dashbordwidget,text="DashBord")
        self.DashBord.pack()
        self.notebook.pack(expand=True, fill="both")



if __name__ == "__main__":
    root=tk.Tk()
    app=zone1(root)
    root.mainloop()