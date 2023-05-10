import ply.lex as lex
import sys


palabrasReservadas = {}
identificador = {}

class MyLexer():
    # CONSTRUCTOR
    lexer = None
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)

    # DESTRUCTOR
    def __del__(self):
        print('Lexer destructor called.')

    # Palabras reservadas del lenguaje
    reserved = {
       'cierto' : 'CIERTO',
       'falso' : 'FALSO',
       'entero' : 'ENTERO',
       'real' : 'REAL',
       'finmientras' : 'FINMIENTRAS',
       'not' : 'NOT',
       'booleano' : 'BOOLEANO',
       'vector' : 'VECTOR',
       'long' : 'LONG',
       'mientras' : 'MIENTRAS',
       'si' : 'SI',
       'entonces' : 'ENTONCES',
       'sino' : 'SINO',
       'finsi' : 'FINSI',
       'and' : 'AND',
       'or' :'OR',
       'registro': 'REGISTRO',
       'funcion': 'FUNCION',
       'devolver': 'DEVOLVER',
       'caracter':'CARACTER'
    }

    # Tokens de nuestro lexico
    tokens = list(reserved.values()) + [
        'NAME', 
        'OPCOMPARE',
        'NUMINTEGER', 
        'NUMREAL',
        'FINPARRAFO',
        'CARACTERC']

    literals = ['=', '+', '-', '*', '/','(', ')', ',', '[', ']', '.', '&', '|', '!', '{','}',':',';']

    def getToken(self):
        return self.tokens


    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s' at line %d, position %d" % (t.value[0], t.lineno, t.lexpos))
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        # self.lexer.num_count = 0

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            # print(tok)

    def t_ignore_COMMENT(self, t):
        r'%.*'
        t.lexer.lineno += t.value.count("\n")

    def t_NUMREAL(self, t):
        r'\d+\.\d*([eE][+-]?\d+)?|\d+[eE][+-]?\d+'
        t.value = float(t.value)
        return t
    def t_NUMINTEGER(self, t):
        r'0[bB][01]+|0[0-7]+|0[xX][0-9a-fA-F]+|\d+'
        if t.value.startswith(('0b', '0B')):
            t.value = int(t.value[2:], 2)
        elif t.value.startswith(('0x', '0X')):
            t.value = int(t.value[2:], 16)
        elif t.value.startswith('0') and len(t.value) > 1:
            t.value = int(t.value[1:], 8)
        else:
            t.value = int(t.value)
        return t
    

    def t_CARACTERC(self,t):
        r"'[^'\\]*(?:\\.[^'\\]*)*'"

        return t

    def t_FINPARRAFO(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_OPCOMPARE(self,t):
        r'(\<\=|\>\=|\>|\<|\=\=)'
        return t

    def t_NAME(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value.lower(), 'NAME')
        if (t.type == "NAME"):
            identificador[t.value] = identificador.get(t.value, 0) + 1
        else:
            palabrasReservadas[t.value] = palabrasReservadas.get(t.value, 0) + 1
        return t

    def print_token(self, token):
        print("Token: {type} -> {value}".format(type=token.type, value=repr(token.value)))

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            self.print_token(tok)


    while True:
        if lexer==None:break
        token = lexer.token()
        if not token:break


