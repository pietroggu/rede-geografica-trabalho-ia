"""Ponto de entrada principal do projeto de Busca em Redes Geográficas.

Disciplina: SCC0230 - Inteligência Artificial
Abordagem A: Projeto de Busca em Redes (Rede Geográfica)
"""

import argparse
import sys
from pathlib import Path

from src.algorithms.a_star import astar
from src.algorithms.best_first import best_first_search
from src.algorithms.bfs import bfs
from src.algorithms.dfs import dfs
from src.algorithms.dijkstra import dijkstra
from src.algorithms.hill_climbing import hill_climbing
from src.core.graph import Graph
from src.geographic import gerar_rede_geografica


def executar_demonstracao():
    """Executa uma demonstração básica dos 6 algoritmos em um grafo toy didático."""
    print("=" * 60)
    print("SCC0230 - Inteligência Artificial | Demonstração dos Algoritmos")
    print("=" * 60)

    grafo = Graph()
    grafo.add_node(0, 0, 0)
    grafo.add_node(1, 2, 3)
    grafo.add_node(2, 5, 3)
    grafo.add_node(3, 7, 0)
    grafo.add_node(4, 4, -2)

    arestas = [
        (0, 1, 2.0),
        (0, 2, 6.0),
        (0, 4, 5.0),
        (1, 2, 3.0),
        (1, 4, 7.0),
        (2, 3, 4.0),
        (2, 4, 3.0),
        (3, 4, 2.0),
    ]
    for u, v, w in arestas:
        grafo.add_edge(u, v, w)

    algoritmos = {
        "BFS": bfs,
        "DFS": dfs,
        "Best-First": best_first_search,
        "Hill Climbing": hill_climbing,
        "Dijkstra": dijkstra,
        "A*": astar,
    }

    origem, destino = 0, 3
    print(f"\nBuscando caminho de {origem} até {destino} em grafo de teste:")

    for nome, func in algoritmos.items():
        caminho, dist, explorados = func(grafo, origem, destino)
        status = f"Distância: {dist:.2f} | Saltos: {len(caminho)-1} | Explorados: {len(explorados)}" if caminho else "Sem caminho"
        print(f"  {nome:14} -> Caminho: {caminho} | {status}")


def main():
    parser = argparse.ArgumentParser(description="Projeto SCC0230 - Busca em Redes Geográficas")
    parser.add_argument("--demo", action="store_true", help="Executa demonstração em grafo didático")
    parser.add_argument("--visualizar", action="store_true", help="Gera as visualizações gráficas da busca (Item 4.4.i)")
    parser.add_argument("--benchmark", action="store_true", help="Executa o benchmark e gera gráficos (Item 4.4.ii e 4.4.iii)")
    parser.add_argument("--tudo", action="store_true", help="Executa o pipeline experimental completo")

    args = parser.parse_args()

    # Se nenhum argumento for passado, executa demo e mostra orientações
    if not (args.demo or args.visualizar or args.benchmark or args.tudo):
        executar_demonstracao()
        print("\nPara executar os experimentos completos:")
        print("  python -m src.main --visualizar   # Gera mapas e caminhos (Item 4.4.i)")
        print("  python -m src.main --benchmark    # Executa buscas em n=2500 e gera gráficos")
        print("  python -m src.main --tudo         # Executa todo o pipeline experimental")
        return

    if args.demo:
        executar_demonstracao()

    if args.visualizar or args.tudo:
        print("\n[1/2] Executando geração de visualizações da busca...")
        from src.experiments.gerar_visualizacao_busca import main as rodar_vis
        rodar_vis()

    if args.benchmark or args.tudo:
        print("\n[2/2] Executando benchmarks e geração de gráficos...")
        from src.experiments.selecionar_vertices import selecionar_pares_comuns
        from src.experiments.executar_buscas import main as rodar_buscas
        from src.experiments.gerar_graficos import main as rodar_graficos

        selecionar_pares_comuns()
        rodar_buscas()
        rodar_graficos()


if __name__ == "__main__":
    main()
