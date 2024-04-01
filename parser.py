from sly import Parser
from lexer import CalcLexer
import numpy as np
import os
import sys
import time


class TypError(Exception):
    pass

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    precedence = (
        ('left', ASSIGN),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE)
        
    )
    debugfile = 'debug.txt'
    tokens = CalcLexer.tokens

    def __init__(self) -> None:
        self.values = {}

    # Grammar rules and actions
    @_('exprs')
    def statement(self, p):
        return p.exprs
    @_('expr PLUS term')
    def expr(self, p):
        return p.expr + p.term
    @_('expr')
    def exprs(self, p):
        return p.expr
    @_('expr ";" exprs')
    def exprs(self, p):
        return p.exprs
    @_('empty')
    def exprs(self, p):
        return None
    @_('')
    def empty(self, p):
        pass
    @_('expr MINUS term')
    def expr(self, p):
        if ( not isinstance(p.expr, type(p.term))):
            return TypeError("Must be from the same type")
        return p.expr - p.term
    @_('term')
    def expr(self, p):
        return p.term

    @_('term TIMES factor')
    def term(self, p):
        if ( not isinstance(p.term, type(p.factor))):
            return TypeError("Must be from the same type")
        return p.term * p.factor
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
        if ( not isinstance(p.term, type(p.term))):
            return TypeError("Must be from the same type")
        return p.term / p.factor

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER
    
    @_('STRLT')
    def factor(self, p):
        return p.STRLT

    @_('LPAREN expr RPAREN')
    def factor(self, p):
        return p.expr
    
    @_('ID ASSIGN expr')
    def exprs(self, p):
        if(type(p.expr) == list):
            self.values[p.ID] = np.array(p.expr)
        else:
            self.values[p.ID] = p.expr
        return None
    @_('ID')
    def factor(self, p):
        return self.values[p.ID]
    
    @_('array')
    def factor(self,p):
        return p.array
    
    @_('LSQB elements RSQB')
    def array(self, p):
        print('LSQB elements RSQB')
        return p.elements
    @_('value')
    def elements(self, p):
        print('value')
        return [p.value]
    @_('value "," elements')
    def elements(self, p):
        print('value "," elements')
        return [p.value] + p.elements
    @_('NUMBER')
    def value(self, p):
        print('NUMBER')
        return p.NUMBER
    @_('ID')
    def value(self, p):
        return self.values[p.ID]
    @_('array')
    def value(self, p):
        return p.array
    @_('QUIT')
    def expr(self, p):
        sys.exit()
    @_('CLEAR')
    def expr(self, p):
        os.system('clear')
        return None
    @_('LS')
    def expr(self, p):
        print(self.values)
        return None

if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            if ( text == ''):
                continue
            result = parser.parse(lexer.tokenize(text))
            if not isinstance(result, type(None)):
                print(result)
        except EOFError:
            break