from MyLexer import MyLexer
#from myLexer import tokens
 # Build the lexer and try it out
import ply.yacc as yacc

class MySyntax(object):
    m = MyLexer()
    tokens = m.tokens
    registrosTemporales = []
    tablaSimbolos = {}
    tipo = ""

    def __init__(self, input):
        print("Construyendo MySyntax")
        yacc.yacc(module=self)
        yacc.parse(input)

    def p_statements(self, p):
        '''statements : statement FINPARRAFO statements
                      |'''
        # Agrega la acción semántica aquí

    def p_statement(self, p):
        '''statement : asignacion
                     | def_funcion
                     | condicional
                     | bucle
                     | declaracion
                     | expresion
                     | '''
        # Agrega la acción semántica aquí

    def p_declaracion(self, p):
        '''declaracion : tipo name_chain '=' expresion
                       | tipo varios_name_chain
                       | declaracion_reg
                       | declaracion_vec'''
        # Agrega la acción semántica aquí

    def p_varios_name_chain(self, p):
        '''varios_name_chain : name_chain ',' varios_name_chain
                       | name_chain '''
        # Agrega la acción semántica aquí

    def p_tipo(self, p):
        '''tipo : ENTERO
                | REAL
                | BOOLEANO
                | CARACTER
                | NAME'''
        # Agrega la acción semántica aquí

    def p_declaracion_reg(self, p):
        '''declaracion_reg : REGISTRO NAME '{' blq_registro '}' '''
        # Agrega la acción semántica aquí

    def p_blq_registro(self, p):
        '''blq_registro : declaracion ';' blq_registro
                        | declaracion ';' FINPARRAFO blq_registro
                        | declaracion ';' '''
        # Agrega la acción semántica aquí


    def p_declaracion_vec(self, p):
        '''declaracion_vec : VECTOR tipo NAME '[' NUMINTEGER ']' '''
        # Agrega la acción semántica aquí

    def p_asignacion(self, p):
        '''asignacion : name_chain '=' expresion
                      | name_chain '[' expresion ']' '=' expresion'''
        # Agrega la acción semántica aquí

    def p_def_funcion(self, p):
        '''def_funcion : FUNCION NAME '(' lista_args ')' ':' tipo  '{' FINPARRAFO statements_func  '}'  '''
        # Agrega la acción semántica aquí

    def p_statements_func(self, p):
        '''statements_func : statements DEVOLVER expresion'''
        # Agrega la acción semántica aquí

    def p_lista_args(self, p):
        '''lista_args : tipo NAME ',' lista_args
                      | tipo NAME
                      |'''
        # Agrega la acción semántica aquí


    def p_lista_expresiones(self, p):
        '''lista_expresiones : expresion ',' lista_expresiones
                             | expresion
                             |'''
        # Agrega la acción semántica aquí

    def p_expresion(self, p):
        '''expresion : expresion_and OR expresion
                     | expresion_and '|' expresion
                     | expresion_and'''
        # Agrega la acción semántica aquí

    def p_expresion_and(self, p):
        '''expresion_and : expresion_comp AND expresion_and
                         | expresion_comp '&' expresion_and
                         | expresion_comp'''
        # Agrega la acción semántica aquí

    def p_expresion_comp(self, p):
        '''expresion_comp : expresion_add OPCOMPARE expresion_comp
                          | expresion_add'''
        # Agrega la acción semántica aquí

    def p_expresion_add(self, p):
        '''expresion_add : expresion_mult '+' expresion_add
                         | expresion_mult '-' expresion_add
                         | expresion_mult'''
        # Agrega la acción semántica aquí

    def p_expresion_mult(self, p):
        '''expresion_mult : factor '*' expresion_mult
                          | factor '/' expresion_mult
                          | factor'''
        # Agrega la acción semántica aquí

    def p_factor(self, p):
        '''factor : '(' expresion ')'
                  | valor
                  | name_chain '(' lista_expresiones ')'
                  | operador_unario factor
                  '''
        # Agrega la acción semántica aquí

    def p_operador_unario(self, p):
        '''operador_unario : '-'
                           | NOT
                           | '!'
                           '''
        # Agrega la acción semántica aquí

    def p_valor(self, p):
        '''valor : NUMREAL
                 | NUMINTEGER
                 | CIERTO
                 | FALSO
                 | CARACTERC
                 | name_chain
                 | name_chain '.' LONG
                 | name_chain '[' expresion ']' '''
        # Agrega la acción semántica aquí

    def p_condicional(self, p):
        '''condicional : SI expresion FINPARRAFO ENTONCES FINPARRAFO statements SINO FINPARRAFO statements  FINSI
                    | SI expresion FINPARRAFO ENTONCES FINPARRAFO statements FINSI'''
        # Agrega la acción semántica aquí


    def p_bucle(self, p):
        '''bucle : MIENTRAS expresion statements FINMIENTRAS
        '''
        # Agrega la acción semántica aquí

    def p_(self, p):
        '''name_chain : NAME
                    | name_chain '.' NAME'''
        # Agrega la acción semántica aquí

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")




