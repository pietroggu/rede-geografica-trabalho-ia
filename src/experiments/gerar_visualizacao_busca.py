"""Gera as visualizações de busca e topologia para rede de pequeno porte (Item 4.4.i)."""

import random
from pathlib import Path

from src.algorithms.a_star import astar
from src.algorithms.best_first import best_first_search
from src.algorithms.bfs import bfs
from src.algorithms.dfs import dfs
from src.algorithms.dijkstra import dijkstra
from src.algorithms.hill_climbing import hill_climbing
from src.geographic import gerar_rede_geografica
from src.visualization import visualizar_comparacao_buscas, visualizar_topologia_rede


def encontrar_maior_componente(grafo):
    """Encontra a lista de vértices da maior componente conexa."""
    visitados = set()
    componentes = []

    for inicio in grafo.adjacency:
        if inicio in visitados:
            continue
        pilha = [inicio]
        visitados.add(inicio)
        comp = []
        while pilha:
            u = pilha.pop()
            comp.append(u)
            for v in grafo.neighbors(u):
                if v not in visitados:
                    visitados.add(v)
                    pilha.append(v)
        componentes.append(comp)

    return max(componentes, key=len), componentes


def main():
    n = 250
    lamb = 0.05
    seed = 42

    pasta_figuras = Path("outputs/figures")
    pasta_figuras.mkdir(parents=True, exist_ok=True)

    print(f"Gerando rede geográfica com n={n}, lambda={lamb}...")
    grafo = gerar_rede_geografica(quantidade_vertices=n, lamb=lamb, seed=seed)
    maior_comp, todas_comps = encontrar_maior_componente(grafo)

    print(f"Total de componentes: {len(todas_comps)} | Maior componente: {len(maior_comp)} vértices")

    # 1. Salvar figura da topologia
    caminho_topologia = pasta_figuras / "topologia_rede_250.png"
    visualizar_topologia_rede(
        grafo,
        todas_comps,
        titulo=f"Topologia da Rede Geográfica (n={n}, λ={lamb})",
        salvar_em=caminho_topologia,
    )
    print(f"Topologia salva em: {caminho_topologia}")

    # 2. Selecionar par de origem e destino na maior componente com distância considerável
    rng = random.Random(2026)
    # Selecionar nós com boa separação espacial para demonstrar a busca
    candidatos = list(maior_comp)
    melhor_par = None
    maior_dist_reta = 0.0

    for _ in range(50):
        u, v = rng.sample(candidatos, 2)
        x1, y1 = grafo.get_position(u)
        x2, y2 = grafo.get_position(v)
        dist_reta = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        if dist_reta > maior_dist_reta:
            maior_dist_reta = dist_reta
            melhor_par = (u, v)

    origem, destino = melhor_par
    print(f"Par selecionado para visualização: Origem {origem} -> Destino {destino} (Dist Euclidiana Direta: {maior_dist_reta:.2f})")

    # 3. Executar algoritmos
    algoritmos = {
        "BFS": bfs,
        "DFS": dfs,
        "Best-First": best_first_search,
        "A*": astar,
        "Hill Climbing": hill_climbing,
        "Dijkstra": dijkstra,
    }

    resultados = {}
    for nome, func in algoritmos.items():
        caminho, dist, explorados = func(grafo, origem, destino)
        resultados[nome] = (caminho, dist, explorados)
        status = f"Dist: {dist:.2f}, Saltos: {len(caminho)-1}, Explorados: {len(explorados)}" if caminho else "FALHA / Mínimo Local"
        print(f"  {nome:14}: {status}")

    # 4. Salvar comparativo de exploração e caminhos
    caminho_visualizacao = pasta_figuras / "visualizacao_buscas_250.png"
    visualizar_comparacao_buscas(
        grafo,
        origem,
        destino,
        resultados,
        titulo=f"Exploração e Caminhos Solução na Rede Geográfica (n={n}, λ={lamb})",
        salvar_em=caminho_visualizacao,
    )
    print(f"Comparativo visual de buscas salvo em: {caminho_visualizacao}")


if __name__ == "__main__":
    main()
