"""Busca Gulosa pela Melhor Escolha (Greedy Best-First Search)."""

import heapq
import math


def heuristica(grafo, u, v):
    """Calcula a distância euclidiana em linha reta entre os nós u e v."""
    x1, y1 = grafo.get_position(u)
    x2, y2 = grafo.get_position(v)
    return math.hypot(x1 - x2, y1 - y2)


def best_first_search(grafo, inicio, destino):
    """Executa a busca Best-First guiada puramente pela heurística euclidiana h(n).

    Args:
        grafo: Instância de Graph.
        inicio: Identificador do nó de partida.
        destino: Identificador do nó de chegada.

    Returns:
        tuple: (caminho, distancia_total, lista_explorados)
    """
    if inicio == destino:
        return [inicio], 0.0, [inicio]

    contador = 0
    fila_prioridade = [(heuristica(grafo, inicio, destino), contador, inicio)]
    visitados = {inicio}
    pais = {inicio: None}
    explorados = []

    encontrado = False

    while fila_prioridade:
        _, _, no_atual = heapq.heappop(fila_prioridade)
        explorados.append(no_atual)

        if no_atual == destino:
            encontrado = True
            break

        for vizinho in grafo.neighbors(no_atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pais[vizinho] = no_atual
                contador += 1
                h = heuristica(grafo, vizinho, destino)
                heapq.heappush(fila_prioridade, (h, contador, vizinho))

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
