import ply.lex as lex
import sys


class MyLexer():
       # CONSTRUCTOR
       def __init__(self):
              print('Lexer constructor called.')
              self.lexer = lex.lex(module=self)
    # DESTRUCTOR

    def __del__(self):
        print('Lexer destructor called.')

     # variables dentro de la clase
    reserved = {
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'while': 'WHILE'
        }
        tokens = (
            'NUM', 'VAR',
        ) + list(reserved.values())
    # funciones dentro de la clase
    # todos los metodos deben tener como primer argumento “self”

    def t_error(self, t):
        print('Illegal character"%s"' % t.value[0])
        t.lexer.skip(1)

    def t_comment(self, t):
        r'\<\!\-\-'
        t.lexer.code_start = t.lexer.lexpos        # Record the starting position
        t.lexer.level = 1                          # Initial brace level
        t.lexer.begin('comment')                   # Enter 'ccode' state

    def t_comment_start(self, t):
        r'\<\!\-\-.*'
        t.lexer.level += 1

    def t_comment_end(self, t):
        r' \-\-\!\>'
        if t.lexer.level == 0:
            t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
            print(t.value)
            t.type = "CCODE"
            t.lexer.lineno += t.value.count('\n')
            t.lexer.begin('INITIAL')
            return t
