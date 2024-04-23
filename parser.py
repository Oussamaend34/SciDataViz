from sly import Parser
from lexer import SciDataVizLexer
from func import BuitInFunc
from error import Error
from view_table import TableView
import numpy as np
import numpy.core._exceptions as np_exceptions
import pandas as pd
import os
import sys
import pickle
import re


class SciDataVizParser(Parser):
    # Get the token list from the lexer (required)
    precedence = (
        ('nonassoc', ASSIGN),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MOD, FLRDIV),
        ('right', UMINUS),
    )
    # debugfile = 'debug.txt'
    tokens = SciDataVizLexer.tokens

    def __init__(self, terminal, notebook) -> None:
        self.values = {"i":complex(0,1), "j": complex(0,1), "e":np.e, "pi":np.pi, "nan":np.nan, "inf":np.inf, "True":True, "False":False}
        with open('primitiveDataTypes.pickle', 'rb') as f:
            self.dataTypes = pickle.load(f)
        self.terminal = terminal
        self.notebook = notebook

    def error(self, token):
        '''
        Default error handling function.  This may be subclassed.
        '''
        err = Error("SyntaxError")
        if token:
            lineno = getattr(token, 'lineno', 0)
            if lineno:
                err.message = f"line {lineno} at '{token.value}'"
            else:
                err.message = f"'{token.value}'"
        else:
            err.message = 'at EOF'
        self.terminal.insert("end",f'\n{err}')
    # Grammar rules and actions
    @_('statements')
    def s(self, p):
        return p.statements
    @_('statement')
    def statements(self, p):
        return p.statement
    @_('statement ";" statements')
    def statements(self, p):
        if isinstance(p.statement, Error):
            return p.statement
        return p.statements
    @_('empty')
    def statements(self, p):
        return None
    @_('value')
    def statement(self, p):
        return p.value
    @_('')
    def empty(self, p):
        pass
    @_('value PLUS term')
    def value(self, p):
        if isinstance(p.value, Error):
            return p.value
        if isinstance(p.term, Error):
            return p.term
        try:
            return np.add(p.value, p.term)
        except (ValueError,np_exceptions.UFuncTypeError, TypeError) as e:
            if isinstance(e,ValueError):
                return Error("ValueError", "Matrices are not aligned")
            elif isinstance(e,TypeError):
                return Error("TypeError", f"You can't add a {self.dataTypes[type(p.value)]} and a {self.dataTypes[type(p.term)]}")
            elif isinstance(e,np_exceptions.UFuncTypeError):
                return Error("TypeError", "You can only do element wise addition between two arrays of the same data type")
    @_('value MINUS term')
    def value(self, p):
        if isinstance(p.value, Error):
            return p.value
        if isinstance(p.term, Error):
            return p.term
        try:
            return np.subtract(p.value, p.term)
        except (ValueError,np_exceptions.UFuncTypeError, TypeError) as e:
            if isinstance(e,ValueError):
                return Error("ValueError", "Matrices are not aligned")
            elif isinstance(e,TypeError):
                return Error("TypeError", f"You can't subtract a {self.dataTypes[type(p.value)]} and a {self.dataTypes[type(p.term)]}")
            elif isinstance(e,np_exceptions.UFuncTypeError):
                return Error("TypeError", "You can only do element wise subtraction between two arrays of the same data type")

    @_('MINUS factor %prec UMINUS')
    def factor(self, p):
        if isinstance(p.factor, Error):
            return p.factor
        return -p.factor
    @_('term')
    def value(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        if isinstance(p.term, Error):
            return p.term
        if isinstance(p.factor, Error):
            return p.factor
        if self.areDigits(p.term, p.factor):
            return p.term * p.factor
        if isinstance(p.term, np.ndarray) and isinstance(p.factor, np.ndarray):
            if p.term.dtype == p.factor.dtype:
                try:
                    return np.multiply(p.term, p.factor)
                except ValueError:
                    return Error("ValueError", "Matrices are not aligned")
            else:
                return Error("TypeError", "You can only do element wise multiplication between two arrays of the same data type")
        try:
            return np.multiply(p.term, p.factor)
        
        except ValueError:
            return Error("TypeError", f"Multiplication between {self.dataTypes[type(p.term)]} and {self.dataTypes[type(p.factor)]} is not allowed")

    @_('term MATMUL factor')
    def term(self, p):
        if isinstance(p.term, Error):
            return p.term
        if isinstance(p.factor, Error):
            return p.factor
        if isinstance(p.term, np.ndarray) and isinstance(p.factor, np.ndarray):
            try:
                return np.matmul(p.term, p.factor)
            except ValueError:
                return Error("ValueError", "Matrices are not aligned")
        else:
            return Error("TypeError", "You can only do matrix maltiplication between two arrays")

    @_('term MOD factor')
    def term(self, p):
        if isinstance(p.term, Error):
            return p.term
        if isinstance(p.factor, Error):
            return p.factor
        if self.areDigits(p.term, p.factor):
            return p.term % p.factor
        else:
            try:
                return np.mod(p.term, p.factor)
            except (ValueError, TypeError, np_exceptions.UFuncTypeError) as e:
                if isinstance(e,ValueError):
                    return Error("ValueError", "Matrices are not aligned")
                elif isinstance(e,TypeError):
                    return Error("TypeError", f"You can't mod a {self.dataTypes[type(p.term)]} and a {self.dataTypes[type(p.factor)]}")
                elif isinstance(e,np_exceptions.UFuncTypeError):
                    return Error("TypeError", "You can only do element wise mod between two arrays of the same data type")
                else:
                    return Error("TypeError", "You can only do element wise mod between two arrays of the same data type")

    @_('term DIVIDE factor')
    def term(self, p):
        if isinstance(p.term, Error):
            return p.term
        if isinstance(p.factor, Error):
            return p.factor
        if self.areDigits(p.term, p.factor):
            try:
                return p.term / p.factor
            except ZeroDivisionError:
                return Error("ZeroDivisionError", "Division by zero")
        if isinstance(p.term, np.ndarray) and isinstance(p.factor, np.ndarray):
            if p.term.dtype == p.factor.dtype:
                try:
                    return np.divide(p.term, p.factor)
                except ValueError:
                    return Error("ValueError", "Matrices are not aligned")
            else:
                return Error("TypeError", "You can only do element wise multiplication between two arrays of the same data type")
        try:
            return np.divide(p.term, p.factor)
        
        except ValueError:
            return Error("TypeError", f"Multiplication between {self.dataTypes[type(p.term)]} and {self.dataTypes[type(p.factor)]} is not allowed")

    @_('term FLRDIV factor')
    def term(self, p):
        if isinstance(p.term, Error):
            return p.term
        if isinstance(p.factor, Error):
            return p.factor
        if self.areDigits(p.term, p.factor):
            try:
                return p.term // p.factor
            except ZeroDivisionError:
                return Error("ZeroDivisionError", "Division by zero")
        else:
            try:
                return np.floor_divide(p.term, p.factor)
            except (ValueError, TypeError, np_exceptions.UFuncTypeError) as e:
                if isinstance(e,ValueError):
                    return Error("ValueError", "Matrices are not aligned")
                elif isinstance(e,TypeError):
                    return Error("TypeError", f"You can't floor divide a {self.dataTypes[type(p.term)]} and a {self.dataTypes[type(p.factor)]}")
                elif isinstance(e,np_exceptions.UFuncTypeError):
                    return Error("TypeError", "You can only do element wise floor division between two arrays of the same data type")
                else:
                    return Error("TypeError", "You can only do element wise floor division between two arrays of the same data type")

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER
    
    @_('STRLT')
    def factor(self, p):
        return p.STRLT

    @_('LPAREN value RPAREN')
    def factor(self, p):
        return p.value
    
    @_('ID ASSIGN value')
    def statement(self, p):
        if isinstance(p.value, Error):
            return p.value
        else:
            self.values[p.ID] = p.value
            return None
    @_('ID')
    def factor(self, p):
        return self.getValue(p.ID)
    
    @_('array')
    def factor(self,p):
        return p.array
    
    @_('LSQB elements RSQB')
    def array(self, p):
        return np.array(p.elements)
    @_('empty')
    def elements(self, p):
        return []
    @_('value')
    def elements(self, p):
        return [p.value]
    @_('value "," elements')
    def elements(self, p):
        return [p.value] + p.elements

    @_('QUIT')
    def statement(self, p):
        sys.exit()
    @_('CLEAR')
    def statement(self, p):
        self.terminal.delete("1.0","end")
        return None
    @_('LS')
    def statement(self, p):
        if len(self.values) == 0:
            self.termianl.insert("end", "No variables declared")
        else:
            self.terminal.insert("end", "\nVariable\tValue\n")
            for variable, value in self.values.items():
                value_lines = str(value).splitlines()
                self.terminal.insert("end", f"{variable}\t{value_lines[0]}\n")
                for line in value_lines[1:]:
                    self.terminal.insert("end", f"\t{line}\n")
        return None
    
    @_('vector')
    def factor(self, p):
        return p.vector
    @_('LPAREN elements RPAREN')
    def vector(self, p):
        return tuple(p.elements)
    
    def getValue(self, index):
        try:
            return self.values[index]
        except KeyError:
            return Error("NameError", f"variable {index} have no value")
    def areDigits(self, value1, value2):
        if(type(value1) in [float, int, complex] and type(value2) in [float, int, complex]):
            return True
        else:
            return False
        


    def isiterable(self, value1):
        if (type(value1) in (tuple,np.ndarray, str)):
            return True
        else:
            return False
        

    @_('ID vector')
    def func(self, p):
        if p.ID in BuitInFunc.Functions:
            f = BuitInFunc(p.ID,p.vector)
            return f
        else:
            return Error("NameError", f"Function {p.ID} not found")
    
    @_('func')
    def factor(self, p):
        if isinstance(p.func, Error):
            return p.func
        func:BuitInFunc = p.func
        if func.name == "View" and len(func.arguments) == 1 and isinstance(func.arguments[0], pd.DataFrame):
            Table = TableView(self.notebook, func.arguments[0])
            Table.name = self.get_DataFrame_name(func.arguments[0])
            current_tab = self.notebook.select()
            current_frame = self.notebook.nametowidget(current_tab)
            if any (re.match(r".!frame\d+.!label", child ) for child in map(str, current_frame.winfo_children())):
                self.notebook.forget(current_tab)
            self.notebook.add(Table.frame, text=Table.name)
            self.notebook.select(Table.frame)
            return None
        return p.func.exec()
    @_('READ')
    def value(self,p):
        return input()
    
    @_('value PIPE func')
    def value(self, p):
        if isinstance(p.value, Error):
            return p.value
        if isinstance(p.func, Error):
            return p.func
        p.func.addArgument(p.value)
        return p.func.exec()
    
    @_('json')
    def value(self, p):
        return p.json
    @_('LQB members RQB')
    def json(self, p):
        if isinstance(p.members, Error):
            return p.members
        return {key: value for key, value in p.members}

    @_('pair')
    def members(self, p):
        if isinstance(p.pair, Error):
            return p.pair
        return [p.pair]

    @_('pair "," members')
    def members(self, p):
        if isinstance(p.pair, Error):
            return p.pair
        if isinstance(p.members, Error):
            return p.members
        return [p.pair] + p.members
    
    @_('value ":" value')
    def pair(self, p):
        if isinstance(p.value0, Error):
            return p.value0
        if isinstance(p.value1, Error):
            return p.value1
        if isinstance(p.value0, (dict, np.ndarray)):
            value0 = tuple(p.value0)
        else:
            value0 = p.value0
        if isinstance(p.value1, (dict, np.ndarray)):
            value1 = tuple(p.value1)
        else:
            value1 = p.value1
        return value0, value1
    
    @_('value LSQB value RSQB')
    def value(self,p):
        if isinstance(p.value0, Error):
            return p.value0
        if isinstance(p.value1, Error):
            return p.value1
        if self.isiterable(p.value0):
            lenght = len(p.value0)
            if p.value1 in range(-lenght, lenght):
                return p.value0[p.value1]
            else:
                return Error("IndexError", f"{self.dataTypes[type(p.value0)]} Index out of range")
        elif isinstance(p.value0,(dict)):
            if p.value1 in p.value0:
                return p.value0[p.value1]
            else:
                return Error("KeyError", f"KeyError: {p.value1}")
        elif isinstance(p.value0,(pd.DataFrame)):
            return p.value0[p.value1]
        else:
            return Error("TypeError", f"{self.dataTypes[type(p.value0)]} not subscriptable")
    
    @_('value LSQB value ":" value RSQB')
    def value(self,p):
        if isinstance(p.value0, Error):
            return p.value0
        if isinstance(p.value1, Error):
            return p.value1
        if isinstance(p.value2, Error):
            return p.value2
        if self.isiterable(p.value0):
            return p.value0[p.value1 : p.value2]
        else:
            return Error("TypeError", f"{self.dataTypes[type(p.value0)]} not subscriptable")

    @_('value LSQB value RSQB ASSIGN value')
    def value(self,p):
        if isinstance(p.value0, Error):
            return p.value0
        if isinstance(p.value1, Error):
            return p.value1
        if isinstance(p.value2, Error):
            return p.value2
        if self.isiterable(p.value0):
            lenght = len(p.value0)
            if p.value1 in range(-lenght, lenght):
                p.value0[p.value1] = p.value2
                return p.value0[p.value1]
            else:
                return Error("IndexError", f"{self.dataTypes[type(p.value0)]} Index out of range")
        elif isinstance(p.value0,dict):
            p.value0[p.value1] = p.value2
            return p.value0[p.value1]
        else:
            return Error("TypeError", f"{self.dataTypes[type(p.value0)]} not subscriptable")

    @_('FALSE')
    def value(self, p):
        return False
    
    @_('TRUE')
    def value(self,p):
        return True
    
    def get_DataFrame_name(self, value):
        for variable, val in self.values.items():
            if isinstance(val, pd.DataFrame) and val.equals(value):
                return variable

if __name__ == '__main__':
    lexer = SciDataVizLexer()
    parser = SciDataVizParser()
    # os.system('clear')
    while True:
        try:
            text = input('SciDataViz > ')
            if ( text == ''):
                continue
            result = parser.parse(lexer.tokenize(text))
            if not isinstance(result, type(None)):
                print(result)
        except EOFError:
            break