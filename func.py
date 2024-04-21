import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cmath
import csv
import pickle
np.complex128

class BuitInFunc:
    
    Functions = {"type": 1, "float": 1, "write": -1, "len": 1, "import": 1, "dataframe":1, "scatterplot":4, "linspace":3, "range":3, "vector":1, "array":1, "string":1, "integer":1, "bool":1, "log":1, "complex":2, "lineplot":3, "sqrt":1, "abs":1, "sin":1, "cos":1, "tan":1, "asin":1, "acos":1, "atan":1, "sinh":1, "cosh":1, "tanh":1, "asinh":1, "acosh":1, "atanh":1, "exp":1, "log10":1, "log2":1, "log1p":1, "expm1":1, "cbrt":1, "square":1, "deg2rad":1, "rad2deg":1, "radians":1, "degrees":1, "ceil":1, "floor":1, "trunc":1, "round":1, "isfinite":1, "isinf":1, "isnan":1, "isnat":1, "signbit":1, "copysign":2, "fabs":1, "fmod":2, "modf":1, "remainder":2, "gcd":2, "lcm":2, "add":2, "subtract":2, "multiply":2, "divide":2, "true_divide":2, "floor_divide":2, "power":2, "mod":2, "remainder":2, "divmod":2, "negative":1, "positive":1, "absolute":1, "invert":1, "left_shift":2, "right_shift":2, "and":2, "or":2, "xor":2, "logical_and":2, "logical_or":2, "logical_xor":2, "logical_not":1, "maximum":2, "minimum":2, "fmax":2, "fmin":2, "heaviside":2, "isfinite":1, "isinf":1, "isnan":1, "isnat":1, "signbit":1, "copysign":2, "fabs":1, "fmod":2, "modf":1, "remainder":2, "gcd":2, "lcm":2, "add":2, "subtract":2, "multiply":2, "divide":2, "true_divide":2, "floor_divide":2, "power":2}
    def __init__(self, name, arguments) -> None:
        self.name = name
        self.arguments = list(arguments)
    def checkArgument(self):
        match self.name:
            case "type":
                return True if len(self.arguments) == 1 else False
            case "float":
                return True if len(self.arguments) == 1 else False
            case "write":
                return True if len(self.arguments) >= 1 else False
            case "log":
                return True if len(self.arguments) == 1 else False
            case "complex":
                return True if len(self.arguments) == 2 else False
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
            case "scatterplot":
                return True if len(self.arguments) in range(2,5) else False
            case "lineplot":
                return True if len(self.arguments) in range(2,4) else False
            case "linspace":
                return True if len(self.arguments) in range(2,4) else False
            case "range":
                return True if len(self.arguments) in range(1,4) else False
            case "sqrt":
                return True if len(self.arguments) == 1 else False
            case "abs":
                return True if len(self.arguments) == 1 else False
            case "sin":
                return True if len(self.arguments) == 1 else False
            case "cos":
                return True if len(self.arguments) == 1 else False
            case "tan":
                return True if len(self.arguments) == 1 else False
            case "asin":
                return True if len(self.arguments) == 1 else False
            case "acos":
                return True if len(self.arguments) == 1 else False
            case "atan":
                return True if len(self.arguments) == 1 else False
            case "sinh":
                return True if len(self.arguments) == 1 else False
            case "cosh":
                return True if len(self.arguments) == 1 else False
            case "tanh":
                return True if len(self.arguments) == 1 else False
            case "asinh":
                return True if len(self.arguments) == 1 else False
            case "acosh":
                return True if len(self.arguments) == 1 else False
            case "atanh":
                return True if len(self.arguments) == 1 else False
            case "exp":
                return True if len(self.arguments) == 1 else False
            case "log10":
                return True if len(self.arguments) == 1 else False
            case "log2":
                return True if len(self.arguments) == 1 else False
            case "log1p":
                return True if len(self.arguments) == 1 else False
            case "expm1":
                return True if len(self.arguments) == 1 else False
            case "cbrt":
                return True if len(self.arguments) == 1 else False
            case "square":
                return True if len(self.arguments) == 1 else False
            case "deg2rad":
                return True if len(self.arguments) == 1 else False
            case "rad2deg":
                return True if len(self.arguments) == 1 else False
            case "radians":
                return True if len(self.arguments) == 1 else False
            case "degrees":
                return True if len(self.arguments) == 1 else False
            case "ceil":
                return True if len(self.arguments) == 1 else False
            case "floor":
                return True if len(self.arguments) == 1 else False
            case "trunc":
                return True if len(self.arguments) == 1 else False
            case "round":
                return True if len(self.arguments) == 1 else False
            case "ones":
                return True if len(self.arguments) == 1 else False
            case "zeros":
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
                case "complex":
                    if isinstance(self.arguments[0], (int, float)) and isinstance(self.arguments[1], (int, float)):
                        return complex(self.arguments[0], self.arguments[1])
                    else:
                        print("Error: Complex numbers must be created from two numbers.")
                        return None
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
                case "sqrt":
                    if isinstance(self.arguments[0],(int,float)) and self.arguments[0] < 0:
                        return complex(np.sqrt(complex(self.arguments[0])))
                    if isinstance(self.arguments[0],np.ndarray) and (self.arguments[0] < 0).any():
                        return np.sqrt(self.arguments[0].astype(complex))
                    return  np.sqrt(self.arguments[0])
                case "abs":
                    return np.abs(self.arguments[0])
                case "sin":
                    return np.sin(self.arguments[0])
                case "cos":
                    return np.cos(self.arguments[0])
                case "tan":
                    return np.tan(self.arguments[0])
                case "asin":
                    return np.arcsin(self.arguments[0])
                case "acos":
                    return np.arccos(self.arguments[0])
                case "atan":
                    return np.arctan(self.arguments[0])
                case "sinh":
                    return np.sinh(self.arguments[0])
                case "cosh":
                    return np.cosh(self.arguments[0])
                case "tanh":
                    return np.tanh(self.arguments[0])
                case "asinh":
                    return np.arcsinh(self.arguments[0])
                case "acosh":
                    return np.arccosh(self.arguments[0])
                case "atanh":
                    return np.arctanh(self.arguments[0])
                case "exp":
                    return np.exp(self.arguments[0])
                case "log10":
                    return np.log10(self.arguments[0])
                case "log2":
                    return np.log2(self.arguments[0])
                case "log1p":
                    return np.log1p(self.arguments[0])
                case "expm1":
                    return np.expm1(self.arguments[0])
                case "cbrt":
                    return np.cbrt(self.arguments[0])
                case "square":
                    return np.square(self.arguments[0])
                case "deg2rad":
                    return np.deg2rad(self.arguments[0])
                case "rad2deg":
                    return np.rad2deg(self.arguments[0])
                case "radians":
                    return np.radians(self.arguments[0])
                case "degrees":
                    return np.degrees(self.arguments[0])
                case "ceil":
                    return np.ceil(self.arguments[0])
                case "floor":
                    return np.floor(self.arguments[0])
                case "trunc":
                    return np.trunc(self.arguments[0])
                case "round":
                    return np.round(self.arguments[0])
                case "linspace":
                    return linspace(self.arguments)
                case "scatterplot":
                    return scatterplot(self.arguments)
                case "lineplot":
                    return lineplot(self.arguments)
                case "range":
                    return rangeF(self.arguments)
                case "write":
                    for argument in self.arguments:
                        print(argument, end= " ")
                    print()
                    return None
                case "log":
                    if isinstance(self.arguments[0], np.ndarray) and (self.arguments[0] < 0).any():
                        return np.log(self.arguments[0].astype(complex))
                    elif isinstance(self.arguments[0], np.ndarray):
                        return np.log(self.arguments[0])
                    if self.arguments[0] < 0:
                        return np.log(complex(self.arguments[0]))
                    return np.log(self.arguments[0])
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
def lineplot(arguments):
    if len(arguments) == 2:
        x_data = arguments[0]
        y_data = arguments[1]
        sns.lineplot(x = x_data, y = y_data)
    if len(arguments) == 3:
        if isinstance(arguments[0], (pd.DataFrame)) and isinstance(arguments[1], (str)) and isinstance(arguments[2], (str)):
            sns.lineplot(data = arguments[0], x = arguments[1], y = arguments[2])
    plt.show()
    return None
def scatterplot(arguments):
    if len(arguments) == 2:
        x_data = arguments[0]
        y_data = arguments[1]
        sns.scatterplot(x = x_data, y = y_data)
    if len(arguments) == 3:
        if isinstance(arguments[0], (pd.DataFrame)) and isinstance(arguments[1], (str)) and isinstance(arguments[2], (str)):
            sns.scatterplot(data = arguments[0], x = arguments[1], y = arguments[2])
    if len(arguments) == 4:
        if isinstance(arguments[0], (pd.DataFrame)) and isinstance(arguments[1], (str)) and isinstance(arguments[2], (str)) and isinstance(arguments[3], (str)):
            sns.scatterplot(data = arguments[0], x = arguments[1], y = arguments[2], hue = arguments[3])
    plt.show()
    return None
def rangeF(arguments):
    if len(arguments) == 1:
        return np.array(range(arguments[0]))
    if len(arguments) == 2:
        return np.array(range(arguments[0], arguments[1]))
    if len(arguments) == 3:
        return np.array(range(arguments[0], arguments[1], arguments[2]))
    return None
def linspace(arguments):
    if len(arguments) == 2:
        if isinstance(arguments[0], (int, float)) and isinstance(arguments[1], (int, float)):
            return np.linspace(arguments[0], arguments[1])
    if len(arguments) == 3:
        if isinstance(arguments[0], (int,float)) and isinstance(arguments[1], (int, float)) and isinstance(arguments[2], int):
            return np.linspace(arguments[0], arguments[1], arguments[2])
    return None

