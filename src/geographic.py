"""Módulo para geração de redes geográficas conforme especificado no Apêndice A."""

import math
import random
from src.core.graph import Graph


def gerar_rede_geografica(quantidade_vertices: int, lamb: float, seed: int = None) -> Graph:
    """Gera uma rede geográfica não-direcionada com conexão exponencial estocástica.

    Coordenadas (x, y) de cada vértice são sorteadas uniformemente no intervalo [0, n],
    conforme especificação do Apêndice A.
    Para cada par de vértices (u, v), a existência de uma aresta obedece à probabilidade:
        P(u -> v) = exp(-lamb * s_uv)
    onde s_uv é a distância euclidiana entre u e v. O peso da aresta é a própria distância s_uv.

    Args:
        quantidade_vertices: Quantidade total de nós (n).
        lamb: Fator de decaimento espacial (lambda).
        seed: Semente de números pseudoaleatórios para garantia de reprodutibilidade.

    Returns:
        Graph: Grafo construído com nós posicionados e arestas ponderadas.
    """
    rng = random.Random(seed)
    grafo = Graph()

    for i in range(quantidade_vertices):
        x = rng.uniform(0, quantidade_vertices)
        y = rng.uniform(0, quantidade_vertices)
        grafo.add_node(i, x, y)

    for u in range(quantidade_vertices):
        x1, y1 = grafo.get_position(u)
        for v in range(u + 1, quantidade_vertices):
            x2, y2 = grafo.get_position(v)
            distancia = math.hypot(x1 - x2, y1 - y2)
            probabilidade = math.exp(-lamb * distancia)

            if rng.random() < probabilidade:
                grafo.add_edge(u, v, distancia)

    return grafo
