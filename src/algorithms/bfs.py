"""Busca em Largura (Breadth-First Search - BFS)."""

from collections import deque
import math


def bfs(grafo, inicio, destino):
    """Executa a busca em largura do vértice de início ao destino.

    Garante o menor caminho em número de arestas (saltos).

    Args:
        grafo: Instância de Graph.
        inicio: Identificador do nó de partida.
        destino: Identificador do nó de chegada.

    Returns:
        tuple: (caminho, distancia_total, lista_explorados)
    """
    if inicio == destino:
        return [inicio], 0.0, [inicio]

    visitados = {inicio}
    fila = deque([inicio])
    pais = {inicio: None}
    explorados = []

    encontrado = False
    while fila:
        no_atual = fila.popleft()
        explorados.append(no_atual)

        if no_atual == destino:
            encontrado = True
            break

        for vizinho in grafo.neighbors(no_atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pais[vizinho] = no_atual
                fila.append(vizinho)

    if not encontrado and destino not in pais:
        return [], math.inf, explorados

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = pais[atual]
    caminho.reverse()

    distancia = sum(
        grafo.neighbors(caminho[i])[caminho[i + 1]]
        for i in range(len(caminho) - 1)
    )

    return caminho, distancia, explorados
