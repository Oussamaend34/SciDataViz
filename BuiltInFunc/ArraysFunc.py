import numpy as np
import pandas as pd
from error import Error


class ArraysFunc():
    Functions = {"zeros": 1, "ones": 1, "arange": 3, "eye": 1, "diag": 1, "full": 2, "random": 1, "inv":1, "transpose":1,"reshape":2,
                "flatten":1, "hstack":2, "vstack":2, "var":1, "quantile":2, "std":1, "mean":1, "median":1, "max":1, "min":1, "sum":1,
                "norm":2, }
    def __init__(self, name, arguments) -> None:
        self.name = name
        self.arguments = list(arguments)
    
    def addArgument(self, argument):
        self.arguments.insert(0,argument)
    
    def __str__(self) -> str:
        return (str(self.name) + " " + str(self.arguments))
    
    def checkarguments(self):
        match self.name:
            case "zeros":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], (int, np.ndarray))
            case "ones":
                return len(self.arguments) == 1 and (isinstance(self.arguments[0], int), isinstance(self.arguments[0], tuple))
            case "arange":
                return len(self.arguments) in range(1,4) and all(isinstance(i, int) for i in self.arguments)
            case "eye":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], int)
            case "diag":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray, list, tuple)
            case "full":
                return len(self.arguments) == 2 and isinstance(self.arguments[0], int) and isinstance(self.arguments[1], (tuple, int, float))
            case "random":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], int)
            case "inv":
                try:
                    return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
                except np.linalg.LinAlgError:
                    return Error("LinAlgError", "Singular matrix")
            case "transpose":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "reshape":
                return len(self.arguments) == 2 and isinstance(self.arguments[0], np.ndarray) and isinstance(self.arguments[1], tuple) and all(isinstance(i, int) for i in self.arguments[1])
            case "flatter":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "hstack":
                return len(self.arguments) >= 2 and all(isinstance(i, np.ndarray) for i in self.arguments)
            case "vstack":
                return len(self.arguments) >= 2 and all(isinstance(i, np.ndarray) for i in self.arguments)
            case "var":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "quantile":
                return len(self.arguments) == 2 and isinstance(self.arguments[0], np.ndarray) and isinstance(self.arguments[1], float) and 0 <= self.arguments[1] <= 1
            case "std":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "mean":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "median":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "max":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "min":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "sum":
                return len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case "norm":
                return (len(self.arguments) == 2 and isinstance(self.arguments[0], np.ndarray) and ((isinstance(self.arguments[1], int) and self.arguments[1]>0) or self.arguments[1] in [np.inf, -np.inf, "fro", 'nuc'])) or len(self.arguments) == 1 and isinstance(self.arguments[0], np.ndarray)
            case _:
                return False
    
    def exec(self):
        if self.checkarguments():
            match self.name:
                case "zeros":
                    return np.zeros(self.arguments[0])
                case "ones":
                    return np.ones(self.arguments[0])
                case "arange":
                    return arange(self.arguments)
                case "eye":
                    return np.eye(self.arguments[0])
                case "diag":
                    return np.diag(self.arguments[0])
                case "full":
                    return np.full(self.arguments[0], self.arguments[1])
                case "random":
                    return np.random.rand(self.arguments[0])
                case "inv":
                    return np.linalg.inv(self.arguments[0])
                case "transpose":
                    return np.transpose(self.arguments[0])
                case "reshape":
                    try:
                        return np.reshape(self.arguments[0], self.arguments[1])
                    except ValueError:
                        return Error("ValueError", "Unvalid new size for the array")
                case "flatten":
                    return self.arguments[0].flatten()
                case "hstack":
                    try:
                        return np.hstack(self.arguments)
                    except ValueError as e:
                        return Error("ValueError", e)
                case "vstack":
                    try:
                        return np.vstack(self.arguments)
                    except ValueError as e:
                        return Error("ValueError", e)
                case "var":
                    return np.var(self.arguments[0])
                case "quantile":
                    return np.quantile(self.arguments[0], self.arguments[1])
                case "std":
                    return np.std(self.arguments[0])
                case "mean":
                    return np.mean(self.arguments[0])
                case "median":
                    return np.median(self.arguments[0])
                case "max":
                    return np.max(self.arguments[0])
                case "min":
                    return np.min(self.arguments[0])
                case "sum":
                    return np.sum(self.arguments[0])
                case "norm":
                    try:
                        if len(self.arguments) == 1:
                            return np.linalg.norm(self.arguments[0])
                        else:    
                            return np.linalg.norm(self.arguments[0], self.arguments[1])
                    except ValueError:
                        return Error("ValueError", "Invalid operations fo this matrix")
        else:
            return Error("type error", f"Invalid arguments for {self.name} function")

def arange(args):
    if len(args) == 1:
        return np.arange(args[0])
    elif len(args) == 2:
        return np.arange(args[0], args[1])
    else:
        return np.arange(args[0], args[1], args[2])