import ttkbootstrap as tb
import tkinter as tk
from visFrame import *


class VisualizationLab():
    def __init__(self, root,dfs={}, plots= {}) -> None:
        self.root = root
        self.plots = plots
        self.visualizationType = tk.StringVar()
        self.optionFrame = tb.Frame(self.root)
        self.optionFrame.pack(pady=10)
        self.container = tb.Frame(root)
        self.container.pack(fill="both", expand=True)
        self.scroolbar = tb.Scrollbar(self.container, orient="vertical")
        self.canvas = tb.Canvas(self.container, yscrollcommand=self.scroolbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroolbar.config(command=self.canvas.yview)
        self.scroolbar.pack(side="right", fill="y")
        self.visTypeCombobox = tb.Combobox(self.optionFrame, values=["Histogram","Line Plot", "Scatter Plot", "Bar Plot",
                                                        "Box Plot", "Violin Plot", "Pie Plot"], state="readonly", textvariable=self.visualizationType, width=20, bootstyle = PRIMARY)
        self.visTypeCombobox.set("Violin Plot")
        self.dfs:dict = dfs
        self.dataframesCombobox = tb.Combobox(self.optionFrame, values=list(self.dfs.keys()), state="readonly", width=20, bootstyle = PRIMARY)
        if len(self.dfs) > 0:
            self.dataframesCombobox.set(list(self.dfs.keys())[0])
            self.df = self.dfs[self.dataframesCombobox.get()]
        else:
            self.df = pd.DataFrame()
        self.dataframesCombobox.bind("<<ComboboxSelected>>", self.onDataframeSelect)
        self.visTypeCombobox.bind("<<ComboboxSelected>>", self.onComboboxSelect)
        self.visualizationFrame = tb.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.visualizationFrame, anchor="nw")
        self.histplot = HistFrame(self.visualizationFrame, self.df, self.plots)
        self.lineplot = LineplotFrame(self.visualizationFrame, self.df, self.plots)
        self.scatterplot = ScatterplotFrame(self.visualizationFrame, self.df, self.plots)
        self.barplot = BarplotFrame(self.visualizationFrame, self.df, self.plots)
        self.boxplot = BoxplotFrame(self.visualizationFrame, self.df, self.plots)
        self.violinplot = ViolinplotFrame(self.visualizationFrame, self.df, self.plots)
        self.pieplot = PieplotFrame(self.visualizationFrame, self.df, self.plots, self.dfs)
        self.violinplot.pack()
        self.visTypeCombobox.pack(side = tk.LEFT)
        self.dataframesCombobox.pack(side = tk.LEFT)
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_frames(self):
        self.histplot.dfs = self.dfs
        self.lineplot.dfs = self.dfs
        self.scatterplot.dfs = self.dfs
        self.barplot.dfs = self.dfs
        self.boxplot.dfs = self.dfs
        self.violinplot.dfs = self.dfs
    def onComboboxSelect(self, event):
        selected_option = self.visTypeCombobox.get()
        self.histplot.pack_forget()
        self.lineplot.pack_forget()
        self.scatterplot.pack_forget()
        self.barplot.pack_forget()
        self.boxplot.pack_forget()
        self.violinplot.pack_forget()
        self.pieplot.pack_forget()
        if selected_option == "Histogram":
            self.histplot.set_df(self.df)
            self.histplot.reset()
            self.histplot.pack()
        elif selected_option == "Line Plot":
            self.lineplot.set_df(self.df)
            self.lineplot.reset()
            self.lineplot.pack()
        elif selected_option == "Scatter Plot":
            self.scatterplot.set_df(self.df)
            self.scatterplot.reset()
            self.scatterplot.pack()
        elif selected_option == "Bar Plot":
            self.barplot.set_df(self.df)
            self.barplot.reset()
            self.barplot.pack()
        elif selected_option == "Box Plot":
            self.boxplot.set_df(self.df)
            self.boxplot.reset()
            self.boxplot.pack()
        elif selected_option == "Violin Plot":
            self.violinplot.set_df(self.df)
            self.violinplot.reset()
            self.violinplot.pack()
        elif selected_option=="Pie Plot":
            self.pieplot.set_df(self.df)
            self.pieplot.reset()
            self.pieplot.pack()

    def onDataframeSelect(self, event):
        selected_df = self.dataframesCombobox.get()
        self.df = self.dfs[selected_df]
        self.onComboboxSelect(event)

if __name__ == "__main__":
    root = tb.Window(themename='superhero', title='SciDataViz')
    root.geometry('400x500')
    iris = pd.read_csv("iris.csv")
    fromage = pd.read_csv("fromage.txt")
    dfs = {"iris": iris, "fromage": fromage}
    app = VisualizationLab(root, dfs=dfs)
    root.mainloop()