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
        # 1. Obtener los datos que ya genera tu código
        vertices, matriz = self.generar_matriz_adyacencia()
    
        # 2. Convertir tu matriz a formato NumPy y crear el grafo
        # Usa nx.DiGraph para grafos dirigidos (con flechas)
        A = np.array(matriz)
        G = nx.from_numpy_array(A, create_using=nx.DiGraph)
        
        # 3. Mapear los números de los índices (0, 1, 2) a tus nombres reales de vértices
        mapeo_nombres = {i: vertices[i] for i in range(len(vertices))}
        G = nx.relabel_nodes(G, mapeo_nombres)
        
        # 4. Dibujar con Matplotlib
        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        
        nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=1200)
        
        # Dibujar los pesos de la matriz
        pesos = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos)
        
        plt.show()


if __name__=="__main__":
    # Cargar los datos desde el archivo Excel
    datos = pd.read_excel('red_isp_65_registros.xlsx')

    # Crear listas a partir del archivo Excel
    origen = datos["Origen"].to_list()
    destino = datos["Destino"].to_list()
    latencia = datos["Latencia"].to_list()
    costo_clp = datos["Costo_CLP"].to_list()
    ancho_banda = datos["Ancho_Banda"].to_list()

    g = Grafo()
    
    largo = len(origen)
    i = 0
    while i < largo:
        print(f"Agregando arista: {origen[i]} -> {destino[i]} con latencia {latencia[i]}")
        g.agregar_vertice(origen[i])
        if destino[i] not in g.vertices:
            g.agregar_vertice(destino[i])
        g.agregar_arista(origen[i], destino[i], latencia[i])
        i += 1

#    g.agregar_vertice("A")
#    g.agregar_vertice("B")
#    g.agregar_vertice("C")

#    g.agregar_arista("A", "B", 10)
#    g.agregar_arista("A", "C", 5)
#    g.agregar_arista("B", "C", 3)

    g.mostrar_lista_adyacencia()

    g.mostrar_matriz_adyacencia()

    g.graficar_grafo()