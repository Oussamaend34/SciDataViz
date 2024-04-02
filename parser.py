from sly import Parser
from lexer import CalcLexer
import numpy as np
import os
import sys
import pickle


class TypError(Exception):
    pass

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    precedence = (
        ('left', ASSIGN),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
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


    @_('term DIVIDE factor')
    def term(self, p):
        if self.areDigits(p.term, p.factor):
            return p.term / p.factor
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
        if(type(p.value) == list):
            self.values[p.ID] = np.array(p.value)
        else:
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
        return p.elements
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

    @_('LPAREN empty RPAREN')
    def vector(self, p):
        return tuple([])
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
        

    @_('ID vector')
    def func(self, p):
        print(p.ID,": ", type(p.ID), p.vector, ":", type(p.vector))
        return None
    @_('func')
    def statement(self, p):
        return None
    @_('WRITE vector')
    def statement(self,p):
        for i in p.vector:
            print(i, end=" ")
        print()
        return None
    @_('READ')
    def value(self,p):
        return input()

    @_('TYPE LPAREN value RPAREN')
    def value(self, p):
        return self.dataTypes[type(p.value)]
    @_('INTEGER LPAREN value RPAREN')
    def value(self, p):
        return int(p.value)
    @_('FLOAT LPAREN value RPAREN')
    def value(self, p):
        return float(p.value)
    @_('STRING LPAREN value RPAREN')
    def value(self, p):
        return str(p.value)
    @_('VECTOR LPAREN value RPAREN')
    def value(self, p):
        return tuple(p.value)
    @_('ARRAY LPAREN value RPAREN')
    def value(self, p):
        return np.array(p.value)

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

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