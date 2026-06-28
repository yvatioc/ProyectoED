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
                columna = vertices.index(destino)
                matriz[fila][columna] = peso
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


if __name__=="__main__":

    g = Grafo()

    g.agregar_vertice("A")
    g.agregar_vertice("B")
    g.agregar_vertice("C")

    g.agregar_arista("A", "B", 10)
    g.agregar_arista("A", "C", 5)
    g.agregar_arista("B", "C", 3)

    g.mostrar_lista_adyacencia()

    g.mostrar_matriz_adyacencia()