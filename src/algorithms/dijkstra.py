"""Algoritmo de Dijkstra para caminho mínimo em grafos ponderados com arestas positivas."""

import heapq
import math


def dijkstra(grafo, origem, destino):
    """Encontra o caminho de menor custo entre origem e destino via Dijkstra (min-heap).

    Args:
        grafo: Instância de Graph.
        origem: Identificador do vértice inicial.
        destino: Identificador do vértice meta.

    Returns:
        tuple: (caminho, distancia_total, lista_explorados)
    """
    fila_prioridade = [(0.0, origem)]
    distancias = {origem: 0.0}
    pais = {origem: None}
    visitados = set()
    explorados = []

    while fila_prioridade:
        dist_atual, vertice_atual = heapq.heappop(fila_prioridade)

        if vertice_atual in visitados:
            continue

        visitados.add(vertice_atual)
        explorados.append(vertice_atual)

        if vertice_atual == destino:
            break

        for vizinho, peso in grafo.neighbors(vertice_atual).items():
            nova_distancia = dist_atual + peso
            if nova_distancia < distancias.get(vizinho, math.inf):
                distancias[vizinho] = nova_distancia
                pais[vizinho] = vertice_atual
                heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

    if destino not in visitados:
        return [], math.inf, explorados

    # Reconstrução do caminho ótimo
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = pais[atual]
    caminho.reverse()

    return caminho, distancias[destino], explorados
