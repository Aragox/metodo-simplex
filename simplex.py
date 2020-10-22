#!/usr/bin/python3

import sys
from prettytable import PrettyTable
from fractions import Fraction
from decimal import Decimal
import copy 

pt = None # Matriz de salida con formato PrettyTable
salida = None # Archivo de salida

var_entrante = "" # Datos para archivo de salida
var_saliente = ""
numero_pivot = None
cont_estado = 0
tipo_solucion = ""

metodo = "Simplex"
optimizacion = ""
matriz = [] # Guarda los números de la tabla actual
nombre_columnas = [] # Guarda los nombres de las columnas de la tabla actual
nombre_filas = [] # Guarda los nombres de las filas de la tabla actual
pos_pivote = [0,0] # Guarda la posición de la fila pivote y la columna pivote
funcion_objetivo = [] # Guarda las variables de la función objetivo inicial/original
variables_problema = 0
M = 1000 # Valor de M en el método de la M

###########################################################################################################
#----------------------------------------------------------------------------------------------------------
#   Clase Fracción y métodos
#   Se usó de referencia la clase "Fraction" implementada por msarialp en https://gist.github.com/mustaa/2350807
#----------------------------------------------------------------------------------------------------------
##########################################################################################################
def gcd(num, denom):
#Función que retorna el máximo común divisor
    if (num == 0 or denom == 0):
        return 1
    
    while num != denom:
        if num > denom:
            num = num - denom
        else:
            denom = denom - num
    return num

class Fraccion:
#Clase Fracción
    def __init__(self, num, denom):
        # Constructor, recibe el numerador y denominador, para luego simplificar la fracción
        self.simplificar(num, denom)
        
    def simplificar(self, num, denom):
        # Función que simplifica la fracción usando el máximo común divisor. Asigna los nuevos valores al numerador y denominador
        self.num = int(num / gcd(abs(num), abs(denom)))
        self.denom = int(denom / gcd(abs(num), abs(denom)))
        if self.denom < 0:
            self.denom = abs(self.denom)
            self.num = -1*self.num
        elif self.denom == 0:
            raise ZeroDivisionError
        elif self.num == 0:
            self.denom = 1
            
    def simplificar_nomod(self, num, denom):
        # Función que simplifica la fracción (sin modificar al asignar) usando el máximo común divisor.
        #Retorna los nuevos valores al numerador y denominador en una tupla
        num1 = int(num / gcd(abs(num), abs(denom))) # Simplificar numerador y denominador
        denom1 = int(denom / gcd(abs(num), abs(denom)))
        if denom1 < 0: # Posibles cambios de signo de numerador y denominador
            denom1 = abs(denom1)
            num1 = -1*num1
        elif denom1 == 0: # Se indefine la fracción
            raise ZeroDivisionError
        elif num1 == 0:
            denom1 = 1
        return num1, denom1 # Retornar tupla
        
    def sum(self, other):
        # Función que suma 2 fracciones. Actualiza el resultado en la fracción izquierda 
        num = self.num*other.denom + self.denom*other.num
        denom = self.denom*other.denom
        self.simplificar(num, denom)
    
    def sub(self, other):
        # Función que resta 2 fracciones. Actualiza el resultado en la fracción izquierda
        num = self.num*other.denom - self.denom*other.num
        denom = self.denom*other.denom
        self.simplificar(num, denom)

    def sub_nomod(self, other):
        # Función que resta 2 fracciones. No realiza modificaciones a la fracción izquierda. Retorna una tupla [numerador,denominador] simplificados
        num = self.num*other.denom - self.denom*other.num # Guardar resultado de la resta
        denom = self.denom*other.denom
        return self.simplificar_nomod(num, denom) # Retornar tupla
    
    def mul(self, other):
        # Función que multiplica 2 fracciones. Actualiza el resultado en la fracción izquierda
        num = self.num*other.num
        denom = self.denom*other.denom
        self.simplificar(num, denom)
    
    def div(self, other):
        # Función que divide 2 fracciones. Actualiza el resultado en la fracción izquierda
        num = self.num*other.denom
        denom = self.denom*other.num
        self.simplificar(num, denom)

    def div_nomod(self, other):
        # Función que divide 2 fracciones. No realiza modificaciones a la fracción izquierda. Retorna una tupla [numerador,denominador] simplificados
        num = self.num*other.denom # Guardar resultado de la división
        denom = self.denom*other.num
        return self.simplificar_nomod(num, denom) # Retornar tupla

    def comparar(self, other):
        # Función que compara 2 fracciones para determinar cuál es mayor.
        #No realiza modificaciones. Retorna True si la fracción de la derecha es mayor, y False en caso contrario
        tupla = self.sub_nomod(other)
        numero = tupla[0]
        if (numero >= 0):
            return False
        return True

    def get_num(self):
        #Función que retorna el numerador de la fracción
        return self.num

    def get_denom(self):
        #Función que retorna el denominador de la fracción
        return self.denom    

    def __str__(self):
        # Función que retorna la fracción como un string 
        if self.denom == 1 or self.num == 0:
            return str(self.num)
        else:
            return '%s/%s' %(self.num, self.denom)

###########################################################################################################
#----------------------------------------------------------------------------------------------------------
#    Final de sección de código
#----------------------------------------------------------------------------------------------------------
###########################################################################################################

def manual():
    print("\n")    
    print("##########################################################################################################")
    print("----------------------------------------------------------------------------------------------------------")
    print("Inicio Sección Ayuda")
    print("----------------------------------------------------------------------------------------------------------")
    print("##########################################################################################################")
    print("\nEstudiante-> Ricardo Víquez Mora")
    print("\n\nDESCRIPCIÓN DEL PROGRAMA:")
    print("Este programa es una implementación del método simplex para resolver problemas de minimización y maximización")
    print("en programación lineal.")
    print("\n\nCÓMO USAR EL PROGRAMA:")
    print("FAALTAAAAA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("\n\nPARÁMETROS DE LÍNEA DE COMANDOS:")   
    print("\n    python simplex.py [-h] archivo.txt\n")     
    print("Donde:")
    print("- El parámetro 'simplex.py' es el nombre del archivo ejecutable.")
    print("- El parámetro '-h' es opcional, y muestra una descripción de como usar el programa, parámetros y formato de")
    print("archivo de entrada.")
    print("- El parámetro 'archivo.txt' es el nombre del archivo de entrada (No se debe de incluir la extensión (.txt)")
    print("en este parámetro).")
    print("\n\nFORMATO DE ARCHIVO DE ENTRADA:")
    print("La estructura del archivo de entrada consiste en elementos separados por coma y en diferentes líneas/filas")
    print("\n    método, optimización, Número de variables de decisión, Número de restricciones\n")
    print("\n    coeficientes de la función objetivo\n")
    print("\n    coeficientes de las restricciones, signo de restricción, números en la derecha de la restricción\n")
    print("Donde:")
    print("- 'método' es un valor numérico [ 0=Simplex, 1=GranM, 2=DosFases]")    
    print("- 'optimización' se indica con min o max")    
    print("\n")
    print("##########################################################################################################")
    print("----------------------------------------------------------------------------------------------------------")
    print("Final Sección Ayuda")
    print("----------------------------------------------------------------------------------------------------------")
    print("##########################################################################################################")
    print("\n")
    
def hallar_letra(letra, lst):
    # Función que retorna True si se encontró la letra en alguna de las palabras de la lista. Retorna False en caso contrario
    return any(letra in palabra for palabra in lst)
    
def inicializar_matriz():
    #Función que inicializa la matriz con ceros
    global matriz
    matriz=[] #Vaciar matriz
    
    for i in range(len(nombre_filas)): #Total de filas
        row=[] #Fila
        for j in range(len(nombre_columnas) - 1): #Total de columnas
            row.append(Fraccion(0,1)) #Añadir Fracción 0/1 para cada columna de esta fila
        matriz.append(row) #Añadir fila definida a la matriz

def operacion_fila(num_fila2, num_fila1, num):
    #Función que suma/resta/multiplica una fila (índice num_fila1) a otra fila (índice num_fila2) de la matriz global,
    #y guarda el resultado modificando la matriz global.
    #"num" es un objeto Fracccion que es multiplicado en la fila a sumar
    global matriz

    fila = copy.deepcopy(matriz[num_fila1])
    if (num_fila2 == num_fila1): # Si es la misma fila
        for j in range(len(nombre_columnas) - 1): #Total de columnas
            Fraccion.mul(matriz[num_fila2][j], num) # Multiplicar y modificar matriz
    else:
        for j in range(len(nombre_columnas) - 1): #Total de columnas
            Fraccion.mul(fila[j], num) # Multiplicar num por fila
            Fraccion.sum(matriz[num_fila2][j], fila[j]) # Sumar y modificar matriz

def cancelar_var_objetivo_con_operaciones(tipo_variable, num = 1):
    # Función que prepara la tabulación de la matriz cuando hay método de la gran M o dos fases (Con operaciones elementales de filas,
    #vuelve cero las variables especificadas en función objetivo). tipo_variable es un string que especifica el tipo de la variable de la columna
    if (hallar_letra(tipo_variable, nombre_columnas)):
        for i in range(len(nombre_filas) - 1):
            for j in range(len(nombre_columnas) - 1): #Total de columnas
                if (nombre_columnas[j+1][0] == tipo_variable and Fraccion.get_num(matriz[i+1][j]) == 1 and Fraccion.get_denom(matriz[i+1][j]) == 1):
                    if (metodo == "GranM"):
                        operacion_fila(0, i+1, Fraccion(M*-1,1))
                    elif (metodo == "DosFases"):
                        operacion_fila(0, i+1, Fraccion(num*-1,1))                            
                    break

def menor_fraccion(lst):
    #Función que retorna el objeto fracción correspondiente al valor menor de una lista de fracciones
    menor = lst[0]
    for i in range(len(lst)):
        elem = lst[i]
        if (Fraccion.comparar(elem, menor)): # Si menor actual es mayor que el elem
            menor = elem

    return menor

def menor_coeficienteObjetivo():
    #Función que retorna la posición del coeficiente mínimo de la función objetivo,
    #lo que permite obtener la posición de la columna pivote
    res = copy.deepcopy(matriz[0])
    fila = res[:len(res)-1] # No se incluye la columna LD
    f = menor_fraccion(fila)
    print("Fila")
    for i in range(len(fila)):
        print(fila[i].__str__())
    print("Menor fraccion: " + f.__str__())
    print("Posicion fraccion: " + str(buscar_fraccion(fila, f)))
    return buscar_fraccion(fila, f) # Retorno la posición de la fracción en la columna
    
def menor_cociente(num_columna):
    #Función que retorna la posición de la fila pivote que contiene el cociente mínimo
    cocientes = []
    LD = []
    res = [sub[num_columna] for sub in matriz] # Obtener la columna
    columna = res[1:len(res)] # No se incluye la fila de la función objetivo
    copiacolumna = copy.deepcopy(columna)
    cont = 0
    while (copiacolumna and cont < len(copiacolumna)): # Remover valores no válidos
        
        if (copiacolumna[cont].get_num() <= 0): # El valor es menor o igual que cero (no válido)             
           print("Objeto a eliminar....")
           print(copiacolumna[cont].get_num())
           print("Índice de objeto....")
           print(copiacolumna.index(copiacolumna[cont]))
           copiacolumna.remove(copiacolumna[cont])
           
        else:
            cont = cont + 1

    if (not copiacolumna): # Si ningún valor de la columna es válido (columna está vacía)
        return -2,-2 # U no Acotada
    
    print("\n")
    print("COLUMNA")
    for i in range(len(columna)):
        print(columna[i].__str__())
    print("\n")
    print("COPIACOLUMNA!")
    for i in range(len(copiacolumna)):
        print(copiacolumna[i].__str__())
    print("\n")
    for i in range(len(columna)):
        for j in range(len(copiacolumna)):
            if (copiacolumna and (columna[i].get_num() == copiacolumna[j].get_num()) and (columna[i].get_denom() == copiacolumna[j].get_denom())): # Asignar los cocientes usando los valores válidos disponibles
               print("LD " + str(i))
               print(matriz[i+1][len(matriz[0])-1])
               tupla = Fraccion.div_nomod(matriz[i+1][len(matriz[0])-1], columna[i]) # Sacar cociente
               f = Fraccion(tupla[0], tupla[1])
               cocientes.append(f) # Guarda cociente
               LD.append(matriz[i+1][len(matriz[0])-1])
               break
        
    valor = menor_fraccion(cocientes) # Chequear si hay cocientes mínimos duplicados
    
    print("\n")
    print("COCIENTES")
    for i in range(len(cocientes)):
        print(cocientes[i].__str__())
    print("Menor fraccion: " + valor.__str__())
    print("Posicion fraccion cocientes: " + str(buscar_fraccion(cocientes, valor)))
    
    pos = buscar_fraccion(cocientes, valor)
    tupla = Fraccion.div_nomod(LD[pos], cocientes[pos])
    f = Fraccion(tupla[0], tupla[1])
    
    print("Posicion fraccion columna: " + str(buscar_fraccion2(columna, f, cocientes[pos], LD) + 1))
    
    min_duplicados = [i for i, x in enumerate(cocientes) if (x.get_num() == valor.get_num()) and (x.get_denom() == valor.get_denom())]
    if (len(min_duplicados) >= 2):
        return buscar_fraccion2(columna, f, cocientes[pos], LD) + 1, -1 # Es solución degenerada
    else:
        return buscar_fraccion2(columna, f, cocientes[pos], LD) + 1, 1 # OK

def obtener_nuevapos():
    #Función que obtiene la nueva posición de la (fila pivote y columna pivote) en la nueva iteración del método simplex
    #Guarda la posición en una variable global (posicion_pivote)
    global tipo_solucion
    global pos_pivote
    
    pos_column = menor_coeficienteObjetivo()
    pos_fila = menor_cociente(pos_column)
    if (pos_fila[1] == -2):
        tipo_solucion = "U no Acotada"
        print("\nTIPO SOLUCIÓN: " + tipo_solucion + "\n")
        sys.exit()
    elif (pos_fila[1] == -1):
        tipo_solucion = "degenerada"
        print("\nTIPO SOLUCIÓN: " + tipo_solucion + "\n")

    pos_pivote[0] = pos_fila[0]# Actualizar la posición pivote
    pos_pivote[1] = pos_column

def hay_negativos():
    #Función que chequea si hay valores negativos en los coeficientes de la función objetivo
    #Retorna True si hay valores negativos y False en caso contrario
    solo_positivos = True
    for j in range(len(matriz[0]) - 1): # No se incluye la columna LD
        if (matriz[0][j].get_num() < 0):
            solo_positivos = False
            break

    return not solo_positivos

def buscar_fraccion(lst, f):
    #Función que retorna el índice de la posición de una fracción si la encuentra en la lista
    #En caso contrario retorna -1
    pos = -1
    for j in range(len(lst)):
        if ((lst[j].get_num() == f.get_num()) and (lst[j].get_denom() == f.get_denom())):
            pos = j
            break

    return pos

def buscar_fraccion2(lst, f, cociente, LD):
    #Función que retorna el índice de la posición de una fracción si la encuentra en la lista, y si genera el mismo cociente
    #En caso contrario retorna -1
    pos = -1
    cont = 0
    for j in range(len(lst)):
        if (lst[j].get_num() > 0): # Sólo trabajaremos con divisores positivos
            tupla = Fraccion.div_nomod(LD[cont], lst[j]) # Sacar cociente
            f = Fraccion(tupla[0], tupla[1])
            cont = cont + 1
            if ((cociente.get_num() == f.get_num()) and (cociente.get_denom() == f.get_denom())): # Si el cociente es el mismo
                pos = j
                break

    return pos

def sustituir_variable_basica():
    #Función que sustituye en la columna de VB, la variable básica saliente con la variable básica entrante
    global nombre_filas
    global var_entrante
    global var_saliente

    var_entrante = copy.deepcopy(nombre_columnas[pos_pivote[1] + 1])  # Asignar columna pivote sin asignar primera columna de nombres
    var_saliente = copy.deepcopy(nombre_filas[pos_pivote[0]]) # Asignar fila pivote sin asignar primera fila de nombres

    nombre_filas[pos_pivote[0]] = str(var_entrante)

def sustituir_funcionObjetivo():
    # Función que coloca la función objetivo original de vuelta en su lugar en la matriz
    global matriz
    
    for j in range(len(funcion_objetivo)):
        matriz[0][j] = funcion_objetivo[j]

def eliminar_columnas_artificiales():
    # Función que elimina las columnas de variables artificiales de la matriz y de nombre_columnas
    global matriz
    global nombre_columnas

    cont = 0    
    while (hallar_letra("a", nombre_columnas) and len(nombre_columnas) > 2 + variables_problema):
        if (nombre_columnas[cont+1][0] == "a"):
            del nombre_columnas[cont+1]
            for c in matriz:
                del c[cont]
        else:
            cont = cont + 1
    

def imprimir_estado(valor):
    # Función que imprime en la salida el estado de la tabla
    salida.write("\n")
    if (valor == 0): # Estado normal
        salida.write("Estado " + str(cont_estado) + "\n")
        salida.write("VB entrante: " + str(var_entrante[1:]) + ", " + "VB saliente: " + str(var_saliente[1:]) + ", " + "Número Pivot: " + str(numero_pivot) + "\n")
    elif (valor == 1): # Estado inicial
        salida.write("Estado " + str(cont_estado) + "\n")         
    elif (valor == 2): # Estado final
        salida.write("Estado " + "Final" + "\n")
        salida.write("VB entrante: " + str(var_entrante[1:]) + ", " + "VB saliente: " + str(var_saliente[1:]) + ", " + "Número Pivot: " + str(numero_pivot) + "\n")
        salida.write("Respuesta Final: U=" + str(26) + ", " + "(RA)" + "\n")   
        
    actualizar_prettytable()
    salida.write(str(pt))
    salida.write("\n")

def ejecutar_iteraciones():
    #Función que ejecuta las iteraciones del método simplex
    global numero_pivot
    global cont_estado

    while (hay_negativos() and cont_estado < 7):
        cont_estado = cont_estado + 1
        print("#####################################################")
        print("ESTADO: "+str(cont_estado))
        print("#####################################################")
        obtener_nuevapos()
        print("POS_PIVOTE: "+str(pos_pivote))
        print("#---------------------------------------------------#")
        numero_pivot = Fraccion(matriz[pos_pivote[0]][pos_pivote[1]].get_num(), matriz[pos_pivote[0]][pos_pivote[1]].get_denom())
        sustituir_variable_basica()
        operacion_fila(pos_pivote[0], pos_pivote[0], Fraccion(matriz[pos_pivote[0]][pos_pivote[1]].get_denom(), matriz[pos_pivote[0]][pos_pivote[1]].get_num()))

        for i in range(len(nombre_filas)):
            if (i != pos_pivote[0] and matriz[i][pos_pivote[1]] != 0):
                operacion_fila(i, pos_pivote[0], Fraccion(matriz[i][pos_pivote[1]].get_num()*-1,matriz[i][pos_pivote[1]].get_denom()))
                
        imprimir_estado(0)
        
    imprimir_estado(2)
    
    
def actualizar_metodo(lst, cantidad_variables):
    #Función que actualiza el método para resolver el problema. Se basa en los simbolos de desigualdades del archivo de entrada.
    #Si sólo hay "<=" se usa el método simplex, pero si hay algún "=" o ">=" se usa el método de la gran M
    #(a menos que se haya especificado el método de las 2 fases)
    global metodo
    
    columna = [sub[cantidad_variables] for sub in lst] # Obtener la columna

    cambio = False # Registra si hubo un cambio en el método
    for i in range(len(lst)): # Determinar si cambiar el método a GranM
        
        if ((columna[i] == "=" or columna[i] == ">=") and metodo == "Simplex"):
            metodo = "GranM" # Cambiar el método a GranM
            cambio = True
            break
        
    if (not cambio and metodo != "Simplex"):
        todos_menoresoiguales = True
        for i in range(len(lst)): # Determinar si cambiar el método a Simplex
            
            if (columna[i] != "<="): 
                todos_menoresoiguales = False
                break
            
        if (todos_menoresoiguales):
            metodo = "Simplex" # Cambiar el método a Simplex
            cambio = True

    if (cambio):
        print("El método se sustituye por: " + str(metodo) + "\n")
        
    else:
        print("El método se mantiene sin cambios\n")

def actualizar_prettytable():
    # Función que actualiza la matriz de salida con los datos actuales de la matriz global
    global pt

    nom_filas_salida = copy.deepcopy(nombre_filas)
    nom_columnas_salida = copy.deepcopy(nombre_columnas)
    for i in range(len(nombre_filas)-1): # Quitar etiquetas a los nombres de las filas
        nom_filas_salida[i+1] = nom_filas_salida[i+1][1:]
        
    for j in range(len(nombre_columnas)-2): # Quitar etiquetas a los nombres de las columnas
        nom_columnas_salida[j+1] = nom_columnas_salida[j+1][1:]
        
    pt = PrettyTable(nom_columnas_salida) # Asignar nombres de columnas al prettytable
    pt.align["VB"] = "l" 
    pt.padding_width = 3
    pt.padding_height = 2
        
    matriz_salida = copy.deepcopy(matriz)
    for i in range(len(matriz)): # Pasar todos las fracciones de matriz a string
        for j in range(len(matriz[0])):
            if (isinstance(matriz_salida[i][j], Fraccion)):
                matriz_salida[i][j] = Fraccion.__str__(matriz_salida[i][j])
            else:
                matriz_salida[i][j] = "NF"
                
    filas_completas = []
    filas = []
    for i in range(len(nombre_filas)): # Asignar filas de números al prettytable, junto con sus nombres de fila
        filas = [nom_filas_salida[i]] + matriz_salida[i]
        filas_completas.append(filas)
        pt.add_row(filas_completas[i])    
    
def main():
    
    global matriz # Para trabajar con variables globales
    global nombre_filas
    global nombre_columnas
    global funcion_objetivo
    global metodo
    global optimizacion
    global variables_problema
    global salida
    
    arg_valido = True 

    if (len(sys.argv) == 3): #Si el número de argumentos es igual a 3
        arg_valido = False # No se intentará resolver el problema del archivo
        
        if (not(isinstance(sys.argv[1], str) and isinstance(sys.argv[2], str))): #Chequear tipos de argumento de línea de comandos
            print("Tipo equivocado de argumentos (Se requiere: string string string)")

        if (sys.argv[1] != "-h"): #De estar presente, ejecutar argumento -h
            print("Argumento #2 debe ser '-h'")
            
        else:
            manual()

    if (len(sys.argv) == 2): #Si el número de argumentos es igual a 2
    
        if (not(isinstance(sys.argv[1], str))):
            print("Tipo equivocado de argumentos (Se requiere: string string)") #Chequear tipos de argumento de línea de comandos
            arg_valido = False # Tipos equivocados

    if (len(sys.argv) > 3 or len(sys.argv) < 2):    
        print("Número equivocado de argumentos (se requieren 2 o 3)")
        arg_valido = False # Número equivocado de argumentos
    
        if (len(sys.argv) == 1): # Si no se agregaron argumentos además del nombre del programa
            print("Sólo se recibió el nombre del programa")
    
    if (arg_valido): #El número y tipo de los argumentos es válido
        entrada = open(sys.argv[1],"r")        
        lineas = entrada.readlines() # Obtiene todas las líneas del archivo de entrada        
        entrada.close() # Cerrar archivo de entrada
        
        for i in range(len(lineas)): # Quitar comillas de las lineas
            lineas[i] = lineas[i].split(',')
            
        variables_problema = int(lineas[0][2]) # Obtener el número de las variables del problema

        num_metodo = int(lineas[0][0]) # Obtener tipo de método
        if (num_metodo == 0):
            metodo = "Simplex"
        elif (num_metodo == 1):
            metodo = "GranM"
        elif (num_metodo == 2):
            metodo = "DosFases"
            
        optimizacion = str(lineas[0][1]) # Obtener tipo de optimización
        
        for j in range(len(lineas[1])): # Obtener la lista de las variables iniciales de la función objetivo
            f = Fraction(Decimal(str(lineas[1][j]).rstrip("\n")))
            num = f.numerator
            denom = f.denominator
            if (optimizacion == "max"):
                funcion_objetivo.append(Fraccion(int(num) * -1,int(denom))) # Hay maximización
            else:
                funcion_objetivo.append(Fraccion(int(num),int(denom))) # Se pasó de minimización a maximización                           
        print("Función objetivo: " + str(funcion_objetivo))    

        actualizar_metodo(lineas[2:], int(lineas[0][2])) # Asignar el método adecuado para el problema del archivo de entrada
            
        cont_var_artificial = 0
        cont_var_exceso = 0
        nombre_columnas = ["VB"] # Colocar etiquetas a los nombres de las columnas

        for j in range(int(lineas[0][2])):
            nombre_columnas.append("n" + "x" + str(j+1)) # Variable normal
            
        for i in range(int(lineas[0][3])):
                
            if (lineas[i+2][int(lineas[0][2])] == "="):
                nombre_columnas.append("a" + "R" + str(cont_var_artificial+1)) # Variable artificial
                cont_var_artificial = cont_var_artificial + 1
                   
            elif (lineas[i+2][int(lineas[0][2])] == ">="):
                 nombre_columnas.append("e" + "x" + str(i+1+int(lineas[0][2]))) # Variable de exceso
                 nombre_columnas.append("a" + "R" + str(cont_var_artificial+1)) # Variable artificial
                 cont_var_exceso = cont_var_exceso + 1
                 cont_var_artificial = cont_var_artificial + 1
                    
            else:
                 nombre_columnas.append("h" + "x" + str(i+1+int(lineas[0][2]))) # Variable de holgura
                
        nombre_columnas.append("LD")
        print(nombre_columnas)
        
        nombre_filas = ["U"] # Obtener el nombre de cada fila (variables básicas)
        for i in range(int(lineas[0][3]) + cont_var_exceso):
            
            if (nombre_columnas[i+1+int(lineas[0][2])][0] != "e" and nombre_columnas[i+1+int(lineas[0][2])][0] != "n"): # No agregar variables de exceso ni las normales como variables básicas
                nombre_filas.append(nombre_columnas[i+1+int(lineas[0][2])])
                
        print(nombre_filas)

        inicializar_matriz() #inicializar matriz con ceros

        agrega_var_exceso = 0 # Cuenta la cantidad de veces que se añadió una variable de exceso seguido de una variable artificial en misma fila
        for i in range(len(nombre_filas)):  # Asignar números a matriz
            for j in range(len(nombre_columnas) - 1):
                
                if (j >= int(lineas[0][2]) and j < len(nombre_columnas) - 2):  # Asignar variables no básicas en restricciones
                    
                    if (j+1 == i + int(lineas[0][2]) + agrega_var_exceso and nombre_columnas[j+1][0] == "h"): # Asignar variables de holgura
                         matriz[i][j] = Fraccion(1,1)

                    elif (j+1 == i + int(lineas[0][2]) + agrega_var_exceso and nombre_columnas[j+1][0] == "e"): # Asignar variable de exceso junto con su variable artificial
                         matriz[i][j] = Fraccion(-1,1)
                         matriz[i][j+1] = Fraccion(1,1)
                         agrega_var_exceso = agrega_var_exceso + 1
                         
                    elif (nombre_columnas[j+1][0] == "a"): # Asignar variables artificiales
                         
                          if (i == 0):
                              if (metodo == "GranM"): # Método de la gran M
                                  matriz[i][j] = Fraccion(M,1)
                              elif (metodo == "DosFases"): # Método de las dos fases
                                  if (optimizacion == "max"):
                                      matriz[i][j] = Fraccion(-1,1) # Hay maximización
                                  else:
                                      matriz[i][j] = Fraccion(1,1) # Se pasó de minimización a maximización
                              
                          elif (j+1 == i + int(lineas[0][2]) + agrega_var_exceso):
                               matriz[i][j] = Fraccion(1,1)                        
                        
                elif (j < int(lineas[0][2]) and i == 0): # Asignar variables básicas en función objetivo
                    f = Fraction(Decimal(str(lineas[i+1][j]).rstrip("\n")))
                    num = f.numerator
                    denom = f.denominator
                    if (optimizacion == "max"):
                        matriz[i][j] = Fraccion(int(num) * -1,int(denom)) # Hay maximización
                    else:
                        matriz[i][j] = Fraccion(int(num),int(denom)) # Se pasó de minimización a maximización
                      
                elif (j < int(lineas[0][2])):  # Asignar variables básicas en restricciones
                     f = Fraction(Decimal(str(lineas[i+1][j]).rstrip("\n")))
                     num = f.numerator
                     denom = f.denominator                        
                     matriz[i][j] = Fraccion(int(num),int(denom)) 
                     
            if (i != 0): # Asignar LD a las restricciones
                f = Fraction(Decimal(str(lineas[i+1][len(lineas[i+1])-1]).rstrip("\n")))
                num = f.numerator
                denom = f.denominator 
                matriz[i][len(matriz[0])-1] = Fraccion(int(num),int(denom))
    
        #Escribir resultado en archivo de salida
        salida = open('ver.txt', 'w')
        
        imprimir_estado(1)

        if (metodo == "DosFases"): # Asignar cero todas las variables que no sean artificiales en función objetivo
            for j in range(len(nombre_columnas) - 1): #Total de columnas
                if (nombre_columnas[j+1][0] != "a"):
                    matriz[0][j] = Fraccion(0,1)
                    
        cancelar_var_objetivo_con_operaciones("a") # Preparar tabla si hay método GranM o de dos fases
                    
        imprimir_estado(1)

        if (metodo != "DosFases"):
            ejecutar_iteraciones()
        else:
            salida.write("\n" + "FASE1" + "\n")
            ejecutar_iteraciones()
            salida.write("\n" + "FASE2" + "\n")
            eliminar_columnas_artificiales()
            sustituir_funcionObjetivo()           
            cancelar_var_objetivo_con_operaciones("n") # Con operaciones elementales de filas, volver cero las variables sustituidas en función objetivo 
            ejecutar_iteraciones()

    #Imprimir datos de línea de comandos
    n = len(sys.argv) 
    print("Total de argumentos pasados:", n) 
  
    print("\nArgumentos pasados:", end = " ") 
    for i in range(0, n): 
        print(sys.argv[i], end = " ")
    print("\n")


if __name__ == "__main__":
    main()
