#!/usr/bin/python3

import sys
from prettytable import PrettyTable
import copy 

matriz = [] # Guarda los números de la tabla actual
nombre_columnas = [] # Guarda los nombres de las columnas de la tabla actual
nombre_filas = [] # Guarda los nombres de las filas de la tabla actual

###########################################################################################################
#----------------------------------------------------------------------------------------------------------
#   Clase Fracción y métodos
#   Se usó de referencia la clase "Fraction" implementada por msarialp en https://gist.github.com/mustaa/2350807
#----------------------------------------------------------------------------------------------------------
##########################################################################################################
def gcd(num, denom):
#Función que retorna el máximo común divisor
    while num != denom:
        if num > denom:
            num = num - denom
        elif (num == 0 or denom == 0):
             return 1
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
    
def inicializar_matriz():
    #Función que inicializa la matriz con ceros
    global matriz
    matriz=[] #Vaciar matriz
    
    for i in range(len(nombre_filas)): #Total de filas
        row=[] #Fila
        for j in range(len(nombre_columnas) - 1): #Total de columnas
            row.append(0) #Añadir 0 para cada columna de esta fila
        matriz.append(row) #Añadir fila definida a la matriz

def main():
    
    global matriz # Para trabajar con variables globales
    global nombre_filas
    global nombre_columnas
    
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
#            f1 = Fraccion(2,-2)
#            f2 = Fraccion(3,4)
#            Fraccion.div(f1,f2)
#            print(Fraccion.__str__(f1))
        
    
    if (arg_valido): #El número y tipo de los argumentos es válido
        entrada = open(sys.argv[1],"r")        
        lineas = entrada.readlines() # Obtiene todas las líneas del archivo de entrada        
        entrada.close() # Cerrar archivo de entrada
        
        for i in range(len(lineas)): # Quitar comillas de las lineas
            lineas[i] = lineas[i].split(',')        
        
        nombre_columnas = ["VB"] # Obtener el nombre de cada columna
        for i in range(int(lineas[0][2]) + int(lineas[0][3])):
           nombre_columnas.append("x" + str(i+1))
        nombre_columnas.append("LD")
        print(nombre_columnas)
        
        nombre_filas = ["U"] # Obtener el nombre de cada fila
        for i in range(int(lineas[0][3])):
           nombre_filas.append(nombre_columnas[i+1+int(lineas[0][2])])
        print(nombre_filas)

        inicializar_matriz() #inicializar matriz

        for i in range(len(nombre_filas)):  # Asignar números a matriz
            for j in range(len(nombre_columnas) - 1):
                
                if (j >= int(lineas[0][2]) and i == 0): # Asignar ceros en función objetivo (incluyendo su LD)
                    matriz[i][j] = Fraccion(0,1)
                    
                elif (j >= int(lineas[0][2]) and j < len(nombre_columnas) - 2):  # Asignar coeficientes de variables de holgura en restricciones
                      if (i+1 == j):
                         matriz[i][j] = Fraccion(1,1)
                         
                      else:
                         matriz[i][j] = Fraccion(0,1)
                      
                elif (j < int(lineas[0][2]) and i == 0): # Asignar y cambiar signo a coeficientes de variables en función objetivo
                      matriz[i][j] = Fraccion(int(lineas[i+1][j]) * -1,1)
                      
                elif (j < int(lineas[0][2])):  # Asignar coeficientes de variables en restricciones
                     matriz[i][j] = Fraccion(int(lineas[i+1][j]),1) 
                     
            if (i != 0): # Asignar LD
                matriz[i][len(matriz[0])-1] = Fraccion(int(lineas[i+1][len(lineas[i+1]) -1 ]),1)             

        #Escribir resultado en archivo de salida
        x = PrettyTable(nombre_columnas) # Asignar nombres de columnas al prettytable
        x.align["VB"] = "l" 
        x.padding_width = 3
        x.padding_height = 2
        
        matriz_salida = copy.deepcopy(matriz)
        for i in range(len(matriz)): # Pasar todos las fracciones de matriz a string
            for j in range(len(matriz[0])):
                matriz_salida[i][j] = Fraccion.__str__(matriz_salida[i][j])
                
        filas_completas = []
        filas = []
        for i in range(len(nombre_filas)): # Asignar filas de números al prettytable, junto con sus nombres de fila
            filas = [nombre_filas[i]] + matriz[i]
            filas_completas.append(filas)
            x.add_row(filas_completas[i])

        salida = open('ver.txt', 'w')
        salida.write("Estado " + str(0) + "\n")
        salida.write("VB entrante: x" + str(1) + ", " + "VB saliente: x" + str(1) + ", " + "Número Pivot: " + str(1) + "\n")
        salida.write(str(x))
        salida.write("\n")
        salida.write("Estado " + "Final" + "\n")
        salida.write("VB entrante: x" + str(1) + ", " + "VB saliente: x" + str(1) + ", " + "Número Pivot: " + str(1) + "\n")
        salida.write("Respuesta Final: U=" + str(26) + ", " + "(RA)" + "\n")        
        salida.write(str(x))





    #Imprimir datos de línea de comandos
    n = len(sys.argv) 
    print("Total de argumentos pasados:", n) 
  
    print("\nArgumentos pasados:", end = " ") 
    for i in range(0, n): 
        print(sys.argv[i], end = " ")
    print("\n")




if __name__ == "__main__":
    main()
