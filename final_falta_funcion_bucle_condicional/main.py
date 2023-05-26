import sys
import os
from MyLexer import MyLexer
sys.path.insert(0, "../..")
from MySyntax import MySyntax
import ply.yacc as yacc
import json

fname="./pruebas/correcto-test_7_funcion"
f= open(fname, 'r')
s = f.read()
p = MySyntax(s)

json_dict = {}
for var in p.variables.keys():
    json_dict[var] = {'tipo': p.variables[var]['tipo']}

    if not (p.haveControlFlow() or p.haveFunctions()):
        json_dict[var]['valor'] = p.variables[var]['valor']

fname = 'output.json'

with open(fname, 'w') as file:
    # Write the dictionary as JSON to the file
    json.dump(json_dict, file)


"""
myLex = MyLexer()
lexer = myLex.lexer
lexer.input(f.read())
myLex.test(s)
"""