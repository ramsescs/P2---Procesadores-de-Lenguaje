from re import T
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

 # Palabras claves reservadas
    reserved = {
        'true' : 'true',
        'false' : 'false',
        'entero' : 'entero',
        'real' : 'real',
        'finmientras' : 'finmientras',
        'not' : 'not',
        'booleano' : 'booleano',
        'vector' : 'vector',
        'sino' : 'sino',
        'finsi' : 'finsi',
        'long' : 'long',
        'mientras' : 'mientras',
        'and' : 'and',
        'si' : 'si',
        'or' : 'or'
    }

 # Tokens de nuestro lexico
    tokens =list(reserved.values())+ [
       'MATRICULA','NAME','MAIL','DNI','OPERADOR','SEPARADOR','ASIGNACION','NUMBER_HEXA','NUMBER_OCTAL','NUMBER_REAL','NUMBER','ID']
 
 # Aparte del estado INITIAL creamos un estado 'iden' para cada identificador y uno 'comment' para cada comentario del tipo <!-- -->
    states = (
    ('iden','exclusive'),
    ('comment','exclusive'))

 # Definimos la entrada a nuestro estado 'comment' 
    def t_comment(self,t):
        r'\<\!\-\-'
     # Guardamos la posicion inicial donde empieza el estado   
        t.lexer.code_start = t.lexer.lexpos        
     # Indicamos que empieza el estado 'comment'
        t.lexer.begin('comment')
    
 # Tratamiento de errores del estado 'comment' (los ignoramos)
    def t_comment_error(self,t):
        t.lexer.skip(1)

 # Definicion de la salida del estado 'comment' y vuelta al inicial
    def t_comment_close(self,t):
        r'\-\-\>'
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
        t.lexer.lineno += t.value.count('\n')
       # Cambiamos al estado por defecto
        t.lexer.begin('INITIAL')  

 # Definimos la entrada a nuestro estado 'iden'
    def t_iden(self,t):
        r'\#\#'
     # Guardamos la posicion inicial donde empieza el estado
        t.lexer.code_start = t.lexer.lexpos        
     # Indicamos que empieza el estado 'iden'
        t.lexer.begin('iden')  

 # Definicion del token 'NAME' exclusivo del estado 'iden'
    def t_iden_NAME(self,t): 
        r'([A-Z][a-z]*)([ \t]+(([A-Z][a-z]*)?))*'
        return t 

 # Definicion del token 'MATRICULA' exclusivo del estado 'iden'
    def t_iden_MATRICULA(self,t):
        r'[0-9][0-9][0-9][0-9][A-Z][A-Z][A-Z]'
        return t 

 # Definicion del token 'MAIL' exclusivo del estado 'iden'
    def t_iden_MAIL(self,t):
        r'.*\@.*\.(com|es)'
        return t

 # Definicion del token 'DNI' exclusivo del estado 'iden'
    def t_iden_DNI(self,t):
        r'[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][A-Z]'
        return t

 # Tratamiento de errores del estado 'iden'
    def t_iden_error(self,t):
     # Seleccionamos todos los caracteres hasta el final de linea,
     # en nuestro caso es el resto del identificador
        i=0
        while t.value[i]!='\n':
            i+=1
     # Imprimimos como error todo el identificador en vez de cada uno de sus literales
        print("Identificador erroneo '%s'" % t.value[0:i])
     # Como hemos llegado a un fin de linea salimos del estado 'iden'
        t.lexer.lineno += t.value[0:i].count('\n')
     # Cambiamos al estado por defecto
        t.lexer.begin('INITIAL')
     # Omitimos los caracteres hasta el final de linea    
        t.lexer.skip(i)
        

 # Definicion de la salida del estado 'iden' al encontrar un salto de linea y vuelta al inicial
    def t_iden_cerrar(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
       # Cambiamos al estado por defecto
        t.lexer.begin('INITIAL')  

 # Token de reconocimiento de los literales empleados como operadores
    def t_OPERADOR(self,t):
        r'[\+\-\*\/\^\<\>\.\|]'
        return t

 # Token de reconocimiento de los literales empleados como separadores
    def t_SEPARADOR(self,t):
        r'[\(\)\[\]\;]'
        return t

 # Token de reconocimiento de los literales empleados para asignaciones
    def t_ASIGNACION(self,t):
        r'(\:)?\='
        return t

 # Token de reconocimiento de un numero entero en formato hexadecimal
    def t_NUMBER_HEXA(self,t):
        r'[0][xX][1-9a-fA-F][0-9a-fA-F]*'
        t.value = int(t.value,0) 
        return t

 # Token de reconocimiento de un numero entero en formato octal
    def t_NUMBER_OCTAL(self,t):
        r'[0][oO][1-7][0-7]+'
        t.value = int(t.value,0)
        return t

 # Token de reconocimiento de un numero real
    def t_NUMBER_REAL(self,t):
        r'(([0-9]+)?(\.[0-9][0-9]*)([e][-+]?[0-9]+)?|([0-9]+)(\.[0-9][0-9]*)?([e][-+]?[0-9]+))'
        t.value = float(t.value)
        return t

 # Token de reconocimiento de un entero decimal
    def t_NUMBER(self,t):
        r'[0-9]+'
        t.value = int(t.value)
        return t
 # Token de reconocimiento de los IDs donde antes se comprueban si son palabras reservadas
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
     # Si son palabras reservadas se antepone al tipo 'ID'
        t.type = self.reserved.get(t.value.lower(),'ID')
        return t

 # Definicion del tratamiento de errores de forma general
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

 # Reconocimiento y conteo del numero de saltos de linea
    def t_endline(self,t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        pass

 # Ignoramos las sentencias precedidas de %% en cualquier estado
    t_ANY_ignore_comment2 = r'%%.*'
 # Ignoramos los espacios en blanco en cualquier estado
    t_ANY_ignore = " \t"
    