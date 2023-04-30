"""import sys
sys.path.insert(0, "../..")
from myLexer import MyLexer
# create objects MY LEXER and MY PARSER
myLex = MyLexer()
lexer=myLex.lexer

fname="input3.txt"
try:
    f = open(fname, 'r')
except IOError:
    print ("Archivo no encontrado:", fname)
s = f.read()
lexer.input(s)
file = open("result.txt", 'w')
file.close()

myLex.test(s)"""
from myLexer import MyLexer


numInt =[]
numRe = []
carater =[]
ids = []
operadores = []
separadores = []
asignacion = []
palabrasReservadas = []
saltoLinea = 0

fname = "input3.txt"

try:
    f = open(fname, 'r')
except IOError:
    print("Archivo no encontrado:", fname)

myLex = MyLexer()
lexer = myLex.lexer
lexer.input(f.read())
n_caracteres = 0

while True:
    tok = lexer.token()
    if not tok:
        break

    if tok.type == "NAME":
        ids.append(tok.value)
    elif tok.type in MyLexer.reserved.values():
        palabrasReservadas.append(tok.value)
    elif tok.type =="NUMINTEGER":
        numInt.append(tok.value)
    elif tok.type == "NUMREAL":
        numRe.append(tok.value)
    elif tok.type == "CARACTERC":
        carater.append(tok.value)
    elif tok.type == "OPCOMPARE":
        operadores.append(tok.value)
    elif tok.type == "FINPARRAFO":
        saltoLinea += 1

    num = str(tok.value)
    n_caracteres += len(num)

print("NUMERO DE LINEAS: ", lexer.lineno)
print("SALTOS DE LINEA : ", saltoLinea)
print("NUMERO DE CARACTERES Y DIGITOS: ", n_caracteres)
print("NUMERO DE ESPACIOS Y SALTOS DE LINEA: ", len(lexer.lexdata) - n_caracteres)

print()

if not len(operadores) == 0:
    print("OPERADORES:")
    print(', '.join(operadores))
    print()


if not len(numRe) == 0:
    print("NÚMEROS REALES:")
    cons_new = [str(a) for a in numRe]
    print(', '.join(cons_new))
    print()

if not len(numInt) == 0:
    print("NUMEROS NATURALES:")
    cons_new = [str(a) for a in numInt]
    print(', '.join(cons_new))
    print()

if not len(carater) == 0:
    print("CARACTERES:")
    cons_new = [str(a) for a in carater]
    print(', '.join(cons_new))
    print()

if not len(palabrasReservadas) == 0:
    print("PALABRAS RESERVADAS:")
    print(', '.join(palabrasReservadas))
    print()

if not len(ids) == 0:
    print("IDENTIFICADORES")
    print(', '.join(ids))
    print()


