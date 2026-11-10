"""Seleção determinística de pares de vértices para os experimentos de benchmark."""

import csv
import random
from pathlib import Path

from src.geographic import gerar_rede_geografica


def encontrar_componentes(grafo):
    """Retorna as componentes conexas do grafo como lista de listas de vértices."""
    visitados = set()
    componentes = []

    for inicio in grafo.adjacency:
        if inicio in visitados:
            continue

        pilha = [inicio]
        visitados.add(inicio)
        componente = []

        while pilha:
            atual = pilha.pop()
            componente.append(atual)

            for vizinho in grafo.neighbors(atual):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    pilha.append(vizinho)

        componentes.append(componente)

    return componentes


def selecionar_pares_comuns(n=2500, lambdas=(0.01, 0.02, 0.03), seed_rede=42, seed_pares=2026, qtd_pares=10):
    """Gera as redes e seleciona pares de vértices que estejam mutuamente conectados em todas as redes.

    Garante que os mesmos 10 pares (origem, destino) possam ser avaliados em todos os valores de lambda.
    """
    componentes_intersecao = None

    print("Identificando maior componente conexa interseccionada...")
    for lamb in lambdas:
        grafo = gerar_rede_geografica(quantidade_vertices=n, lamb=lamb, seed=seed_rede)
        comps = encontrar_componentes(grafo)
        maior = set(max(comps, key=len))
        print(f"  Lambda {lamb}: {len(maior)} vértices na maior componente ({100*len(maior)/n:.1f}%)")

        if componentes_intersecao is None:
            componentes_intersecao = maior
        else:
            componentes_intersecao = componentes_intersecao.intersection(maior)

    print(f"Vértices conectados em todas as 3 redes: {len(componentes_intersecao)}")

    # Sorteio determinístico
    rng = random.Random(seed_pares)
    candidatos = sorted(componentes_intersecao)
    sorteados = rng.sample(candidatos, qtd_pares * 2)

    pares = [
        (sorteados[i], sorteados[i + 1])
        for i in range(0, qtd_pares * 2, 2)
    ]

    # Salva arquivo CSV com caminho relativo portável
    pasta_saida = Path("outputs/tables")
    pasta_saida.mkdir(parents=True, exist_ok=True)
    arquivo_csv = pasta_saida / "pares_experimentos.csv"

    with open(arquivo_csv, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["par", "origem", "destino"])
        for i, (origem, destino) in enumerate(pares, start=1):
            escritor.writerow([i, origem, destino])

    print(f"\n{qtd_pares} pares salvos com sucesso em: {arquivo_csv}")
    for i, (origem, destino) in enumerate(pares, start=1):
        print(f"  Par {i:02d}: {origem} -> {destino}")

    return pares


if __name__ == "__main__":
    selecionar_pares_comuns()
