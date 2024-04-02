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

def clarke_wright(matriz_distancia):
    n = len(matriz_distancia)
    ahorros = np.zeros((n, n))

    print("Distance Matrix:")
    imprimirMatriz(matriz_distancia)

    #Calcular una lista para el ahorro
    savings_list = OrderedDict()
    for i in range(1, n):
        for j in range(i + 1, n):
            savings_list[(i + 1, j + 1)] = matriz_distancia[i][0] + matriz_distancia[0][j] - matriz_distancia[i][j]

    #Ordenar la lista de ahorro
    savings_list = OrderedDict(sorted(savings_list.items(), key=lambda x: x[1], reverse=True))

    print("Savings list:")
    print(savings_list)

    

# Start of the program
if len(sys.argv) != 2:
    print("Usage: ahorros_algorithm.py <file with matrix>")
    sys.exit(1)

file_path = sys.argv[1]

# Load the matrix from the file
matriz_distancia = cargar_laberinto(file_path)

clarke_wright(matriz_distancia)