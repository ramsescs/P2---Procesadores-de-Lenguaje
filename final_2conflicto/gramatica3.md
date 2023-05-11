
<statements> ::= <statement> FINPARRAFO <statements> | lambda

<statement> ::= <asignacion> | <def_funcion>  | <condicional> | <bucle> | <declaracion> | <expresion> | lambda

<declaracion> ::= <tipo> <name_chain> '=' <expresion> | <tipo> <varios_name_chain> | <declaracion_reg> | <declaracion_vec>

<varios_name_chain> ::= <name_chain> ',' <varios_name_chain> | <name_chain>

<tipo> ::= ENTERO | REAL | BOOLEANO | CARACTER | NAME

<declaracion_reg> ::= REGISTRO NAME '{' <blq_registro> '}'

<blq_registro> ::= <declaracion> ';' <blq_registro> | <declaracion> ';' FINPARRAFO <blq_registro> | <declaracion> ';' 

<declaracion_vec> ::= VECTOR <tipo> NAME '[' NUMINTEGER ']'

<asignacion> ::= <name_chain> '=' <expresion> | <name_chain> '[' <expresion> ']' '=' <expresion>

<def_funcion> ::= FUNCION NAME '(' <lista_args> ')' ':' <tipo> '{' FINPARRAFO <statements_func> '}'

<statements_func> ::= <statements> DEVOLVER <expresion>

<lista_args> ::= <tipo> NAME ',' <lista_args> | <tipo> NAME | lambda

<lista_expresiones> ::= <expresion> ',' <lista_expresiones> | <expresion> | lambda

<expresion> ::= <expresion_and> OR <expresion> | <expresion_and> '|' <expresion> | <expresion_and>

<expresion_and> ::= <expresion_comp> '&' <expresion_and> |<expresion_comp> AND <expresion_and> | <expresion_comp>

<expresion_comp> ::= <expresion_add> OPCOMPARE <expresion_comp> | <expresion_add>

<expresion_add> ::= <expresion_mult> '+' <expresion_add> | <expresion_mult> '-' <expresion_add> | <expresion_mult> 

<expresion_mult> ::= <factor> '*' <expresion_mult> | <factor> '/' <expresion_mult> | <factor>

<factor> ::= '(' <expresion> ')' | <valor> | <name_chain> '(' <lista_expresiones> ')' | <operador_unario> <factor>

<operador_unario> ::= '-' | NOT | '!'

<valor> ::= NUMREAL | NUMINTEGER | CIERTO | FALSO | CARACTERC | <name_chain> | <name_chain> '.' LONG | <name_chain> '[' expresion ']'

<condicional> ::= SI <expresion> FINPARRAFO ENTONCES FINPARRAFO <statements> SINO FINPARRAFO <statements> FINSI | SI <expresion> FINPARRAFO ENTONCES FINPARRAFO <statements> FINSI

<bucle> ::= MIENTRAS <expresion> <statements> FINMIENTRAS 

<name_chain> ::= NAME | <name_chain> '.' NAME 