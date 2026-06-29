import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Grafo:

    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, nombre):
        if nombre not in self.vertices:
            self.vertices[nombre] = []

    def agregar_arista(self, origen, destino, peso):
        self.vertices[origen].append((destino, peso))

    def mostrar_lista_adyacencia(self):
        print("Lista de adyacencia")
        for vertice, vecinos in self.vertices.items():
            print(f"{vertice} -> ", end="")
            if len(vecinos) == 0:
                print("-")
            else:
                conexiones = []
                for destino, peso in vecinos:
                    conexiones.append(f"{destino}({peso})")
                print(", ".join(conexiones))

    def generar_matriz_adyacencia(self):
        vertices = list(self.vertices.keys())
        n = len(vertices)
        matriz = []
        for i in range(n):
            fila = [0] * n
            matriz.append(fila)
        
        for origen in self.vertices:
            fila = vertices.index(origen)
            for destino, peso in self.vertices[origen]:
                if destino in self.vertices:
                    columna = vertices.index(destino)
                    matriz[fila][columna] = peso
                else:
                    # Opcional: Imprime un aviso en consola para que sepas qué nodo falta agregar
                    print(f"Advertencia: El nodo '{destino}' se usa como destino pero no está registrado en self.vertices.")
        return vertices, matriz

    def mostrar_matriz_adyacencia(self):

        vertices, matriz = self.generar_matriz_adyacencia()

        print("\nMATRIZ DE ADYACENCIA\n")

        print("   ", end="")

        for v in vertices:
            print(f"{v:>4}", end="")

        print()

        for i in range(len(vertices)):

            print(f"{vertices[i]:>3}", end="")

            for j in range(len(vertices)):
                print(f"{matriz[i][j]:>4}", end="")

            print()
    def graficar_grafo(self):
        vertices, matriz = self.generar_matriz_adyacencia()
    
        # se pasa la matriz a un array de numpy para poder usarla con networkx
        n_matriz = np.array(matriz)
        grafo = nx.from_numpy_array(n_matriz, create_using=nx.DiGraph)
        
        # cambia los numeros presentados en el grafo por los nombres de los vertices
        cambio_nombres = {}
        for i in range(len(vertices)):
            cambio_nombres[i] = vertices[i]
        grafo = nx.relabel_nodes(grafo, cambio_nombres)
        
        # Dibujar con Matplotlib
        pos = nx.spring_layout(grafo)
        # plt.figure(figsize=(ancho, alto))
        plt.figure(figsize=(8, 6))
        
        nx.draw(grafo, pos, with_labels=True, node_color='lightgreen', node_size=1200)
        
        # Dibujar los pesos de la matriz
        pesos = nx.get_edge_attributes(grafo, 'weight')
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=pesos)
        
        plt.show()

def carga_datos_excel(nombre_archivo):
    # Cargar los datos desde el archivo Excel
    datos = pd.read_excel(nombre_archivo)

    # Crear listas a partir del archivo Excel
    origen = datos["Origen"].to_list()
    destino = datos["Destino"].to_list()
    latencia = datos["Latencia"].to_list()
    costo_clp = datos["Costo_CLP"].to_list()
    ancho_banda = datos["Ancho_Banda"].to_list()

    g = Grafo()
    
    largo = len(origen)
    i = 0
    # Agregar los vértices y aristas al grafo
    while i < largo:
        g.agregar_vertice(origen[i])
        if destino[i] not in g.vertices:
            g.agregar_vertice(destino[i])
        g.agregar_arista(origen[i], destino[i], latencia[i])
        i += 1
    return g

def mostrar_datos(grafo):
    grafo.mostrar_lista_adyacencia()
    grafo.mostrar_matriz_adyacencia()
    grafo.graficar_grafo()

def ingreso_de_ruta(g):

    # Solicitar al usuario que ingrese el nodo de origen y destino
    print("Ingrese el nodo de origen:")
    nodo_origen = input().strip().upper()
    while nodo_origen not in g.vertices:
        print("Nodo de origen no válido. Ingrese un nodo existente:")
        nodo_origen = input().strip().upper()
    
    print("Ingrese el nodo de destino:")
    nodo_destino = input().strip().upper()
    while nodo_destino not in g.vertices:
        print("Nodo de destino no válido. Ingrese un nodo existente:")
        nodo_destino = input().strip().upper()

    return nodo_origen, nodo_destino

def sub_grafo(g, n_o, n_d, n_g):
    nodo_origen = n_o
    nodo_destino = n_d

    # si se encuentra un camino valido desde el nodo de origen hasta el nodo de destino, se agrega al subgrafo
    if nodo_origen == nodo_destino:
        n_g.agregar_vertice(nodo_origen)
        return True

    destinos = []
    pesos = []

    # conseguir los nodos destino y pesos del nodo de origen
    if nodo_origen in g.vertices:
        vertice = g.vertices[nodo_origen]
        for destino, peso in vertice:
            destinos.append(destino)
            pesos.append(peso)
    
    # varible para determinar si al menos un camino desde el nodo de origen llega hasta el nodo de destino exitoso
    al_menos_uno_sirve = False

    # recorrer los destinos del nodo de origen y verificar si alguno de ellos tiene un camino exitoso hasta el nodo destino
    for i in destinos:
        camino_exitoso = sub_grafo(g, i, nodo_destino, n_g)
        
        # Si el camino desde el nodo actual hasta el nodo destino es exitoso, 
        # entonces este nodo forma parte del subgrafo
        if camino_exitoso:
            al_menos_uno_sirve = True
            
            # agregar el camino al subgrafo
            if nodo_origen not in n_g.vertices:
                n_g.agregar_vertice(nodo_origen)
            if i not in n_g.vertices:
                n_g.agregar_vertice(i)
                
            n_g.agregar_arista(nodo_origen, i, pesos[destinos.index(i)])

    return al_menos_uno_sirve

if __name__=="__main__":
    grafo = carga_datos_excel("archivo_prueba2.xlsx")
    nodo_origen, nodo_destino =ingreso_de_ruta(grafo)
    #mostrar_datos(grafo)
    n_g = Grafo()
    nuevo_g = sub_grafo(grafo, nodo_origen, nodo_destino,n_g)

    n_g.mostrar_lista_adyacencia()
    n_g.graficar_grafo()
