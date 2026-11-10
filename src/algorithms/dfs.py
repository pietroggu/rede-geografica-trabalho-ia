"""Busca em Profundidade (Depth-First Search - DFS)."""

import math


def dfs(grafo, inicio, destino):
    """Executa a busca em profundidade iterativa do vértice de início ao destino.

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
    explorados = [inicio]
    pais = {inicio: None}
    pilha = [(inicio, iter(grafo.neighbors(inicio)))]

    encontrado = False

    while pilha and not encontrado:
        atual, vizinhos = pilha[-1]

        try:
            vizinho = next(vizinhos)

            if vizinho in visitados:
                continue

            visitados.add(vizinho)
            pais[vizinho] = atual
            explorados.append(vizinho)

            if vizinho == destino:
                encontrado = True
                break

            pilha.append((vizinho, iter(grafo.neighbors(vizinho))))

        except StopIteration:
            pilha.pop()

    if not encontrado:
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
