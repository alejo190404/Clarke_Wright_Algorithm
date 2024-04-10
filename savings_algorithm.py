# Import libraries
import sys
import numpy as np
from collections import OrderedDict

def imprimirMatriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            print(matriz[i][j], end="\t")
        print()

def cargar_laberinto(ruta_archivo):
    laberinto = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            # Remove square brackets and split by comma
            valores = linea.strip().replace('[', '').replace(']', '').split(',')
            fila = [int(x) for x in valores if x]  # Filter out empty strings
            laberinto.append(fila)
    return laberinto

#Función para saber si un elemento está en un arreglo
def estaEnArreglo(arreglo, elemento):
    for i in range(len(arreglo)):
        if (arreglo[i] == elemento):
            return True
    return False

def estaEnMatriz(matriz, elemento):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if (matriz[i][j] == elemento):
                return True
    return False

#Función para anadir un punto a una ruta
def anadirPuntoARuta(ruta, punto):
    if (estaEnArreglo(ruta, punto[0])):
        #El punto no es interior desde el comienzo o desde el final
        if(ruta.index(punto[0]) == 1):
            ruta.insert(ruta.index(punto[0]) , punto[1])
        else:
            ruta.insert(ruta.index(punto[0]) + 1, punto[1])
    else:
        if(ruta.index(punto[1]) == 1):
            ruta.insert(ruta.index(punto[1]), punto[0])
        else:
            ruta.insert(ruta.index(punto[1]) + 1, punto[0])
        

def fusionar_rutas(ruta1, ruta2, first_key):
    ruta_fusionada = []
    for i in range(len(ruta1)):
        if (ruta1[i] == first_key[0] or ruta1[i] == first_key[1]):
            ruta_fusionada.append(ruta1[i])
            break
        ruta_fusionada.append(ruta1[i])
    if (ruta2.index(first_key[0]) == 1 or ruta2.index(first_key[1]) == len(ruta2) - 2):
        for i in ruta2[1:]:
            ruta_fusionada.append(i)
    return ruta_fusionada

def clarke_wright(matriz_distancia):
    n = len(matriz_distancia)
    ahorros = np.zeros((n, n))

    print("Distance Matrix:")
    imprimirMatriz(matriz_distancia)

    #Calcular una lista para el ahorro
    lista_ahorro = OrderedDict()
    for i in range(1, n):
        for j in range(i + 1, n):
            lista_ahorro[(i + 1, j + 1)] = matriz_distancia[i][0] + matriz_distancia[0][j] - matriz_distancia[i][j]

    #Ordenar la lista de ahorro
    lista_ahorro = OrderedDict(sorted(lista_ahorro.items(), key=lambda x: x[1], reverse=True))

    print("Savings list:")
    print(lista_ahorro)

    routes = [[]]
    

    while(lista_ahorro):
        #Extraer el primer elemnto de la lista
        for key, value in lista_ahorro.items():
            first_key = key
            first_value = value
            break
            
        #Añadir las restricciones que se deseen
        #En este caso, no se seleccionan restricciones, aparte de ahorrar

        #Condición A: Ninguna de los puntos ha sido incluído en una ruta
        if (not(estaEnMatriz(routes, first_key[0])) and not(estaEnMatriz(routes, first_key[1]))):
            routes.append([1, first_key[0], first_key[1], 1])

        #Condición B:
        #Existe en una ruta existente
        if (estaEnMatriz(routes, first_key[0]) and not(estaEnMatriz(routes, first_key[1]))):
            #Encontrar la ruta en la que el punto se encuentra
            for route in routes:
                if (estaEnArreglo(route, first_key[0])):
                    #El punto no es interior a la ruta
                    if (route.index(first_key[0]) == 1 or route.index(first_key[0]) == len(route) - 2):
                        #Añadir el punto a la ruta actual
                        route = anadirPuntoARuta(route, first_key)
                        break
        

        if (not(estaEnMatriz(routes, first_key[0])) and estaEnMatriz(routes, first_key[1])):
            for route in routes:
                if (estaEnArreglo(route, first_key[1])):
                    if (route.index(first_key[1]) == 1 or route.index(first_key[1]) == len(route) - 2):
                        route = anadirPuntoARuta(route, first_key)
                        break

        #Doble AND para condición c
        if ((estaEnMatriz(routes, first_key[0])) and (estaEnMatriz(routes, first_key[1]))):
            #Ninguno de los puntos es interior a la ruta en la que están
            for route1 in routes:
                if(estaEnArreglo(route1, first_key[0]) and not(estaEnArreglo(route1, first_key[1]))):
                    if (route1.index(first_key[0]) <= 1 and route1.index(first_key[0]) >= len(route1) - 2):
                        for route2 in routes:
                            if(not(estaEnArreglo(route2, first_key[0])) and estaEnArreglo(route2, first_key[1])):
                                if (route2.index(first_key[1]) <= 1 and route2.index(first_key[1]) >= len(route2) - 2):
                                    pass
                                    #Fusionar ambas rutas, siempre y cuando cumplan las restricciones
                                    routeFusionada = fusionar_rutas(route1, route2, first_key)
                                    routes.remove(route1)
                                    routes.remove(route2)
                                    routes.append(routeFusionada)
                                    break
                            break
                    break
                if(not(estaEnArreglo(route1, first_key[0])) and estaEnArreglo(route1, first_key[1])):
                    if (route1.index(first_key[1]) > 1 and route1.index(first_key[1]) > 1):
                        for route2 in routes:
                            if(estaEnArreglo(route2, first_key[0]) and not(estaEnArreglo(route2, first_key[1]))):
                                if (route2.index(first_key[0]) > 1 and route2.index(first_key[1]) < len(route2) - 2):
                                    pass
                                    #Fusionar ambas rutas, siempre y cuando cumplan las restricciones
                                    routeFusionada = fusionar_rutas(route1, route2, first_key)
                                    routes.remove(route1)
                                    routes.remove(route2)
                                    routes.append(routeFusionada)
                                    break
                            break
                    break

            

        #Eliminar la lista de rutas
        lista_ahorro.pop(first_key)
    
    print("Camino encontrado:")
    return routes.pop(1)
    
#Comienzo del programa
if len(sys.argv) != 2:
    print("Usage: savings_algorithm.py <file with matrix>")
    sys.exit(1)

file_path = sys.argv[1]

#Cargar matriz desde el archivo
matriz_distancia = cargar_laberinto(file_path)

print(clarke_wright(matriz_distancia))