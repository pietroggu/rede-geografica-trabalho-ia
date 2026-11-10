"""Algoritmo de Busca A* (A-Estrela) com heurística euclidiana admissível."""

import heapq
import math


def heuristica(grafo, u, v):
    """Calcula a distância euclidiana em linha reta entre os nós u e v."""
    x1, y1 = grafo.get_position(u)
    x2, y2 = grafo.get_position(v)
    return math.hypot(x1 - x2, y1 - y2)


def astar(grafo, inicio, destino):
    """Executa o algoritmo A* encontrando o caminho de menor custo total f(n) = g(n) + h(n).

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
    h_inicio = heuristica(grafo, inicio, destino)
    fila_prioridade = [(h_inicio, 0.0, contador, inicio)]
    
    g_score = {inicio: 0.0}
    pais = {inicio: None}
    visitados = set()
    explorados = []

    encontrado = False

    while fila_prioridade:
        _, custo_g, _, no_atual = heapq.heappop(fila_prioridade)

        if no_atual in visitados:
            continue

        visitados.add(no_atual)
        explorados.append(no_atual)

        if no_atual == destino:
            encontrado = True
            break

        for vizinho, peso in grafo.neighbors(no_atual).items():
            tentativa_g = custo_g + peso
            if tentativa_g < g_score.get(vizinho, math.inf):
                g_score[vizinho] = tentativa_g
                pais[vizinho] = no_atual
                contador += 1
                f_vizinho = tentativa_g + heuristica(grafo, vizinho, destino)
                heapq.heappush(fila_prioridade, (f_vizinho, tentativa_g, contador, vizinho))

    if not encontrado:
        return [], math.inf, explorados

    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = pais[atual]
    caminho.reverse()

    return caminho, g_score[destino], explorados
