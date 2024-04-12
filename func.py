import pickle
import numpy as np
import pandas as pd
import csv

class Func:
    def __init__(self, name, arguments) -> None:
        self.name = name
        self.arguments = list(arguments)


class BuitInFunc:
    Functions = {"type": 1, "float": 1, "write": -1, "len": 1, "import": 1, "dataframe":1}
    def __init__(self, name, arguments) -> None:
        self.name = name
        self.arguments = list(arguments)
    def checkArgument(self):
        match self.name:
            case "type":
                return True if len(self.arguments) == 1 else False
            case "float":
                return True if len(self.arguments) == 1 else False
            case "integer":
                return True if len(self.arguments) == 1 else False
            case "string":
                return True if len(self.arguments) == 1 else False
            case "array":
                return True if len(self.arguments) == 1 else False
            case "vector":
                return True if len(self.arguments) == 1 else False
            case "dataframe":
                return True if len(self.arguments) == 1 else False
            case "bool":
                return True if len(self.arguments) == 1 else False
            case "len":
                return True if len(self.arguments) == 1 else False
            case "import":
                return True if len(self.arguments) == 1 else False
            case _ :
                return True
            


    def addArgument(self, argument):
        self.arguments.insert(0,argument)
    def exec(self):
        if self.checkArgument():
            match self.name:
                case "type":
                    if self.checkArgument():
                        with open('primitiveDataTypes.pickle', 'rb') as f:
                            dataTypes = pickle.load(f)
                        return dataTypes[type(self.arguments[0])]
                    else:
                        print(f"Argument Error: {self.name}() takes {BuitInFunc.Functions[self.name]} argument {len(self.arguments)} were given")
                        return None
                case "float":
                    return float(self.arguments[0])
                case "integer":
                    return int(self.arguments[0])
                case "string":
                    return str(self.arguments[0])
                case "array":
                    return np.array(self.arguments[0])
                case "vector":
                    return tuple(self.arguments[0])
                case "dataframe":
                    return pd.DataFrame(self.arguments[0])
                case "len":
                    return len(self.arguments[0])
                case "bool":
                    return bool(self.arguments[0])
                case "import":
                    return read(self.arguments[0])
                case "write":
                    for argument in self.arguments:
                        print(argument, end= " ")
                    print()
                    return None
                case _ :
                    return None
        else:
            print(f"Argument Error: {self.name}() takes {BuitInFunc.Functions[self.name]} argument {len(self.arguments)} were given")
            return None
        
    def __str__(self) -> str:
        return (str(self.name) + " " + str(self.arguments))




def read_csv(filename):
    with open(filename, newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.readline(), delimiters=';,|#\t')
        csvfile.seek(0)
        header  = csv.Sniffer().has_header(csvfile.readline())
    if header:
        return pd.read_csv(filename, sep=dialect.delimiter, header=0)
    else:
        return pd.read_csv(filename, sep=dialect.delimiter)
def read(filename):
    functions = [read_csv, pd.read_excel, pd.read_json]
    for f in functions:
        try:
            return f(filename)
            break
        except:
            pass
    print("Error reading file.")
    return None







    #     switch_case = {
    #         "print": self.print_func,
    #         "len": self.len_func
    #     }

    #     func = switch_case.get(self.name, self.unknown_func)
    #     func()

    # def print_func(self):
    #     print(*self.arguments)

    # def len_func(self):
    #     result = len(self.arguments[0])
    #     print(result)

    # def unknown_func(self):
    #     print("Unknown function")
    #     if self.name == "print":
    #         print(*self.arguments)
    #     elif self.name == "len":
    #         result = len(self.arguments[0])
    #         print(result)
    #     else:
    #         print("Unknown function")





