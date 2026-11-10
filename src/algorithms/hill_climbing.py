"""Subida de Encosta (Hill Climbing) sem backtracking."""

import math


def heuristica(grafo, u, v):
    """Calcula a distância euclidiana em linha reta entre os nós u e v."""
    x1, y1 = grafo.get_position(u)
    x2, y2 = grafo.get_position(v)
    return math.hypot(x1 - x2, y1 - y2)


def hill_climbing(grafo, inicio, destino):
    """Executa Hill Climbing guloso estrito sem backtracking em direção ao destino.

    A cada passo, seleciona o vizinho não visitado com menor heurística h.
    Interrompe a busca se nenhum vizinho estritamente melhorar a estimativa (mínimo local).

    Args:
        grafo: Instância de Graph.
        inicio: Identificador do nó de partida.
        destino: Identificador do nó de chegada.

    Returns:
        tuple: (caminho, distancia_total, lista_explorados)
    """
    if inicio == destino:
        return [inicio], 0.0, [inicio]

    atual = inicio
    visitados = {inicio}
    caminho = [inicio]
    explorados = [inicio]

    while atual != destino:
        melhor_vizinho = None
        melhor_h = heuristica(grafo, atual, destino)

        for vizinho in grafo.neighbors(atual):
            if vizinho not in visitados:
                h_vizinho = heuristica(grafo, vizinho, destino)
                if h_vizinho < melhor_h:
                    melhor_h = h_vizinho
                    melhor_vizinho = vizinho

        # Se não há melhora estrita (mínimo local atingido), encerra sem retorno
        if melhor_vizinho is None:
            return [], math.inf, explorados

        atual = melhor_vizinho
        visitados.add(atual)
        caminho.append(atual)
        explorados.append(atual)

    distancia = sum(
        grafo.neighbors(caminho[i])[caminho[i + 1]]
        for i in range(len(caminho) - 1)
    )

    return caminho, distancia, explorados
