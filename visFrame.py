import ttkbootstrap as tb
from ttkbootstrap import *
from tkinter.messagebox import showerror, showinfo
import tkinter as tk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt




class PieplotFrame():
    def __init__(self,root, df, plots={}, dfs = {}) -> None:
        self.root:tb.Window = root
        self.df = df
        self.dfs = dfs
        self.plots = plots
        self.optionsFrame = tb.Frame(root)
        self.Title = tb.Label(self.optionsFrame, text = "Title", width=20)
        self.vizTitle = tb.Entry(self.optionsFrame, width=20)
        self.sizeslable = tb.Label(self.optionsFrame, text = "Sizes", width=20)
        self.sizes = tb.Combobox(self.optionsFrame, values=list(self.df.columns), bootstyle="primary", state="readonly", width=20)
        self.labelsLabel = tb.Label(self.optionsFrame, text = "Labels", width=20)
        self.labels = tb.Combobox(self.optionsFrame, values=list(self.df.columns), bootstyle="primary", state="readonly", width=20)
        self.pcdistanceLabel = tb.Label(self.optionsFrame, text = "Pc Distance", width=20)
        self.pcdistance = tb.Entry(self.optionsFrame, width=20)
        self.pcdistance.insert(0, 0.6)
        self.labeldistanceLabel = tb.Label(self.optionsFrame, text = "Label Distance", width=20)
        self.labeldistance = tb.Entry(self.optionsFrame, width=20)
        self.labeldistance.insert(0, 1.1)
        self.autopct = tb.IntVar()
        self.autopctCheck = tb.Checkbutton(self.optionsFrame, text="Auto Percent", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.autopct)
        self.autopct.set(False)
        self.shadow = tb.IntVar()
        self.shadowCheck = tb.Checkbutton(self.optionsFrame, text="Shadow", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.shadow)
        self.shadow.set(False)
        self.resetButton = tb.Button(root, text="Reset", bootstyle="danger", width=10)
        self.Vizbutton = tb.Button(root, text="Visualize", bootstyle="primary", width=15)
        self.AddButton = tb.Button(root, text="Add To Dashboard", bootstyle="success", width=20)
        self.resetButton.config(command=self.reset)
        self.Vizbutton.config(command=self.Visualize)
        self.AddButton.config(command=self.AddToDashboard)
        self.grid()
    def grid(self):
        self.optionsFrame.grid_rowconfigure(0, weight=1)
        self.optionsFrame.grid_rowconfigure(1, weight=1)
        self.optionsFrame.grid_rowconfigure(2, weight=1)
        self.optionsFrame.grid_rowconfigure(4, weight=1)
        self.optionsFrame.grid_columnconfigure(0, weight=1)
        self.optionsFrame.grid_columnconfigure(1, weight=1)
        self.Title.grid(row=0, column=0, columnspan=2)
        self.vizTitle.grid(row=1, column=0, columnspan=2)
        self.sizeslable.grid(row=2, column=0)
        self.sizes.grid(row=3, column=0)
        self.labelsLabel.grid(row=2, column=1)
        self.labels.grid(row=3, column=1)
        self.pcdistanceLabel.grid(row=4, column=0)
        self.pcdistance.grid(row=5, column=0)
        self.labeldistanceLabel.grid(row=4, column=1)
        self.labeldistance.grid(row=5, column=1)
        self.autopctCheck.grid(row=6, column=0, padx=5, pady=10)
        self.shadowCheck.grid(row=6, column=1, padx=5, pady=10)
    def pack(self):
        self.optionsFrame.pack(expand=True, fill="both")
        self.resetButton.pack(side = LEFT, padx=5, pady=10, expand=True)
        self.AddButton.pack(side=LEFT, padx=5, pady=10, expand=True)
        self.Vizbutton.pack(side = LEFT, padx=5, pady=10, expand=True, fill="both")
    def pack_forget(self):
        self.optionsFrame.pack_forget()
        self.resetButton.pack_forget()
        self.AddButton.pack_forget()
        self.Vizbutton.pack_forget()
    def set_df(self, df):
        self.df:pd.DataFrame = df
        self.sizes.config(values=list(self.df.columns))
        self.labels.config(values=list(self.df.columns))
    def reset(self):
        self.vizTitle.delete(0, END)
        self.sizes.set("")
        self.labels.set("")
        self.pcdistance.delete(0, END)
        self.labeldistance.delete(0, END)
        self.autopct.set(False)
        self.shadow.set(False)
        self.pcdistance.insert(0, 0.6)
        self.labeldistance.insert(0, 1.1)
    def Visualize(self):
        plt.clf()
        Title = self.vizTitle.get()
        sizes = self.sizes.get()
        labels = self.labels.get()
        pcdistance = self.pcdistance.get()
        labeldistance = self.labeldistance.get()
        autopct = self.autopct.get()
        shadow = self.shadow.get()
        try:
            labeldistance = float(labeldistance)
        except:
            showerror("Error", "Label Distance must be a float")
            return
        try:
            pcdistance = float(pcdistance)
        except:
            showerror("Error", "Pc Distance must be a float")
            return
        if autopct:
            autopct = "%1.1f%%"
        else:
            autopct = None
        if sizes == "":
            showerror("Error", "Sizes is required")
            return
        if labels == "":
            showerror("Error", "Labels is required")
            return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            plt.pie(self.df[sizes], labels=self.df[labels], autopct=autopct, shadow=shadow, pctdistance=float(pcdistance), labeldistance=float(labeldistance))
            if Title:
                plt.title(Title)
            plt.show()
        except Exception as e:
            showerror("Error", "An error occured while visualizing")
    def AddToDashboard(self):
        plt.clf()
        Title = self.vizTitle.get()
        sizes = self.sizes.get()
        labels = self.labels.get()
        pcdistance = self.pcdistance.get()
        labeldistance = self.labeldistance.get()
        autopct = self.autopct.get()
        shadow = self.shadow.get()
        try:
            labeldistance = float(labeldistance)
        except:
            showerror("Error", "Label Distance must be a float")
            return
        try:
            pcdistance = float(pcdistance)
        except:
            showerror("Error", "Pc Distance must be a float")
            return
        if autopct:
            autopct = "%1.1f%%"
        else:
            autopct = None
        if sizes == "":
            showerror("Error", "Sizes is required")
            return
        if labels == "":
            showerror("Error", "Labels is required")
            return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            plt.pie(self.df[sizes], labels=self.df[labels], autopct=autopct, shadow=shadow, pctdistance=float(pcdistance), labeldistance=float(labeldistance))
            if Title:
                plt.title(Title)
            path = f"plots/Pieplot_{Title}_{sizes}_{labels}_{pcdistance}_{labeldistance}_{autopct}_{shadow}.png"
            plt.savefig(path)
            plt.clf()
            plt.close()
            for key, value in self.dfs.items():
                if self.df.equals(value):
                    df = key
            self.plots[f"{len(self.plots)+1}"] = [len(self.plots)+1,df, "Pieplot", sizes, labels, path]
            showinfo("Success", "Plot added to dashboard")
        except Exception as e:
            showerror("Error", "An error occured while adding to dashboard")




class VisulazationFrame():
    def __init__(self, root, df, plots = {}, dfs = {}) -> None:
        self.root:tb.Window = root
        self.df = df
        self.dfs = dfs
        self.plots = plots
        self.optionsFrame = tb.Frame(root)
        self.Title = tb.Label(self.optionsFrame, text = "Title", width=20)
        self.vizTitle = tb.Entry(self.optionsFrame, width=20)
        self.xlabel = tb.Label(self.optionsFrame, text = "X-axis Label", width=20)
        self.vizxLabel = tb.Entry(self.optionsFrame, width=20)
        self.ylabel = tb.Label(self.optionsFrame, text = "Y-axis Label", width=20)
        self.vizyLabel = tb.Entry(self.optionsFrame, width=20)
        self.X = tb.Label(self.optionsFrame, text = "X-axis", width=20)
        self.vizx = tb.Combobox(self.optionsFrame, values=list(self.df.columns), bootstyle="primary", state="readonly", width=20)
        self.Y = tb.Label(self.optionsFrame, text = "Y-axis", width=20)
        self.vizy = tb.Combobox(self.optionsFrame, values=list(self.df.columns), bootstyle="primary", state="readonly", width=20)
        self.Vizbutton = tb.Button(root, text="Visualize", bootstyle="primary", width=15)
        self.resetButton = tb.Button(root, text="Reset", bootstyle="danger", width=10)
        self.AddButton = tb.Button(root, text="Add To Dashboard", bootstyle="success", width=20)

    def set_df(self, df):
        self.df:pd.DataFrame = df
        self.vizx.config(values=list(self.df.columns))
        self.vizy.config(values=list(self.df.columns))
    def grid(self):
        self.optionsFrame.grid_rowconfigure(0, weight=1)
        self.optionsFrame.grid_rowconfigure(1, weight=1)
        self.optionsFrame.grid_rowconfigure(2, weight=1)
        self.optionsFrame.grid_rowconfigure(4, weight=1)
        self.optionsFrame.grid_columnconfigure(0, weight=1)
        self.optionsFrame.grid_columnconfigure(1, weight=1)
        self.Title.grid(row=0, column=0, columnspan=2)
        self.vizTitle.grid(row=1, column=0, columnspan=2)
        self.X.grid(row=2, column=0)
        self.vizx.grid(row=3, column=0)
        self.xlabel.grid(row= 2, column=1)
        self.vizxLabel.grid(row=3,column=1)
        self.Y.grid(row=4, column=0)
        self.vizy.grid(row=5, column=0)
        self.ylabel.grid(row=4, column=1)
        self.vizyLabel.grid(row=5, column=1)
    def pack(self):
        self.optionsFrame.pack(expand=True, fill="both")
        self.resetButton.pack(side = LEFT, padx=5, pady=10, expand=True)
        self.AddButton.pack(side=LEFT, padx=5, pady=10, expand=True)
        self.Vizbutton.pack(side = LEFT, padx=5, pady=10, expand=True, fill="both")
    def pack_forget(self):
        self.optionsFrame.pack_forget()
        self.resetButton.pack_forget()
        self.AddButton.pack_forget()
        self.Vizbutton.pack_forget()

class HistFrame(VisulazationFrame):
    def __init__(self, root, df, plots, dfs= {}) -> None:
        super().__init__(root, df, plots, dfs)
        self.bins = tb.Entry(self.optionsFrame, width=20)
        self.bins.insert(0, "10")
        self.binsLabel = tb.Label(self.optionsFrame, text="Bins", width=20)
        self.histoptionsLabel = tb.Label(self.optionsFrame, text="Hist Options", width=20)
        self.histoptions = tb.Combobox(self.optionsFrame, values = ["bars", "step", "poly"], width=20, state="readonly")
        self.histoptions.set("bars")
        self.histstatLabel = tb.Label(self.optionsFrame, text="Hist Stat", width=20)
        self.histstat = tb.Combobox(self.optionsFrame, values = ["count", "frequency", "density", "probability", "percent"], width=20, state="readonly")
        self.hueLabel = tb.Label(self.optionsFrame, text="Color", width=20)
        self.hue = tb.Combobox(self.optionsFrame, values = [""]+list(self.df.columns), width=20, state="readonly")
        self.histstat.set("count")
        self.kde = tb.IntVar()
        self.kdecheck = tb.Checkbutton(self.optionsFrame, text="Kernel Density", width=20, bootstyle = "round-toggle", offvalue=False, onvalue=True, variable=self.kde)
        self.kde.set(False)
        self.fill = tb.IntVar()
        self.fill_check = tb.Checkbutton(self.optionsFrame, text="Fill", width=20, bootstyle = "round-toggle", offvalue=False, onvalue=True, variable=self.fill)
        self.fill.set(True)
        self.resetButton.config(command=self.reset)
        self.Vizbutton.config(command=self.Visualize)
        self.AddButton.config(command=self.AddToDashboard)
        self.grid()
    def grid(self):
        super().grid()
        self.histstatLabel.grid(row=6, column=0)
        self.histstat.grid(row=7, column=0)
        self.histoptionsLabel.grid(row=6, column=1)
        self.histoptions.grid(row=7, column=1)
        self.binsLabel.grid(row=8, column=0)
        self.bins.grid(row=9, column=0)
        self.hueLabel.grid(row=8, column=1)
        self.hue.grid(row=9, column=1)
        self.kdecheck.grid(row=10, column=0, padx=5, pady=10)
        self.fill_check.grid(row=10, column=1, padx=5, pady=10)
    def set_df(self, df):
        super().set_df(df)
        self.hue.config(values=[""]+list(self.df.columns))

    def reset(self):
        self.vizTitle.delete(0, END)
        self.vizxLabel.delete(0, END)
        self.vizyLabel.delete(0, END)
        self.vizx.set("")
        self.vizy.set("")
        self.histoptions.set("bars")
        self.bins.delete(0, END)
        self.bins.insert(0, "10")
        self.histstat.set("count")
        self.hue.set("")
        self.kde.set(False)
        self.fill.set(True)

    def Visualize(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        ylabel = self.vizyLabel.get()
        xlabel = self.vizxLabel.get()
        hue = self.hue.get()
        fill = self.fill.get()
        try:
            bins = int(self.bins.get())
        except:
            showerror("Error", "Bins must be an integer")
            return
        histoptions = self.histoptions.get()
        histstat = self.histstat.get()
        if hue == "":
            hue = None
        if x == "":
            x = None
        if y == "":
            y = None
        if hue:
            if not (x or y):
                showerror("Error", "X-axis or Y-axis is required when using color")
                return
        kde = self.kde.get()
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.histplot(data=self.df, x=x, y=y, hue=hue, bins=bins, element=histoptions, stat=histstat, kde=kde, fill=fill)
            plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.show()
        except Exception as e:
            showerror("Error", "An error occured while visualizing")
    
    def AddToDashboard(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        ylabel = self.vizyLabel.get()
        xlabel = self.vizxLabel.get()
        hue = self.hue.get()
        fill = self.fill.get()
        try:
            bins = int(self.bins.get())
        except:
            showerror("Error", "Bins must be an integer")
            return
        histoptions = self.histoptions.get()
        histstat = self.histstat.get()
        if hue == "":
            hue = None
        if x == "":
            x = None
        if y == "":
            y = None
        if hue:
            if not (x or y):
                showerror("Error", "X-axis or Y-axis is required when using color")
                return
        kde = self.kde.get()
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.histplot(data=self.df, x=x, y=y, hue=hue, bins=bins, element=histoptions, stat=histstat, kde=kde, fill=fill)
            plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            path = f"plots/Histplot_{Title}_{xlabel}_{ylabel}_{hue}_{bins}_{histoptions}_{histstat}_{kde}_{fill}_{x}_{y}.png"
            plt.savefig(path)
            plt.clf()
            plt.close()
            for key, value in self.dfs.items():
                if self.df.equals(value):
                    df = key
            self.plots[f"{len(self.plots)+1}"] = [len(self.plots)+1, df,"Histplot",x,y, path]
            showinfo("Success", "Plot added to dashboard")
        except Exception as e:
            showerror("Error", "An error occured while adding to dashboard")


class ScatterplotFrame(VisulazationFrame):
    def __init__(self, root, df, plots ={}, dfs = {}) -> None:
        super().__init__(root, df, plots, dfs)
        self.hueLabel = tb.Label(self.optionsFrame, text="Color", width=20)
        self.hue = tb.Combobox(self.optionsFrame, values = [""] + list(self.df.columns), width=20, state="readonly")
        self.hue.set("")
        self.sizeLabel = tb.Label(self.optionsFrame, text="Size", width=20)
        self.size = tb.Combobox(self.optionsFrame, values =  [""] + list(self.df.columns), width=20, state="readonly")
        self.size.set("")
        self.styleLabel = tb.Label(self.optionsFrame, text="Style", width=20)
        self.style = tb.Combobox(self.optionsFrame, values = [""] + list(self.df.columns), width=20, state="readonly")
        self.style.set("")
        self.resetButton.config(command=self.reset)
        self.Vizbutton.config(command=self.Visualize)
        self.AddButton.config(command=self.AddToDashboard)
        self.grid()
        
    def grid(self):
        super().grid()
        self.hueLabel.grid(row=6, column=1)
        self.hue.grid(row=7, column=1)
        self.sizeLabel.grid(row=6, column=0)
        self.size.grid(row=7, column=0)
        self.styleLabel.grid(row=8, column=0)
        self.style.grid(row=9, column=0)

    def reset(self):
        self.vizTitle.delete(0, END)
        self.vizxLabel.delete(0, END)
        self.vizyLabel.delete(0, END)
        self.hue.set("")
        self.size.set("")
        self.style.set("")
        self.vizx.set("")
        self.vizy.set("")

    def set_df(self, df):
        super().set_df(df)
        self.hue.config(values=[""]+list(self.df.columns))
        self.size.config(values=[""]+list(self.df.columns))
        self.style.config(values=[""]+list(self.df.columns))

    def Visualize(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        size = self.size.get()
        style = self.style.get()
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if size == "":
            size = None
        if style == "":
            style = None
        if any([x, y, hue, size, style]):
            if not x:
                showerror("Error", "X-axis is required")
                return
            if not y:
                showerror("Error", "Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.scatterplot(data=self.df, x=x, y=y, hue=hue, size=size, style=style)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.show()
        except Exception as e:
            showerror("Error", "An error occured while visualizing")
    
    def AddToDashboard(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        size = self.size.get()
        style = self.style.get()
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if size == "":
            size = None
        if style == "":
            style = None
        if any([x, y, hue, size, style]):
            if not x:
                showerror("Error", "X-axis is required")
                return
            if not y:
                showerror("Error", "Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.scatterplot(data=self.df, x=x, y=y, hue=hue, size=size, style=style)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            path = f"plots/Scatterplot_{Title}_{xlabel}_{ylabel}_{hue}_{size}_{style}_{x}_{y}.png"
            plt.savefig(path)
            plt.clf()
            plt.close()
            for key, value in self.dfs.items():
                if self.df.equals(value):
                    df = key
            self.plots[f"{len(self.plots)+1}"] = [len(self.plots)+1, df,"Scatterplot",x,y, path]
            showinfo("Success", "Plot added to dashboard")
        except Exception as e:
            showerror("Error", "An error occured while adding to dashboard")


class LineplotFrame(ScatterplotFrame):
    def __init__(self, root, df, plots = {}, dfs = {}) -> None:
        super().__init__(root, df, plots, dfs)
        self.unitsLabel = tb.Label(self.optionsFrame, text="Units", width=20)
        self.units = tb.Combobox(self.optionsFrame, values = [""] + list(self.df.columns), width=20, state="readonly")
        self.units.set("")
        self.errorbar = tb.IntVar()
        self.errorbarCheck = tb.Checkbutton(self.optionsFrame, text="Error Bars", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.errorbar)
        self.errorbar.set(False)
        self.grid_more()
    
    def grid_more(self):
        self.unitsLabel.grid(row=10, column=0)
        self.units.grid(row=11, column=0)
        self.errorbarCheck.grid(row=10, column=1)
    def reset(self):
        self.vizTitle.delete(0, END)
        self.vizxLabel.delete(0, END)
        self.vizyLabel.delete(0, END)
        self.hue.set("")
        self.size.set("")
        self.style.set("")
        self.units.set("")
        self.vizx.set("")
        self.vizy.set("")
        self.errorbar.set(False)
    
    def set_df(self, df):
        super().set_df(df)
        self.units.config(values=[""]+list(self.df.columns))
    
    def Visualize(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        size = self.size.get()
        style = self.style.get()
        units = self.units.get()
        errorbar = self.errorbar.get()
        if not errorbar:
            errorbar = None
        else:
            errorbar = ("ci", 95)
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if size == "":
            size = None
        if style == "":
            style = None
        if units == "":
            units = None
        if any([x, y, hue, size, style, units]):
            if not x:
                showerror("Error", "X-axis is required")
                return
            if not y:
                showerror("Error", "Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.lineplot(data=self.df, x=x, y=y, hue=hue, size=size, style=style, units=units, estimator=None, errorbar=errorbar)
            plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.show()
        except Exception as e:
            showerror("Error", "An error occured while visualizing")
    
    def AddToDashboard(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        size = self.size.get()
        style = self.style.get()
        units = self.units.get()
        errorbar = self.errorbar.get()
        if not errorbar:
            errorbar = None
        else:
            errorbar = ("ci", 95)
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if size == "":
            size = None
        if style == "":
            style = None
        if units == "":
            units = None
        if any([x, y, hue, size, style, units]):
            if not x:
                showerror("Error", "X-axis is required")
                return
            if not y:
                showerror("Error", "Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.lineplot(data=self.df, x=x, y=y, hue=hue, size=size, style=style, units=units, estimator=None, errorbar=errorbar)
            plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            path = f"plots/Lineplot_{Title}_{xlabel}_{ylabel}_{hue}_{size}_{style}_{units}_{x}_{y}.png"
            plt.savefig(path)
            plt.clf()
            plt.close()
            for key, value in self.dfs.items():
                if self.df.equals(value):
                    df = key
            self.plots[f"{len(self.plots)+1}"] = [len(self.plots)+1,df,"Lineplot",x,y, path]
            showinfo("Success", "Plot added to dashboard")
        except Exception as e:
            showerror("Error", "An error occured while adding to dashboard")

class BarplotFrame(VisulazationFrame):
    def __init__(self, root, df, plots = {}, dfs = {}) -> None:
        super().__init__(root, df, plots, dfs)
        self.hueLabel = tb.Label(self.optionsFrame, text="Color", width=20)
        self.hue = tb.Combobox(self.optionsFrame, values = [""] + list(self.df.columns), width=20, state="readonly")
        self.hue.set("")
        self.estimatorLabel = tb.Label(self.optionsFrame, text="Estimator", width=20)
        self.estimator = tb.Combobox(self.optionsFrame, values = ["mean", "median", "sum", "count", "max", "min"], width=20, state="readonly")
        self.estimator.set("mean")
        self.errorbar = tb.IntVar()
        self.errorbarCheck = tb.Checkbutton(self.optionsFrame, text="Error Bars", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.errorbar)
        self.errorbar.set(False)
        self.fill = tb.IntVar()
        self.fillCheck = tb.Checkbutton(self.optionsFrame, text="Fill", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.fill)
        self.fill.set(True)
        self.resetButton.config(command=self.reset)
        self.Vizbutton.config(command=self.Visualize)
        self.AddButton.config(command=self.AddToDashboard)
        self.grid()

    def grid(self):
        super().grid()
        self.hueLabel.grid(row=6, column=1)
        self.hue.grid(row=7, column=1)
        self.estimatorLabel.grid(row=6, column=0)
        self.estimator.grid(row=7, column=0)
        self.errorbarCheck.grid(row=8, column=0)
        self.fillCheck.grid(row=8, column=1)
    def reset(self):
        self.vizTitle.delete(0, END)
        self.vizxLabel.delete(0, END)
        self.vizyLabel.delete(0, END)
        self.hue.set("")
        self.vizx.set("")
        self.vizy.set("")
        self.estimator.set("mean")
        self.errorbar.set(False)
        self.fill.set(True)
    
    def set_df(self, df):
        super().set_df(df)
        self.hue.config(values=[""]+list(self.df.columns))
    def Visualize(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        estimator = self.estimator.get()
        fill = self.fill.get()
        errorbar = self.errorbar.get()
        if not errorbar:
            errorbar = None
        else:
            errorbar = "sd"
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if any([x, y, hue]):
            if not x:
                showerror("Error", "X-axis is required")
                return
            if not y:
                showerror("Error", "Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.barplot(data=self.df, x=x, y=y, hue=hue, estimator=estimator, errorbar=errorbar, fill=fill)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.show()
        except Exception as e:
            showerror("Error", "An error occured while visualizing")

    def AddToDashboard(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        estimator = self.estimator.get()
        fill = self.fill.get()
        errorbar = self.errorbar.get()
        if not errorbar:
            errorbar = None
        else:
            errorbar = "sd"
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if any([x, y, hue]):
            if not x:
                showerror("Error", "X-axis is required")
                return
            if not y:
                showerror("Error", "Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.barplot(data=self.df, x=x, y=y, hue=hue, estimator=estimator, errorbar=errorbar, fill=fill)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            path = f"plots/Barplot_{Title}_{xlabel}_{ylabel}_{hue}_{estimator}_{fill}_{errorbar}_{x}_{y}.png"
            plt.savefig(path)
            plt.clf()
            plt.close()
            for key, value in self.dfs.items():
                if self.df.equals(value):
                    df = key
            self.plots[f"{len(self.plots)+1}"] = [len(self.plots)+1, df,"Barplot",x,y, path]
            showinfo("Success", "Plot added to dashboard")
        except Exception as e:
            showerror("Error", "An error occured while adding to dashboard")
class BoxplotFrame(VisulazationFrame):
    def __init__(self, root, df, plots={}, dfs ={}) -> None:
        super().__init__(root, df, plots, dfs)
        self.hueLabel = tb.Label(self.optionsFrame, text="Color", width=20)
        self.hue = tb.Combobox(self.optionsFrame, values = [""] + list(self.df.columns), width=20, state="readonly")
        self.hue.set("")
        self.gapLabel = tb.Label(self.optionsFrame, text="Gap", width=20)
        self.gap = tb.Entry(self.optionsFrame, width=20)
        self.gap.insert(0, "0")
        self.widthLabel = tb.Label(self.optionsFrame, text="Width", width=20)
        self.width = tb.Entry(self.optionsFrame, width=20)
        self.width.insert(0, "0.8")
        self.fill = tb.IntVar()
        self.fillCheck = tb.Checkbutton(self.optionsFrame, text="Fill", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.fill)
        self.fill.set(True)
        self.nativescale = tb.IntVar()
        self.nativescaleCheck = tb.Checkbutton(self.optionsFrame, text="Native Scale", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.nativescale)
        self.nativescale.set(False)
        self.resetButton.config(command=self.reset)
        self.Vizbutton.config(command=self.Visualize)
        self.AddButton.config(command=self.AddToDashboard)
        self.grid()

    def grid(self):
        super().grid()
        self.hueLabel.grid(row=6, column=1)
        self.hue.grid(row=7, column=1)
        self.gapLabel.grid(row=6, column=0)
        self.gap.grid(row=7, column=0)
        self.widthLabel.grid(row=8, column=0)
        self.width.grid(row=9, column=0)
        self.fillCheck.grid(row=8, column=1)
        self.nativescaleCheck.grid(row=9, column=1)
    def reset(self):
        self.vizTitle.delete(0, END)
        self.vizxLabel.delete(0, END)
        self.vizyLabel.delete(0, END)
        self.hue.set("")
        self.vizx.set("")
        self.vizy.set("")
        self.gap.delete(0, END)
        self.gap.insert(0, "0")
        self.width.delete(0, END)
        self.width.insert(0, "0.8")
        self.fill.set(True)
        self.nativescale.set(False)
    def set_df(self, df):
        super().set_df(df)
        self.hue.config(values=[""]+list(self.df.columns))
    def Visualize(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        gap = self.gap.get()
        width = self.width.get()
        fill = self.fill.get()
        nativescale = self.nativescale.get()
        try:
            gap = float(gap)
        except:
            showerror("Error", "Gap must be a float")
            return
        try:
            width = float(width)
        except:
            showerror("Error", "Width must be a float")
            return
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if any([x, y, hue]):
            if not (x or y):
                showerror("Error", "X-axis or Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.boxplot(data=self.df, x=x, y=y, hue=hue, width=width, gap=gap, fill=fill, dodge=True, orient="v", color=None, palette=None, saturation=0.75, linewidth=None, whis=1.5)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.show()
        except Exception as e:
            showerror("Error", "An error occured while visualizing")
    
    def AddToDashboard(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        gap = self.gap.get()
        width = self.width.get()
        fill = self.fill.get()
        nativescale = self.nativescale.get()
        try:
            gap = float(gap)
        except:
            showerror("Error", "Gap must be a float")
            return
        try:
            width = float(width)
        except:
            showerror("Error", "Width must be a float")
            return
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if any([x, y, hue]):
            if not (x or y):
                showerror("Error", "X-axis or Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.boxplot(data=self.df, x=x, y=y, hue=hue, width=width, gap=gap, fill=fill, dodge=True, orient="v", color=None, palette=None, saturation=0.75, linewidth=None, whis=1.5)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            path = f"plots/Boxplot_{Title}_{xlabel}_{ylabel}_{hue}_{gap}_{width}_{fill}_{nativescale}_{x}_{y}.png"
            plt.savefig(path)
            plt.clf()
            plt.close()
            for key, value in self.dfs.items():
                if self.df.equals(value):
                    df = key
            self.plots[f"{len(self.plots)+1}"] = [len(self.plots)+1, df,"Boxplot",x,y, path]
            showinfo("Success", "Plot added to dashboard")
        except Exception as e:
            showerror("Error", "An error occured while adding to dashboard")

class ViolinplotFrame(BoxplotFrame):
    def __init__(self, root, df, plots = {}, dfs = {}) -> None:
        super().__init__(root, df, plots, dfs)
        self.split = tb.IntVar()
        self.innerLabel = tb.Label(self.optionsFrame, text="Inner", width=20)
        self.inner = tb.Combobox(self.optionsFrame, values=["box", "quartile", "point", "stick", "None"], width=20, state="readonly")
        self.inner.set("box")
        self.densitynormLabel = tb.Label(self.optionsFrame, text="Density Norm", width=20)
        self.densitynorm = tb.Combobox(self.optionsFrame, values=["area", "count", "width"], width=20, state="readonly")
        self.densitynorm.set("area")
        self.splitCheck = tb.Checkbutton(self.optionsFrame, text="Split", width=20, bootstyle="round-toggle", offvalue=False, onvalue=True, variable=self.split)
        self.split.set(False)
        self.resetButton.config(command=self.reset)
        self.Vizbutton.config(command=self.Visualize)
        self.AddButton.config(command=self.AddToDashboard)
        self.grid_more()
    
    def grid_more(self):
        self.innerLabel.grid(row=10, column=0)
        self.inner.grid(row=11, column=0)
        self.densitynormLabel.grid(row=10, column=1)
        self.densitynorm.grid(row=11, column=1)
        self.splitCheck.grid(row=12, column=0, columnspan=2)
    def reset(self):
        super().reset()
        self.split.set(False)
        self.inner.set("box")
        self.densitynorm.set("area")
    def Visualize(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        gap = self.gap.get()
        width = self.width.get()
        fill = self.fill.get()
        nativescale = self.nativescale.get()
        split = self.split.get()
        inner = self.inner.get()
        densitynorm = self.densitynorm.get()
        if inner == "None":
            inner = None
        try:
            gap = float(gap)
        except:
            showerror("Error", "Gap must be a float")
            return
        try:
            width = float(width)
        except:
            showerror("Error", "Width must be a float")
            return
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if any([x, y, hue]):
            if not (x or y):
                showerror("Error", "X-axis or Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.violinplot(data=self.df, x=x, y=y, hue=hue, width=width, gap=gap, inner=inner, split=split, fill=fill, native_scale=nativescale, density_norm=densitynorm)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            plt.show()
        except Exception as e:
            showerror("Error", "An error occured while visualizing")
    
    def AddToDashboard(self):
        plt.clf()
        Title = self.vizTitle.get()
        x = self.vizx.get()
        y = self.vizy.get()
        xlabel = self.vizxLabel.get()
        ylabel = self.vizyLabel.get()
        hue = self.hue.get()
        gap = self.gap.get()
        width = self.width.get()
        fill = self.fill.get()
        nativescale = self.nativescale.get()
        split = self.split.get()
        inner = self.inner.get()
        densitynorm = self.densitynorm.get()
        if inner == "None":
            inner = None
        try:
            gap = float(gap)
        except:
            showerror("Error", "Gap must be a float")
            return
        try:
            width = float(width)
        except:
            showerror("Error", "Width must be a float")
            return
        if x == "":
            x = None
        if y == "":
            y = None
        if hue == "":
            hue = None
        if any([x, y, hue]):
            if not (x or y):
                showerror("Error", "X-axis or Y-axis is required")
                return
        try:
            sns.set_theme(style="darkgrid", context="notebook", palette="deep", font="sans-serif", font_scale=1, color_codes=True, rc=None)
            sns.violinplot(data=self.df, x=x, y=y, hue=hue, width=width, gap=gap, inner=inner, split=split, fill=fill, native_scale=nativescale, density_norm=densitynorm)
            if Title:
                plt.title(Title)
            if xlabel:
                plt.xlabel(xlabel)
            if ylabel:
                plt.ylabel(ylabel)
            path = f"plots/Violinplot_{Title}_{xlabel}_{ylabel}_{hue}_{gap}_{width}_{fill}_{nativescale}_{split}_{inner}_{densitynorm}_{x}_{y}.png"
            plt.savefig(path)
            plt.clf()
            plt.close()
            for key, value in self.dfs.items():
                if self.df.equals(value):
                    dataframe = key
            self.plots[f"{len(self.plots)+1}"] = [len(self.plots)+1, dataframe,"Violinplot",x,y, path]
            showinfo("Success", "Plot added to dashboard")
        except Exception as e:
            print(e)
            showerror("Error", "An error occured while adding plot to dashboard")
            return


if __name__ == "__main__":
    root = tb.Window(themename='superhero', title='SciDataVizLab')
    df = pd.read_csv("iris.csv")
    print(df)
    app = PieplotFrame(root, df)
    app.pack()
    root.mainloop()