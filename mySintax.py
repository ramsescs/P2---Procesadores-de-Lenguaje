# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:37:34 2022

@author: user
"""

from xmlrpc.client import boolean
from myLexer import MyLexer 
#from myLexer import tokens
 # Build the lexer and try it out
import ply.yacc as yacc 
import sys
import os
 
class MySintax(object):
    m = MyLexer()
    tokens = m.tokens 
    registrosTemporales=[0]
    cont_registro=0
    cont_lable=1
    tablaSimbolos = {}
    tipo=""
    valor_defecto={"entero":0,"booleano":False,"real":0.0}
    v_print=False
    count =0
    file=""
    isVector = False
    list_while=[]
    

    def __init__(self,input,file):
        print("Construyendo MySintax")
        self.file= file
        yacc.yacc(module=self)
        yacc.parse(input)
        
        
    
    # La línea puede empezar por la declaración de una variable y su asignación
    # También puede empezar por declarar una variable
    # En caso de que ya está declarada, procedemos a inicializar la variable.
    
    
    def p_statement_declare (self, p):
        
        '''statement : statement tipo NAME assign_statement FINPARRAFO 
                      | statement tipo NAME variosVariables FINPARRAFO 
                      | statement NAME assign_statement FINPARRAFO
                      | statement vector tipo assign_statement FINPARRAFO
                      | statement assign_statement FINPARRAFO

        '''
        self.isVector = False
        error = False


        if p[3] != None and p[2] != None and (p[2].lower() == "booleano" or p[2].lower() == "entero" or p[2].lower()=="real") and (p[1] not in self.tablaSimbolos):
            #solo declaracion
            if len(p)==6 and p[4]==None:
                self.tablaSimbolos[p[3]] = {"tipo": p[2].lower(), "valor":0} #por cambiar el valor
            else: #declarar + asignar valor
                if (type(p[4]) is str) and p[4].lower()=="true":p[4]=True
                elif (type(p[4]) is str) and p[4].lower()=="false": p[4]=False       

                if (type(p[4]) is int and p[2].lower() == "entero") or (type(p[4]) is bool and p[2].lower() == "booleano") or (type(p[4]) is float and p[2].lower() == "real"):
                    self.tablaSimbolos[p[3]] = {"tipo": p[2].lower(), "valor":p[4]}
                    
                    #if p[2] == None: self.tablaSimbolos[p[1]]["valor"]=self.valor_defecto[self.tipo.lower()]
                    
                elif(type(p[4]) is str) and self.tablaSimbolos[p[4]]["tipo"] == p[2].lower():
                    self.tablaSimbolos[p[3]] = {"tipo": p[2].lower(), "valor":p[4]}
                        #if p[2] == None: self.tablaSimbolos[p[1]]["valor"]=self.valor_defecto[self.tipo.lower()]
                else:
                    self.file.write(f"ERROR: TIPO DE VARIABLE NO COINCIDENTE")
                    error = True
                    
        
        #cuando esta declarado y se quiere una reasignacion
        elif p[2] != "vector" and len(p)>4:
            if p[2] in self.tablaSimbolos: # en caso de que no sea un vector y ya exista la variable
                
                if (type(p[3]) is str) and p[3].lower()=="true":p[3]=True
                elif (type(p[3]) is str) and p[3].lower()=="false": p[3]=False

                if (type(p[3]) is int and self.tablaSimbolos[p[2]]["tipo"].lower() == "entero") or (type(p[3]) is bool and self.tablaSimbolos[p[2]]["tipo"].lower() == "booleano") or (type(p[3]) is float and self.tablaSimbolos[p[2]]["tipo"].lower() == "real"):
                    self.tablaSimbolos[p[2]]["valor"]=p[3]
                    
                elif(type(p[3]) is str) and self.tablaSimbolos[p[2]]["tipo"] == self.tablaSimbolos[p[3]]["tipo"].lower():
                    self.tablaSimbolos[p[2]]["valor"]=p[3]     

                else:
                    self.file.write(f"ERROR: TIPO DE VARIABLE NO COINCIDENTE")
                    error = True
             
            #cuando quierese redeclarar y es de otro tipo 
            else:
                self.file.write(f"ERROR: VARIABLE NO DECLARADO O REDECLARACION DE VARIABLES")
                error = True
            
        self.tipo = ""
        self.isVector = False
            #print("p_statement_assign: ", self.tablaSimbolos)
        
        if(len(p) == 5 and p[3] != None and not error):
            self.file.write(f"( =, {p[3]}, , {p[2]})\n")
        elif len(p) == 6 and p[4] != None and not error:
            self.file.write(f"( =, {p[4]}, , {p[3]})\n")
            

    def p_vector(self, p):
        '''
        vector : VECTOR
        '''
        self.isVector = True
        p[0]=p[1].lower()
    def p_tipo(self, p):
        '''
        tipo : BOOLEANO 
              | ENTERO 
              | REAL
        '''
        p[0]=p[1]
        self.tipo = p[1]
        #self.file.write("p_tipo:"+str(p[0])+"\n")
        
          
    # La asignación consiste en asignar un valor a una variable. 
    def p_statement_assign (self,p):
    
        '''assign_statement :   assign_statement1 variosVariables
                              | NAME "[" NAME "]" restoVector
                              | NAME "[" NUMBER "]" restoVector

        '''        
       #print("p[2] ", p[2])
       #print("tipo ", self.tipo)
        error = False
        
        len_vector=-1
        #en la estructura del vector, se guardan el tipo y su tamaño.
        if len(p) == 6:
            if self.isVector and p[5] != None: self.file.write(f"ERROR: DECLARACION DE VECTORES NO SE ASIGNAN VALOR")
            elif self.isVector and p[5] == None and p[1] not in self.tablaSimbolos:
                #Cuando es declarada con un int
                if type(p[3]) is int: 
                    self.tablaSimbolos[p[1]]={"tipo":self.tipo.lower(), "valor":p[3]}
                    len_vector=p[3]
                #Cuando es declarada con una variable
                elif type(p[3]) is str and type(self.tablaSimbolos[p[3]]["valor"] is int):
                    self.tablaSimbolos[p[1]]={"tipo":self.tipo.lower(), "valor":self.tablaSimbolos[p[3]]["valor"]}
                    len_vector=self.tablaSimbolos[p[3]]["valor"]
            
            #asignacion
            else: 
                if type(p[3]) is str and type(self.tablaSimbolos[p[3]]["valor"]) is int and self.tablaSimbolos[p[3]]["valor"]<self.tablaSimbolos[p[1]]["valor"]:
                    self.file.write(f"( =, {p[5]}, , {p[1]}[{p[3]}])\n")
                elif type(p[3]) is int and p[3]<self.tablaSimbolos[p[1]]["valor"]: 
                    self.file.write(f"( =, {p[5]}, , {p[1]}[{p[3]}])\n")
                else:
                    self.file.write(f"ERROR, INDEX OF ARRAY")
            
        else:
            p[0] = p[1]
    def p_restoVectors (self,p):
        '''restoVector : assign_statement1 
                        | 
        
        '''
        if len(p)>1:
            p[0]=p[1]
            
    def p_statement_assign_varios_variables (self,p):
       '''variosVariables : "," NAME assign_statement1 variosVariables
                            | "," NAME variosVariables
                            |
       ''' 
       if len(p) == 5:
        #print("-----------p_statement_assign_varios_variables",p[3] )
        self.tablaSimbolos[p[2]] = {"tipo": self.tipo.lower(), "valor":p[3]}
        if p[3] == None: self.tablaSimbolos[p[2]]["valor"]=self.valor_defecto[self.tablaSimbolos[p[2]]["tipo"]]
       elif len(p)>1:
           self.tablaSimbolos[p[2]] = {"tipo": self.tipo.lower(), "valor":self.valor_defecto[self.tipo.lower()]}
        

    # Procedemos a asignar a una varible
    def p_statement_assign1 (self,p):
        
        '''assign_statement1 :  "=" expresion_matematica
                                | "=" condition
                                
                                    
        '''
        if len(p) != 1:
            p[0] = p[2]
        
    
    # Un statement puede dar lugar a una expresion o (una declaración o asignación de variables con las reglas anteriores).
    def p_statement_expr (self,p):
        '''statement :     statement expresion 
                            |
        '''
        """
        if len(p)>2:
            print("p_statement: ", p[2])
        """
    # Una expresion puede ser una expresion matematica, un bucle o una condición
    def p_expresion(self,p):
        ''' expresion :   expresion_matematica FINPARRAFO
                          | salto_condition 
                          | salto_bucle 
        '''
        p[0]=p[1]
        
        
        #print("p_expresion: ", p[0])
        
    # Una expresión matemática puede llevar un parentesis o no, 
    def p_expresion_matematica_con_parentesis(self,p):
        '''expresion_matematica : '(' expresion_matematica ')'
        '''
        #print("p_expresion_matematica_con_parentesis: ", p[0])
    # Una expresion_matemática puede estar compuesto por varias operaciones matemáticas serado por operadores. 
    def p_expresion_matematica(self,p):
        '''expresion_matematica :    expresion_matematica '+' expresion_matematica2
                                   | expresion_matematica '-' expresion_matematica2
                                   | expresion_matematica2
        '''
        #print("expresion_matematica: ", p[1])

        if len(p)==2:
            p[0]=p[1]
        else:
            
            #if len(registrosTemporales) < 8: ??????????
            registro = "t"+str(len(self.registrosTemporales))
            self.registrosTemporales.append(registro)
            self.file.write(f"( {p[2]}, {p[1]}, {p[3]}, {registro})\n")
            #p[0]=p[1]+p[3]
            p[0]=registro
            """
            if p[2] == '+':
                subvalor = p[1]+p[3]
            else:
                subvalor = p[1]-p[3]
            """
            if (type(p[3])) is int: subtipo="entero"
            elif (type(p[3])) is bool: subtipo="booleano"
            else: subtipo="real"
            
            self.tablaSimbolos[registro] = {"tipo": subtipo.lower()} 

                
    
    def p_expression_binop2(self,p):
        """expresion_matematica2 : expresion_matematica2 '*' valor_signo 
                      | expresion_matematica2 '/' valor_signo
                      | valor_signo
                      """
        
        if len(p) == 4: 
            registro = "t"+str(len(self.registrosTemporales))
            self.registrosTemporales.append(registro)
            self.file.write(f"( {p[2]}, {p[1]}, {p[3]}, {registro})\n") 
            p[0]=registro
            """
            if p[2] == '*':
                subvalor = p[1]*p[3]
            else:
                subvalor = p[1]/p[3]
            """
            if (type(p[3])) is int: subtipo="entero"
            elif (type(p[3])) is bool: subtipo="booleano"
            else: subtipo="real"
            
            self.tablaSimbolos[registro] = {"tipo": subtipo.lower()}            

        else:
            p[0] = p[1]               
            
    def p_expression_uminus(self,p):
        """valor_signo : '-' fin_expresion_matematica
                        | fin_expresion_matematica
                        | '+' fin_expresion_matematica
                        """
        if len(p) == 3:
            if p[1]== '-':
                p[0] = -p[2]
            elif p[1]== '+':
                p[0] = p[2]
        else:
            p[0] = p[1]
        if self.v_print : print("p_expression_uminus: ", p[0])
            
    # Cada expresion_matematica puede terminar en un number, float, scientific, hexadecimal o exponencial
    def p_expresion_matematica_fin(self,p):
        '''fin_expresion_matematica : NUMBER
                                        | FLOAT
                                        | SCIENTIFIC
                                        | HEXADECIMAL
                                        | OCTAL
                                        | NAME 
                                        | NAME "." LONG
                                        
        '''
        
        if len(p)==4:
            p[0]=self.tablaSimbolos[p[1]]["valor"]
            registro = "t"+str(len(self.registrosTemporales))
            self.registrosTemporales.append(registro)
            self.file.write(f"( =, {p[0]}, , {registro})\n")
        else: p[0]=p[1]
       

        if self.v_print : print("p_expresion_matematicac_fin: ", p[0])
        
    # una condition puede estar formada por varias condiciones serparadas por un operador lógico
    def p_condition(self,p):
        ''' condition :  condition AND fin_condition
                        | condition '&' fin_condition
                        | condition OR fin_condition
                        | condition '|' fin_condition
                        | NOT fin_condition
                        | '!' fin_condition
                        | fin_condition
        '''
        if len(p)==2:
            p[0]=p[1]
        elif len(p)==4:
            if p[2].lower() == 'and': p[2] = '&'
            if p[2].lower() == 'or': p[2] = '|'
            registro = "t"+str(len(self.registrosTemporales))
            self.registrosTemporales.append(registro)
            self.file.write(f"( {p[2]}, {p[1]}, {p[3]}, {registro})\n")
            p[0]=registro
            
            self.tablaSimbolos[registro] = {"tipo":"booleano"} 
        else:
            if p[2].lower() == 'not': p[2] = '!'
            registro = "t"+str(len(self.registrosTemporales))
            self.registrosTemporales.append(registro)
            self.file.write(f"( {p[1]}, {p[2]},  , {registro})\n")
            p[0]=registro
            self.tablaSimbolos[registro] = {"tipo":"booleano"}

    # aux sirve para indicar los elementos que pueden realizar una comparación
    def p_aux(self,p):
        ''' aux : fin_expresion_matematica  
                  | TRUE 
                  | FALSE 
                  | '(' expresion_matematica ')'
        '''
        if len(p)==2:
            p[0]=p[1]
    # una condition termina con una comparación o en una variable (si solo termina con una variable esta tiene que ser booleana) 
    def p_fin_condition(self, p):
        ''' fin_condition : aux OPECOMPARE aux
                            | TRUE
                            | FALSE
                            | '(' aux OPECOMPARE aux ')'
                            
        '''
        
        if len(p)==2:
            p[0]=p[1]
        else:
            if len(p)==4: pos=1
            if len(p)==6: pos=2
            registro = "t"+str(len(self.registrosTemporales))
            self.registrosTemporales.append(registro)
            self.file.write(f"( {p[pos+1]}, {p[pos]}, {p[pos+2]}, {registro})\n")
            p[0]=registro
            self.tablaSimbolos[registro] = {"tipo":"booleano"}
            
        
###Sección Condition
    def p_expresion_condition(self,p):
        ''' salto_condition :  SI condition print_entonces statement resto_condition
        '''
        self.count-=1
        if self.count == 0: self.file.write(f"( label, L0, , )\n")
            
    def p_expresion_resto_condition(self,p):
        ''' resto_condition :  FINSI
                             | sino_part statement FINSI
        '''       
        if len(p) == 2:
            label_local = "L"+str(self.cont_lable-1)
            self.file.write(f"( label, {label_local}, , )\n")

    def p_expresion_condition2(self,p):
        """ print_entonces : ENTONCES
        """
        self.count+=1

        label_local1 = "L"+str(self.cont_lable)
        self.cont_lable+=1
        label_local2 = "L"+str(self.cont_lable)
        self.cont_lable+=1
        
        registro = "t"+str(len(self.registrosTemporales)-1)

        self.file.write(f"( gotoc, {registro}, ,{label_local1})\n")
        self.file.write(f"( goto, {label_local2}, ,)\n")
        self.file.write(f"( label, {label_local1}, , )\n")

    def p_expresion_condition3(self,p):
        """sino_part : SINO 
        """
        self.file.write(f"(goto, L0, , )\n")
        label_local = "L"+str(self.cont_lable-1)
        self.file.write(f"( label, {label_local}, , )\n")
        
        
        


###Sección Bucle
    def p_expresion_bucle(self,p):
        ''' salto_bucle : mientras_part condition_part statement FINMIENTRAS
        '''
        
        
        self.count-=1
        self.file.write(f"( goto, {self.list_while.pop()}, , )\n")
        
        if self.count == 0: self.file.write(f"( label, L0, , )\n")

    def p_expresion_bucle2(self,p):
        """mientras_part : MIENTRAS
        """
        self.count+=1
        label_local1 = "L"+str(self.cont_lable)
        self.cont_lable+=1
        self.list_while.append(label_local1)
        self.file.write(f"( label, {label_local1}, , )\n")
        
    def p_expresion_bucle3(self,p):
        """condition_part : condition
        """
        registro = "t"+str(len(self.registrosTemporales)-1)

        self.file.write(f"( gotocf, {registro}, , L0)\n")

        
    def p_error(self,p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")