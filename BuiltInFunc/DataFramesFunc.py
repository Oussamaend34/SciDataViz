import pandas as pd
import numpy as np
from error import Error

class DataFrameFunc():
    Functions = {"head": 1, "tail": 1, "info": 1, "describe": 1, "shape": 1,"columns": 1, "drop": 2, "dropna":1, "index": 1, "query": 2, "sort_values": 2, "sort_index": 0 
                    ,"copy": 1, "drop_duplicates": 1, "to_csv":1, "set_index": 1, "reset_index": 1, "groupby": 1}
    def __init__(self, name, arguments) -> None:
        self.name = name
        self.arguments:list[pd.DataFrame] = list(arguments)
    
    def addArgument(self, argument):
        self.arguments.insert(0,argument)

    def __str__(self) -> str:
        return (str(self.name) + " " + str(self.arguments))
    
    def checkarguments(self):
        match self.name:
            case "head":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "tail":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "info":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "describe":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "shape":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], (pd.DataFrame, np.ndarray))
            case "columns":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "index":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "drop":
                return len(self.arguments) == 2 and isinstance(self.arguments[0], pd.DataFrame) and (isinstance(self.arguments[1], np.ndarray) or isinstance(self.arguments[1], str))
            case "dropna":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "query":
                return len(self.arguments) == 2 and isinstance(self.arguments[0], pd.DataFrame) and isinstance(self.arguments[1], str)
            case "sort_values":
                return len(self.arguments) == 2 and isinstance(self.arguments[0], pd.DataFrame) and isinstance(self.arguments[1], str)
            case "sort_index":
                return len(self.arguments) == 0
            case "copy":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "drop_duplicates":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "to_csv":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case "set_index":
                return len(self.arguments) == 2 and isinstance(self.arguments[0], pd.DataFrame) and isinstance(self.arguments[1], str)
            case "reset_index":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], pd.DataFrame)
            case _:
                return False
            

    def exec(self):
        if self.checkarguments():
            match self.name:
                case "head":
                    return self.arguments[0].head()
                case "tail":
                    return self.arguments[0].tail()
                case "info":
                    return self.arguments[0].info()
                case "describe":
                    return self.arguments[0].describe()
                case "shape":
                    return self.arguments[0].shape
                case "columns":
                    return tuple(self.arguments[0].columns)
                case "index":
                    return tuple(self.arguments[0].index)
                case "drop":
                    if isinstance(self.arguments[1], str) and not self.arguments[1] in self.arguments[0].columns:
                        return Error("ValueError", f"Column {self.arguments[1]} not found")
                    if isinstance(self.arguments[1], np.ndarray) and not all(col in self.arguments[0].columns for col in self.arguments[1]):
                        return Error("ValueError", f"Column {self.arguments[1]} not found")
                    return self.arguments[0].drop(columns = self.arguments[1])
                case "dropna":
                    return self.arguments[0].dropna()
                case "query":
                    return query(self.arguments[0], self.arguments[1])
                case "sort_values":
                    if  not self.arguments[1] in self.arguments[0].columns:
                        return Error("ValueError", f"Column {self.arguments[1]} not found")
                    return sort_values(self.arguments[0], self.arguments[1])
                case "sort_index":
                    return self.arguments[0].sort_index()
                case "copy":
                    return self.arguments[0].copy()
                case "drop_duplicates":
                    return self.arguments[0].drop_duplicates()
                case "to_csv":
                    return self.arguments[0].to_csv()
                case "set_index":
                    if not self.arguments[1] in self.arguments[0].columns:
                        return Error("ValueError", f"Column {self.arguments[1]} not found")
                    return self.arguments[0].set_index(self.arguments[1])
                case "reset_index":
                    return self.arguments[0].reset_index()
        elif not isinstance(self.arguments[0], pd.DataFrame):
            return Error("TypeError", "Invalid Type")
        else:
            return Error("ArgumentNumberError", f"{self.name}() takes {DataFrameFunc.Functions[self.name]} argument {len(self.arguments)} were given")



def query(df:pd.DataFrame, query:str):
    try:
        query:pd.DataFrame = df.query(query)
    except Exception as e:
        return Error("ValueError", f"Invalid query {query} : {e}")
    if query.empty:
        return Error("ValueError", "Empty DataFrame")
    return query
def sort_values(df:pd.DataFrame, by:str):
    if by in df.columns:
        return df.sort_values(by = by)
    return Error("ValueError", f"Column {by} not found")

if __name__ == "__main__":
    iris = pd.read_csv("iris.csv")
    print(sort_values(iris, "s"))
