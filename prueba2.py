nodo_origen = "A"

dicc = {nodo_origen: {"B": 10, "C": 5}}

destinos = []
pesos = []

for destino, peso in dicc[nodo_origen].items():
    destinos.append(destino)
    pesos.append(peso)

print("Destinos:", destinos)  # Imprime la lista de destinos para el nodo de origen "A"
print("Pesos:", pesos)  # Imprime la lista de pesos para el nodo de

nodo_origen = "B"

# Imprime el diccionario de destinos y pesos para el nodo de origen "B"
dicc[nodo_origen] = {"C": 3}
for i in dicc:
    print(dicc[i])  # Imprime el diccionario de destinos y pesos para el nodo de origen

print(dicc)  # Imprime el diccionario completo con todos los nodos de origen y sus destinos