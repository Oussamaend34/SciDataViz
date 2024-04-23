import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from error import Error
import numpy.core._exceptions as numpy_exceptions
import csv
import pickle
np.complex128

class BuitInFunc:
    
    Functions = {"type": 1, "float": 1, "write": -1, "len": 1, "import": 1, "dataframe":1, "scatterplot":4,
                    "linspace":3, "range":3, "vector":1, "array":1, "string":1, "integer":1, "bool":1, "log":1,
                    "complex":2, "lineplot":3, "sqrt":1, "abs":1, "sin":1, "cos":1, "tan":1, "asin":1, "acos":1,
                    "atan":1, "sinh":1, "cosh":1, "tanh":1, "asinh":1, "acosh":1, "atanh":1, "exp":1, "log10":1,
                    "log2":1, "log1p":1, "expm1":1, "cbrt":1, "square":1, "deg2rad":1, "rad2deg":1, "radians":1,
                    "degrees":1, "ceil":1, "floor":1, "trunc":1, "round":1, "std":1, "mean":1,"sum":1, "ones":1,
                    "zeros":1, "eye":1, "diag":1, "rand":1, "randn":1, "randint":3, "randint":3, "randint":3,
                    "histplot":4, "View":1, 'head':1, 'tail':1, 'info':1, 'describe':1, 'shape':1, 'columns':1,}
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
            case "std":
                return True if len(self.arguments) == 1 else False
            case "mean":
                return True if len(self.arguments) == 1 else False
            case "sum":
                return True if len(self.arguments) == 1 else False
            case "eye":
                return True if len(self.arguments) == 1 else False
            case "diag":
                return True if len(self.arguments) == 1 else False
            case "rand":
                return True if len(self.arguments) == 1 else False
            case "randn":
                return True if len(self.arguments) == 1 else False
            case "randint":
                return True if len(self.arguments) in range(2,4) else False
            case "histplot":
                return True if len(self.arguments) in range(2,5) else False
            case "View":
                return False
            case 'head':
                return True if len(self.arguments) == 1 else False
            case 'tail':
                return True if len(self.arguments) == 1 else False
            case 'info':
                return True if len(self.arguments) == 1 else False
            case 'describe':
                return True if len(self.arguments) == 1 else False
            case 'shape':
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
                    return self.raiseArgumentTypeError(int)
                case "string":
                    return self.raiseArgumentTypeError(str)
                case "array":
                    return self.raiseArgumentTypeError(np.array)
                case "vector":
                    return tuple(self.arguments[0])
                case "dataframe":
                    return self.raiseArgumentTypeError(pd.DataFrame)
                case "len":
                    return self.raiseArgumentTypeError(len)
                case "bool":
                    return self.raiseArgumentTypeError(bool)
                case "import":
                    return read(self.arguments[0])
                case "sqrt":
                    return self.raiseArgumentTypeError(sqrt)
                case "abs":
                    return self.raiseArgumentTypeError(abs)
                case "sin":
                    return self.raiseArgumentTypeError(np.sin)
                case "cos":
                    return self.raiseArgumentTypeError(np.cos)
                case "tan":
                    return self.raiseArgumentTypeError(np.tan)
                case "asin":
                    return self.raiseArgumentTypeError(np.arcsin)
                case "acos":
                    return self.raiseArgumentTypeError(np.arccos)
                case "atan":
                    return self.raiseArgumentTypeError(np.arctan)
                case "sinh":
                    return self.raiseArgumentTypeError(np.sinh)
                case "cosh":
                    return self.raiseArgumentTypeError(np.cosh)
                case "tanh":
                    return self.raiseArgumentTypeError(np.tanh)
                case "asinh":
                    return self.raiseArgumentTypeError(np.arcsinh)
                case "acosh":
                    return self.raiseArgumentTypeError(np.arccosh)
                case "atanh":
                    return self.raiseArgumentTypeError(np.arctanh)
                case "exp":
                    return self.raiseArgumentTypeError(np.exp)
                case "log10":
                    return self.raiseArgumentTypeError(lambda e: logarithm(self.arguments, np.log10))
                case "log2":
                    return self.raiseArgumentTypeError(lambda e:logarithm(self.arguments, np.log2))
                case "log1p":
                    return np.log1p(self.arguments[0])
                case "expm1":
                    return np.expm1(self.arguments[0])
                case "cbrt":
                    return np.cbrt(self.arguments[0])
                case "square":
                    return self.raiseArgumentTypeError(np.square)
                case "deg2rad":
                    return self.raiseArgumentTypeError(np.deg2rad)
                case "rad2deg":
                    return self.raiseArgumentTypeError(np.rad2deg)
                case "radians":
                    return self.raiseArgumentTypeError(np.radians)
                case "degrees":
                    return self.raiseArgumentTypeError(np.degrees)
                case "ceil":
                    return self.raiseArgumentTypeError(np.ceil)
                case "floor":
                    return self.raiseArgumentTypeError(np.floor)
                case "trunc":
                    return self.raiseArgumentTypeError(np.trunc)
                case "round":
                    return self.raiseArgumentTypeError(np.round)
                case "linspace":
                    return linspace(self.arguments)
                case "scatterplot":
                    return scatterplot(self.arguments)
                case "lineplot":
                    return lineplot(self.arguments)
                case "histplot":
                    return histplot(self.arguments)
                case "range":
                    return rangeF(self.arguments)
                case "write":
                    for argument in self.arguments:
                        print(argument, end= " ")
                    print()
                    return None
                case "log":
                    return self.raiseArgumentTypeError(lambda e:logarithm(self.arguments, np.log))
                case "std":
                    return float(np.std(self.arguments[0]))
                case "mean":
                    return float(np.mean(self.arguments[0]))
                case "sum":
                    return float(np.sum(self.arguments[0]))
                case "ones":
                    return np.ones(self.arguments[0])
                case "zeros":
                    return np.zeros(self.arguments[0])
                case "eye":
                    return np.eye(self.arguments[0])
                case "diag":
                    return np.diag(self.arguments[0])
                case "rand":
                    return np.random.rand(self.arguments[0])
                case "randn":
                    return np.random.randn(self.arguments[0])
                case "randint":
                    return np.random.randint(self.arguments[0], self.arguments[1], self.arguments[2])
                case _ :
                    return None
        else:
            return Error("ArgumentNumberError", f"{self.name}() takes {BuitInFunc.Functions[self.name]} argument {len(self.arguments)} were given")
        
    def __str__(self) -> str:
        return (str(self.name) + " " + str(self.arguments))

    def raiseArgumentTypeError(self, function):
        try:
            return function(self.arguments[0])
        except (TypeError, numpy_exceptions._UFuncNoLoopError, ValueError) as e:
            return Error("ArgumentTypeError", f"You provided an invalid argument for {self.name}")

def sqrt(arguments):
    if isinstance(arguments[0],(int,float)) and arguments[0] < 0:
        return complex(np.sqrt(complex(arguments[0])))
    if isinstance(arguments[0],np.ndarray) and (arguments[0] < 0).any():
        return np.sqrt(arguments[0].astype(complex))
    return  np.sqrt(arguments[0])
def logarithm(arguments, logFunc):
    if isinstance(arguments[0], np.ndarray) and (arguments[0] < 0).any():
        return logFunc(arguments[0].astype(complex))
    elif isinstance(arguments[0], np.ndarray):
        return logFunc(arguments[0])
    if arguments[0] < 0:
        return complex(logFunc(complex(arguments[0])))
    return logFunc(arguments[0])
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
        except:
            pass
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
def histplot(arguments):
    if len(arguments) == 2:
        data = arguments[0]
        x = arguments[1]
        sns.histplot(data, x = x)
    if len(arguments) == 3:
        data = arguments[0]
        x = arguments[1]
        hue = arguments[2]
        sns.histplot(data, x = x, hue = hue)
    plt.show()
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

