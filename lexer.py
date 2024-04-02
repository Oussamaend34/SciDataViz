from sly import Lexer

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {  
                NUMBER, ID, STRLT,
                PLUS, MINUS, TIMES, DIVIDE, MATMUL, ASSIGN, 
                LPAREN , RPAREN, LSQB, RSQB, PIPE,
                WRITE, READ,
                QUIT, CLEAR, LS,
                TYPE, INTEGER, FLOAT, STRING, ARRAY, VECTOR
            }


    literals = { '{', '}', ';' , ','}

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    RPAREN  = r'\)'
    LPAREN  = r'\('
    LSQB    = r'\['
    RSQB    = r'\]'
    MATMUL  = r'@'
    PIPE    = r'\|'

    @_(r"\d+\.\d*", r'\d+')
    def NUMBER(self, t):
        if ( "." in t.value):
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t
    @_(r"\".*?\"",r"\'.*\'")
    def STRLT(self, t):
        t.value = t.value.split(t.value[0])[1]
        return t

    # Identifiers and keywords
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['quit']      = QUIT
    ID['clear']     = CLEAR
    ID['ls']        = LS
    ID['write']     = WRITE
    ID['read']      = READ
    ID['type']      = TYPE
    ID['float']     = FLOAT
    ID['integer']    = INTEGER
    ID['string']    = STRING 
    ID['array']      = ARRAY
    ID['vector']    = VECTOR

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':
    data = '''
"hello" + " " + "world"
'''
    lexer = CalcLexer()
    for tok in lexer.tokenize(data):
        print(tok)