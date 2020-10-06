#!/usr/bin/python3

import sys
from prettytable import PrettyTable

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
def main():

    arg_valido = True

    if (len(sys.argv) == 3):
        arg_valido = False
        
        if (not(isinstance(sys.argv[1], str) and isinstance(sys.argv[2], str))):
            print("Tipo equivocado de argumentos (Se requiere: string string string)")

        if (sys.argv[1] != "-h"):
            print("Argumento #2 debe ser '-h'")
            
        else:
            manual()

    if (len(sys.argv) == 2):
    
        if (not(isinstance(sys.argv[1], str))):
            print("Tipo equivocado de argumentos (Se requiere: string string)")
            arg_valido = False

    if (len(sys.argv) > 3 or len(sys.argv) < 2):    
        print("Número equivocado de argumentos (se requieren 2 o 3)")
        arg_valido = False
    
        if (len(sys.argv) == 1):
            print("Sólo se recibió el nombre del programa")
        
    
    if (arg_valido): #El número y tipo de los argumentos es válido
        r = open(sys.argv[1],"r")
        print ("Nombre de archivo: ", r.name)
        x = PrettyTable([r.name, "Area", "Population", "Annual Rainfall"])
        x.align[r.name] = "l" 
        x.padding_width = 1 
        x.add_row(["Adelaide",1295, 1158259, 600.5])
        x.add_row(["Brisbane",5905, 1857594, 1146.4])
        x.add_row(["Darwin", 112, 120900, 1714.7])
        x.add_row(["Hobart", 1357, 205556, 619.5])
        x.add_row(["Sydney", 2058, 4336374, 1214.8])
        x.add_row(["Melbourne", 1566, 3806092, 646.9])
        x.add_row(["Perth", 5386, 1554769, 869.4])
        r.close()
        w = open('ver.txt', 'w')
        w.write(str(x))
        w.write("\n")
        w.write(str(x))





    #Imprimir datos de línea de comandos
    n = len(sys.argv) 
    print("Total de argumentos pasados:", n) 
  
    print("\nArgumentos pasados:", end = " ") 
    for i in range(0, n): 
        print(sys.argv[i], end = " ")
    print("\n")




if __name__ == "__main__":
    main()
