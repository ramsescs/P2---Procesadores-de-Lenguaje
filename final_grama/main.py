import sys
from MyLexer import MyLexer
sys.path.insert(0, "../..")
from MySyntax2 import MySyntax
import ply.yacc as yacc

fname="input3.txt"
f= open(fname, 'r')
s = f.read()
MySyntax(s)

"""myLex = MyLexer()
lexer = myLex.lexer
lexer.input(f.read())
myLex.test(s)
"""