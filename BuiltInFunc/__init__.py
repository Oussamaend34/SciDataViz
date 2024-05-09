from .BasicFunc import BasicFunc
from .DataFramesFunc import DataFrameFunc
from .ArraysFunc import ArraysFunc
from error import Error


def getFunction(name, arguments):
    l = [BasicFunc, DataFrameFunc, ArraysFunc]
    for Functions in l:
        if name in Functions.Functions:
            return Functions(name, arguments)
    return Error("NameError", f"Function {name} not found")

if __name__ == "__main__":
    for function in BasicFunc.Functions:
        if function in DataFrameFunc.Functions:
            print(f"{function} DataFrames")
        if function in ArraysFunc.Functions:
            print(f"{function} Arrays")
    for function in DataFrameFunc.Functions:
        if function in BasicFunc.Functions:
            print(f"{function} Basic")
        if function in ArraysFunc.Functions:
            print(f"{function} Arrays")
    for function in ArraysFunc.Functions:
        if function in BasicFunc.Functions:
            print(f"{function} Basic")
        if function in DataFrameFunc.Functions:
            print(f"{function} DataFrames")