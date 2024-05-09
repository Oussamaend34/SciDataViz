from sly import Lexer
from error import Error

class SciDataVizLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {  
                NUMBER, ID, STRLT, TRUE, FALSE,
                PLUS, MINUS, TIMES, DIVIDE, FLRDIV, MOD, MATMUL, ASSIGN, POWER,
                LPAREN , RPAREN, LSQB, RSQB, LQB, RQB, PIPE,
                READ, QUIT, CLEAR, LS,
                GT, LT, GE, LE, EQ, NE, AND, OR, NOT
            }


    literals = { ';' , ',', ':'}

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    POWER   = r'\*\*'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    FLRDIV  = r'//'
    DIVIDE  = r'/'
    MOD     = r'%'
    MATMUL  = r'@'
    GE      = r'>='
    LE      = r'<='
    EQ      = r'=='
    GT      = r'>'
    LT      = r'<'
    NE      = r'!='
    ASSIGN  = r'(<-|=)'
    RPAREN  = r'\)'
    LPAREN  = r'\('
    LSQB    = r'\['
    RSQB    = r'\]'
    LQB     = r'{'
    RQB     = r'}'
    PIPE    = r'\|'

    @_(r"\d+\.\d*", r'\d+')
    def NUMBER(self, t):
        if ( "." in t.value):
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t
    @_(r"\".*?\"",r"\'.*?\'")
    def STRLT(self, t):
        t.value = t.value.split(t.value[0])[1]
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['quit']      =   QUIT
    ID['clear']     =   CLEAR
    ID['ls']        =   LS
    ID['read']      =   READ
    ID['True']      =   TRUE
    ID['False']     =   FALSE
    ID['and']       =   AND
    ID['or']        =   OR
    ID['not']       =   NOT

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        self.index += 1
        return Error(f"Illegal character '{t.value[0]}'", self.lineno)

if __name__ == '__main__':
    data = '''
iris["new_columns"] = iris["sepal_width"] + iris["petal_width"]
'''
    lexer = SciDataVizLexer()
    for tok in lexer.tokenize(data):
        print(tok)