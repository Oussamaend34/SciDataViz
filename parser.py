from sly import Parser
from lexer import CalcLexer
from func import BuitInFunc
import numpy as np
import os
import sys
import pickle


class TypError(Exception):
    pass

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    precedence = (
        ('nonassoc', ASSIGN),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE, MOD, FLRDIV),
        ('right', UMINUS),
    )
    debugfile = 'debug.txt'
    tokens = CalcLexer.tokens

    def __init__(self) -> None:
        self.values = {}
        with open('primitiveDataTypes.pickle', 'rb') as f:
            self.dataTypes = pickle.load(f)

    # Grammar rules and actions
    @_('statements')
    def s(self, p):
        return p.statements
    @_('statement')
    def statements(self, p):
        return p.statement
    @_('statement ";" statements')
    def statements(self, p):
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
        return p.value + p.term

    @_('value MINUS term')
    def value(self, p):
        if self.areDigits(p.value, p.term):
            return p.value - p.term
        return TypeError("Must be from the same type")

    @_('MINUS factor %prec UMINUS')
    def factor(self, p):
        return -p.factor
    @_('term')
    def value(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        if self.areDigits(p.term, p.factor):
            return p.term * p.factor
        return TypeError("Must be from the same type")

    @_('term MATMUL factor')
    def term(self, p):
        if isinstance(p.term, np.ndarray) and isinstance(p.factor, np.ndarray):
            try:
                return np.matmul(p.term, p.factor)
            except ValueError:
                print("you can't do this multiplication")
                return None
        else:
            print('You can only do matrix maltiplication between two arrays')
            return None

    @_('term MOD factor')
    def term(self, p):
        if self.areDigits(p.term, p.factor):
            return p.term % p.factor
        return TypeError("Must between two numbers")

    @_('term DIVIDE factor')
    def term(self, p):
        if self.areDigits(p.term, p.factor):
            return p.term / p.factor
        return TypeError("Must be from the same type")

    @_('term FLRDIV factor')
    def term(self, p):
        if self.areDigits(p.term, p.factor):
            return p.term // p.factor
        return TypeError("Must be from the same type")

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
        self.values[p.ID] = p.value
        return p.value
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
        os.system('clear')
        return None
    @_('LS')
    def statement(self, p):
        print(self.values)
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
            print(f"variable {index} have no value")
            return None
    def areDigits(self, value1, value2):
        if(type(value1) in [float, int] and type(value2) in [float, int]):
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
        f = BuitInFunc(p.ID,p.vector)
        return f
    
    @_('func')
    def factor(self, p):
        return p.func.exec()
    @_('READ')
    def value(self,p):
        return input()
    
    @_('value PIPE func')
    def value(self, p):
        p.func.addArgument(p.value)
        return p.func.exec()
    
    @_('json')
    def value(self, p):
        return p.json
    @_('LQB members RQB')
    def json(self, p):
        return {key: value for key, value in p.members}

    @_('pair')
    def members(self, p):
        return [p.pair]

    @_('pair "," members')
    def members(self, p):
        return [p.pair] + p.members
    
    @_('value ":" value')
    def pair(self, p):
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
        if self.isiterable(p.value0):
            lenght = len(self.value0)
            if p.value1 in range(-lenght, lenght):
                return p.value0[p.value1]
            else:
                print(f"IndexError: {self.dataTypes[type(p.value0)]} Index out of range")
        elif isinstance(p.value0,dict):
            if p.value1 in p.value0:
                return p.value0[p.value1]
            else:
                print(f"KeyError: {p.value1}")
        else:
            print(f"TypeError: {self.dataTypes[type(p.value0)]} not subscriptable")
    
    @_('value LSQB value ":" value RSQB')
    def value(self,p):
        if self.isiterable(p.value0):
            return p.value0[p.value1 : p.value2]
        else:
            print(f"TypeError: {self.dataTypes[type(p.value0)]} not subscriptable")

    @_('value LSQB value RSQB ASSIGN value')
    def value(self,p):
        if self.isiterable(p.value0):
            lenght = len(p.value0)
            if p.value1 in range(-lenght, lenght):
                p.value0[p.value1] = p.value2
                return p.value0[p.value1]
            else:
                print(f"IndexError: {self.dataTypes[type(p.value0)]} Index out of range")
        elif isinstance(p.value0,dict):
            p.value0[p.value1] = p.value2
            return p.value0[p.value1]
        else:
            print(f"TypeError: {self.dataTypes[type(p.value0)]} not subscriptable")

    @_('FALSE')
    def value(self, p):
        return False
    
    @_('TRUE')
    def value(self,p):
        return True

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
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