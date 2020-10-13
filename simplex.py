#!/usr/bin/python3

import sys
from prettytable import PrettyTable
import copy 

pt = None # Matriz de salida con formato PrettyTable
tipo_solucion = ""
metodo = 0
optimizacion = ""
matriz = [] # Guarda los números de la tabla actual
nombre_columnas = [] # Guarda los nombres de las columnas de la tabla actual
nombre_filas = [] # Guarda los nombres de las filas de la tabla actual
pos = []
#fila = []
#columna = []
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
        num = int(num / gcd(abs(num), abs(denom))) # Simplificar numerador y denominador
        denom = int(denom / gcd(abs(num), abs(denom)))
        if denom < 0: # Posibles cambios de signo de numerador y denominador
            denom = abs(denom)
            num = -1*num
        elif denom == 0: # Se indefine la fracción
            raise ZeroDivisionError
        return num, denom # Retornar tupla

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
    for j in range(len(nombre_columnas) - 1): #Total de columnas
        Fraccion.mul(fila[j], num) # Multiplicar num por fila
        Fraccion.sum(matriz[num_fila2][j], fila[j])

def minimo():
    #Función que retorna la posición del coeficiente mínimo de la función objetivo,
    #lo que permite obtener la posición de la columna pivote
    fila = copy.deepcopy(matriz[0])
    for j in range(len(nombre_columnas) - 2): #Total de columnas objetivo menos columna LD
        fila[j] = get_num(fila[j]) / get_denom(fila[j])    
    return fila.index(min(fila))   
    
def minimo_cociente(num_columna):
    #Función que retorna la posición de la fila pivote que contiene el cociente mínimo 
    res = [sub[num_columna] for sub in matriz] # Obtener la columna
    columna = copy.deepcopy(res)
    for i in range(len(nombre_filas) - 1): #Se usa el total de filas menos la fila de función objetivo
        columna[i+1] = get_num(columna[i+1]) / get_denom(columna[i+1]) # Guardar valores numéricos
        if (columna[i+1] <= 0): # Remover valores negativos
            columna.remove(columna[i+1])
            if (not columna):
               return -2,-2 # U no Acotada
        else:
            columna[i+1] = (get_num(matriz[i+1][len(matriz[0])-1]) / get_denom(matriz[i+1][len(matriz[0])-1])) / columna[i+1] # Guardar cocientes
            
    valor = min(columna) # Chequear si hay cocientes mínimos duplicados
    min_duplicados = [i for i, x in enumerate(columna) if x == valor]
    if (len(min_duplicados) >= 2):
        return columna.index(min(columna)), -1 # Es solución degenerada
    else:
        return columna.index(min(columna)), 1 # OK

def obtener_nuevapos():
    #Función que obtiene la nueva posición de la (fila pivote y columna pivote) en la nueva iteración del método simplex
    global tipo_solucion
    
    pos_column = minimo()
    pos_fila = minimo_cociente(pos_column)
    if (pos_fila[1] == -2):
        print("U no Acotada")
        sys.exit()
    elif (pos_fila[1] == -1):
        tipo_solucion = "degenerada"                
    return pos_fila, pos_column

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
    global metodo
    global optimizacion
    
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

        metodo = int(lineas[0][0]) # Obtener tipo de método

        optimizacion = str(lineas[0][1]) # Obtener tipo de optimización 
            
        cont_var_artificial = 0
        cont_var_exceso = 0
        print(int(lineas[0][2]))
        print(int(lineas[0][3]))
        nombre_columnas = ["VB"] # Colocar etiquetas a los nombres de las columnas
        #ARRRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEGGGGGGGGGGGGGGGLLLLLLLLLLLLLLAAAAAAAAAAAAAARRRRRRRRRRRRRR
        for i in range(int(lineas[0][3]) + 2):
            for j in range(int(lineas[0][2]) + int(lineas[0][3])):
                
                if (j >= int(lineas[0][2]) and lineas[i+2][int(lineas[0][2])] == "="):
                   nombre_columnas.append("a" + "R" + str(cont_var_artificial+1)) # Variable artificial
                   cont_var_artificial = cont_var_artificial + 1
                   
                elif (j >= int(lineas[0][2]) and lineas[i][int(lineas[0][2])] == ">="):
                    nombre_columnas.append("e" + "x" + str(j+1)) # Variable de exceso
                    nombre_columnas.append("a" + "R" + str(cont_var_artificial+1)) # Variable artificial
                    cont_var_exceso = cont_var_exceso + 1
                    cont_var_artificial = cont_var_artificial + 1
                    
                else:
                    nombre_columnas.append("h" + "x" + str(j+1)) # Variable de holgura
                
        nombre_columnas.append("LD")
        print(nombre_columnas)
        
        nombre_filas = ["U"] # Obtener el nombre de cada fila (variables básicas)
        for i in range(int(lineas[0][3]) + cont_var_exceso):
            
            if (nombre_columnas[i+1+int(lineas[0][2])][0] != "e"): # No agregar variables de exceso como variables básicas
                nombre_filas.append(nombre_columnas[i+1+int(lineas[0][2])])
                
        print(nombre_filas)

        inicializar_matriz() #inicializar matriz con ceros

        agrega_var_exceso = 0 # Cuenta la cantidad de veces que se añadió una variable de exceso seguido de una variable artificial en misma fila
        for i in range(len(nombre_filas)):  # Asignar números a matriz
            for j in range(len(nombre_columnas) - 1):
                
                if (j >= int(lineas[0][2]) and j < len(nombre_columnas) - 2):  # Asignar variables no básicas en restricciones
                    
                    if (j - int(lineas[0][2]) + agrega_var_exceso == i-1 and nombre_columnas[j+1][0] == "h"): # Asignar variables de holgura
                         matriz[i][j] = Fraccion(1,1)

                    elif (j - int(lineas[0][2]) + agrega_var_exceso == i-1 and nombre_columnas[j+1][0] == "e"): # Asignar variable de exceso junto con su variable artificial
                         matriz[i][j] = Fraccion(-1,1)
                         matriz[i][j+1] = Fraccion(1,1)
                         agrega_var_exceso = agrega_var_exceso + 1
                         
                    elif (nombre_columnas[j+1][0] == "a"): # Asignar variables artificiales
                          
                          if (i == 0):
                              matriz[i][j] = Fraccion(M,1)
                              
                          elif (j - int(lineas[0][2]) + agrega_var_exceso == i-1):
                               matriz[i][j] = Fraccion(1,1)                        
                        
                elif (j < int(lineas[0][2]) and i == 0): # Asignar variables básicas en función objetivo
                    if (optimizacion == "max"):
                        matriz[i][j] = Fraccion(int(lineas[i+1][j]) * -1,1) # Hay maximización
                    else:
                        matriz[i][j] = Fraccion(int(lineas[i+1][j]),1) # Se pasó de minimización a maximización
                      
                elif (j < int(lineas[0][2])):  # Asignar variables básicas en restricciones
                     matriz[i][j] = Fraccion(int(lineas[i+1][j]),1) 
                     
            if (i != 0): # Asignar LD a las restricciones
                matriz[i][len(matriz[0])-1] = Fraccion(int(lineas[i+1][len(lineas[i+1]) -1 ]),1)
    
        actualizar_prettytable()
        #Escribir resultado en archivo de salida
        salida = open('ver.txt', 'w')
        salida.write("Estado " + str(0) + "\n")
        salida.write("VB entrante: x" + str(1) + ", " + "VB saliente: x" + str(1) + ", " + "Número Pivot: " + str(1) + "\n")
        salida.write(str(pt))
        salida.write("\n")
        salida.write("Estado " + "Final" + "\n")
        salida.write("VB entrante: x" + str(1) + ", " + "VB saliente: x" + str(1) + ", " + "Número Pivot: " + str(1) + "\n")
        salida.write("Respuesta Final: U=" + str(26) + ", " + "(RA)" + "\n")        
        salida.write(str(pt))
        salida.write("\n")

        # Preparar la tabulación de la matriz cuando hay método de la gran M (Quitar M's en función objetivo)       
        if (hallar_letra("a", nombre_columnas)):
            for i in range(len(nombre_filas) - 1):
                for j in range(len(nombre_columnas) - 1): #Total de columnas
                    if (nombre_columnas[j+1][0] == "a" and Fraccion.get_num(matriz[i+1][j]) == 1 and Fraccion.get_denom(matriz[i+1][j]) == 1):
                        operacion_fila(0, i+1, Fraccion(M*-1,1))
                        break

        actualizar_prettytable()
        salida.write(str(pt))

    #Imprimir datos de línea de comandos
    n = len(sys.argv) 
    print("Total de argumentos pasados:", n) 
  
    print("\nArgumentos pasados:", end = " ") 
    for i in range(0, n): 
        print(sys.argv[i], end = " ")
    print("\n")


if __name__ == "__main__":
    main()
