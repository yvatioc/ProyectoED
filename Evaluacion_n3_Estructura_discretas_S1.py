#AUTHORS: Cesar Araya, Erick Arroyo, Ignacio Yévenes
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import heapq

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, nombre):
        if nombre not in self.vertices:
            self.vertices[nombre] = []

    # Agregar arista con latencia, costo, ancho de banda y estado
    def agregar_arista(self, origen, destino, latencia, costo, ancho_banda, estado="Activo"):
        if destino not in self.vertices:
            self.agregar_vertice(destino)
        # Conexión de Ida
        self.vertices[origen].append((destino, latencia, costo, ancho_banda, estado))

    def mostrar_lista_adyacencia(self):
        print("Lista de adyacencia")
        for vertice, vecinos in self.vertices.items():
            print(f"{vertice} -> ", end="")
            if len(vecinos) == 0:
                print("-")
            else:
                conexiones = []
                for destino, lat, costo, ab, estado in vecinos:
                    conexiones.append(f"{destino} (Lat: {lat}, Costo: {costo}, AB: {ab}, Est: {estado})")
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
            for destino, lat, costo, ab, estado in self.vertices[origen]:
                if destino in self.vertices:
                    columna = vertices.index(destino)
                    matriz[fila][columna] = lat
                else:
                    print(f"Advertencia: El nodo '{destino}' falta en self.vertices.")
        return vertices, matriz
    
    def mostrar_matriz_adyacencia(self):
            vertices, matriz = self.generar_matriz_adyacencia()
            
            df_matriz = pd.DataFrame(matriz, index=vertices, columns=vertices)
            
            df_matriz.to_csv("matriz_adyacencia_completa.csv")
            
            print("\n" + "="*50)
            print(" MATRIZ DE ADYACENCIA")
            print("="*50)
            print("La matriz completa de 65x65 se ha guardado en el archivo 'matriz_adyacencia_completa.csv' para su correcta visualización.")
            print("\nAquí tienes una vista previa de los primeros 10x10 nodos:\n")
            
            vista_previa = df_matriz.iloc[:10, :10].replace(0, "-")
            print(vista_previa)

    def graficar_grafo(self):
            vertices, matriz = self.generar_matriz_adyacencia()
            n_matriz = np.array(matriz)
            grafo = nx.from_numpy_array(n_matriz, create_using=nx.DiGraph)
            
            cambio_nombres = {i: vertices[i] for i in range(len(vertices))}
            grafo = nx.relabel_nodes(grafo, cambio_nombres)
            
            plt.figure(figsize=(20, 16))
            
            nodos_ordenados = sorted(list(grafo.nodes()))
            pos = {}
            for i, nodo in enumerate(nodos_ordenados):
                col = i % 9 
                row = i // 9 
                pos[nodo] = (col, -row) 
                
            nx.draw_networkx_nodes(grafo, pos, node_color='lightgreen', node_size=500, edgecolors='darkgreen')
            nx.draw_networkx_labels(grafo, pos, font_size=8, font_weight='bold')

            nx.draw_networkx_edges(grafo, pos, arrowsize=8, edge_color='gray', alpha=0.4, 
                                connectionstyle='arc3,rad=0.2')

            pesos = nx.get_edge_attributes(grafo, 'weight')
            nx.draw_networkx_edge_labels(
                grafo, pos, edge_labels=pesos, font_size=7, font_color='darkred',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.5)
            )
            
            plt.title("Topología de Red ISP (Vista de Tablero)", fontsize=18, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

    def modificar_arista(self, origen, destino, nueva_latencia, nuevo_costo, nuevo_ancho_banda, nuevo_estado):
        if origen in self.vertices:
            for i, (dest, lat, costo, ab, estado) in enumerate(self.vertices[origen]):
                if dest == destino:
                    self.vertices[origen][i] = (destino, nueva_latencia, nuevo_costo, nuevo_ancho_banda, nuevo_estado)
                    print(f"Arista modificada: {origen} -> {destino}")
                    return
        print(f"No se encontró la arista: {origen} -> {destino}")
    
    def eliminar_arista(self, origen, destino):
        if origen in self.vertices:
            for i, (dest, lat, costo, ab, estado) in enumerate(self.vertices[origen]):
                if dest == destino:
                    del self.vertices[origen][i]
                    print(f"Arista eliminada: {origen} -> {destino}")
                    return
        print(f"No se encontró la arista: {origen} -> {destino}")

    def buscar_ruta_optima(self, origen, destino):
        # La cola de prioridad guarda: (latencia_total, neg_ancho_banda_prom, costo_total, nodo_actual, camino_recorrido, lista_anchos_banda)
        # Usamos ancho de banda negativo para que heapq priorice el número mayor (al ser menor en negativo)
        cola = [(0, 0, 0, origen, [origen], [])]
        
        # Diccionario para guardar el mejor estado con el que llegamos a un nodo y podar caminos ineficientes
        mejores_estados = {origen: (0, 0, 0)}
        
        while cola:
            lat_total, neg_ab_prom, costo_total, actual, camino, ab_list = heapq.heappop(cola)
            
            # Si llegamos al destino, como usamos heapq, esta es la ruta óptima garantizada
            if actual == destino:
                ab_promedio = -neg_ab_prom if ab_list else 0
                return camino, lat_total, ab_promedio, costo_total
                
            for vecino, v_lat, v_costo, v_ab, v_estado in self.vertices.get(actual, []):
                # Ignorar enlaces inactivos o evitar ciclos volviendo a nodos ya visitados
                if v_estado != "Activo" or vecino in camino:
                    continue
                    
                nueva_lat = lat_total + v_lat
                nuevo_costo = costo_total + v_costo
                nueva_ab_list = ab_list + [v_ab]
                nuevo_ab_prom = sum(nueva_ab_list) / len(nueva_ab_list)
                nuevo_neg_ab_prom = -nuevo_ab_prom
                
                nuevo_estado = (nueva_lat, nuevo_neg_ab_prom, nuevo_costo)
                
                # Si no hemos visitado el vecino, o si encontramos una ruta mejor jerárquicamente
                if vecino not in mejores_estados or nuevo_estado < mejores_estados[vecino]:
                    mejores_estados[vecino] = nuevo_estado
                    heapq.heappush(cola, (nueva_lat, nuevo_neg_ab_prom, nuevo_costo, vecino, camino + [vecino], nueva_ab_list))
                    
        # Si la cola se vacía y no llegamos al destino, no hay ruta
        return None, 0, 0, 0
    
    # Comprobar si la red se desconecta
    def es_conexo(self, ignorar_nodo=None):
        nodos_validos = [n for n in self.vertices if n != ignorar_nodo]
        if not nodos_validos or len(nodos_validos) == 1:
            return True
            
        visitados = set()
        cola = [nodos_validos[0]]
        visitados.add(nodos_validos[0])
        
        while cola:
            actual = cola.pop(0)
            # Conexiones salientes
            for destino, lat, costo, ab, estado in self.vertices.get(actual, []):
                if destino != ignorar_nodo and destino not in visitados:
                    visitados.add(destino)
                    cola.append(destino)
            # Conexiones entrantes
            for origen in self.vertices:
                if origen != ignorar_nodo:
                    for dest, lat, costo, ab, estado in self.vertices.get(origen, []):
                        if dest == actual and origen not in visitados:
                            visitados.add(origen)
                            cola.append(origen)
                            
        return len(visitados) == len(nodos_validos)

    # Eliminar un router validando que no sea punto de articulación
    def eliminar_router(self, router):
        if router not in self.vertices:
            print(f"Error: El router '{router}' no existe.")
            return
            
        if not self.es_conexo(ignorar_nodo=router):
            print(f"Operación Denegada: No se puede eliminar '{router}'. Es un punto de articulación y dejará zonas aisladas.")
            return
            
        del self.vertices[router]
        for origen in self.vertices:
            self.vertices[origen] = [(d, l, c, a, e) for (d, l, c, a, e) in self.vertices[origen] if d != router]
        print(f"Éxito: Router '{router}' eliminado correctamente.")

    # Análisis de zonas aisladas
    def analizar_conectividad(self):
        if not self.vertices:
            print("La red está vacía.")
            return
            
        # Usamos nuestra función es_conexo sin ignorar ningún nodo
        if self.es_conexo():
            print("Red estable: Todos los routers están interconectados. No hay zonas aisladas.")
        else:
            print("¡Alerta! Se detectaron zonas aisladas en la red.")
    

def carga_datos_excel(nombre_archivo):
    datos = pd.read_excel(nombre_archivo)
    origen = datos["Origen"].to_list()
    destino = datos["Destino"].to_list()
    latencia = datos["Latencia"].to_list()
    costo_clp = datos["Costo_CLP"].to_list()
    ancho_banda = datos["Ancho_Banda"].to_list()

    g = Grafo()
    largo = len(origen)
    i = 0
    while i < largo:
        g.agregar_vertice(origen[i])
        g.agregar_arista(origen[i], destino[i], latencia[i], costo_clp[i], ancho_banda[i])
        i += 1
    return g
    

def mostrar_datos(grafo):
    grafo.mostrar_lista_adyacencia()
    grafo.mostrar_matriz_adyacencia()
    grafo.graficar_grafo()

def ingreso_de_ruta(g):
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
    
if __name__ == "__main__":
    print("Cargando sistema desde 'red_isp_65_registros.xlsx'...")
    grafo = carga_datos_excel("red_isp_65_registros.xlsx")

    while True:
        print("\n" + "="*50)
        print("   SISTEMA DE ANÁLISIS Y MONITOREO DE REDES ISP")
        print("="*50)
        print("1. Mostrar Red (Lista, Matriz y Visualización gráfica)")
        print("2. Modificar Enlace")
        print("3. Eliminar Enlace")
        print("4. Eliminar Router Válido")
        print("5. Análisis de Conectividad (Zonas aisladas)")
        print("6. Análisis de Rutas (Camino Óptimo)")
        print("7. Salir del sistema")
        print("="*50)
        
        opcion = input("Seleccione una opción (1-7): ").strip()
        
        if opcion == "1":
            mostrar_datos(grafo)
            
        elif opcion == "2":
            print("\n--- MODIFICAR ENLACE ---")
            origen = input("Router Origen: ").strip().upper()
            while origen not in grafo.vertices:
                print("Router de origen no válido. Ingrese un router existente:")
                origen = input().strip().upper()

            while True:
                destino = input("Router Destino: ").strip().upper()
                
                # verificar si el router destino existe en la red
                if destino not in grafo.vertices:
                    print("El router de destino no existe en el sistema. Intente de nuevo.")
                    continue  # Reinicia el while True para pedir el destino otra vez
                
                # Si existe en la red, se busca si hay conexión directa desde el origen
                existe = False
                for dest, *_ in grafo.vertices[origen]:
                    if dest == destino:
                        existe = True
                        break  # Rompe el bucle FOR, ya se encontró el enlace
            
                if existe:
                    break  # Rompe el bucle while true
                else:
                    print(f"No existe un enlace directo desde '{origen}' hacia '{destino}'. Intente de nuevo.")
                    print("Para volver al menú principal, ingrese 1.")
                    elec = input("Ingrese su elección: ").strip()
                    if elec == "1":
                        break 
                try:
                    lat = int(input("Nueva Latencia (ms): "))
                    costo = int(input("Nuevo Costo (CLP): "))
                    ab = int(input("Nuevo Ancho Banda (Mbps): "))
                    estado = input("Estado (Activo/Inactivo): ").strip().capitalize()
                    grafo.modificar_arista(origen, destino, lat, costo, ab, estado)
                except ValueError:
                    print("Error: Ingresaste un valor no numérico para latencia, costo o ancho de banda.")
                
        elif opcion == "3":
            print("\n--- ELIMINAR ENLACE ---")
            origen = input("Router Origen: ").strip().upper()
            while origen not in grafo.vertices:
                print("Router de origen no válido. Ingrese un router existente:")
                origen = input().strip().upper()

            while True:
                destino = input("Router Destino: ").strip().upper()
                
                # verificar si el router destino existe en la red
                if destino not in grafo.vertices:
                    print("El router de destino no existe en el sistema. Intente de nuevo.")
                    continue  # Reinicia el while True para pedir el destino otra vez
                
                # Si existe en la red, se busca si hay conexión directa desde el origen
                existe = False
                for dest, *_ in grafo.vertices[origen]:
                    if dest == destino:
                        existe = True
                        break  # Rompe el bucle FOR, ya se encontró el enlace
            
                if existe:
                    break  # Rompe el bucle while true
                else:
                    print(f"No existe un enlace directo desde '{origen}' hacia '{destino}'. Intente de nuevo.")
                    print("Para volver al menú principal, ingrese 1.")
                    elec = input("Ingrese su elección: ").strip()
                    if elec == "1":
                        break  # Salir del bucle while True y volver al menú principal
            grafo.eliminar_arista(origen, destino)
            
        elif opcion == "4":
            print("\n--- ELIMINAR ROUTER ---")
            router = input("Ingrese el Router a eliminar: ").strip().upper()
            grafo.eliminar_router(router)
            
        elif opcion == "5":
            print("\n--- ANÁLISIS DE CONECTIVIDAD ---")
            grafo.analizar_conectividad()
            
        elif opcion == "6":
            print("\n--- ANÁLISIS DE RUTAS (DIJKSTRA) ---")
            nodo_origen, nodo_destino = ingreso_de_ruta(grafo)
            camino, lat_total, ab_promedio, costo_total = grafo.buscar_ruta_optima(nodo_origen, nodo_destino)
            
            print("\n" + "-"*40)
            if camino:
                print(f"Ruta Seleccionada : {' -> '.join(camino)}")
                print(f"Latencia Total    : {lat_total} ms")
                print(f"Ancho Banda Asoc. : {ab_promedio:.2f} Mbps (Promedio)")
                print(f"Costo Total       : ${costo_total} CLP")
            else:
                print(f"Error: No existe ruta posible entre {nodo_origen} y {nodo_destino}.")
            print("-"*40)
            
        elif opcion == "7":
            print("Saliendo del sistema... ¡Nos vemos!")
            break
            
        else:
            print("Opción no válida. Intente de nuevo.")