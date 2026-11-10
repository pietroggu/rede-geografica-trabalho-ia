"""Execução de benchmark dos algoritmos de busca nas redes geográficas."""

import csv
import math
import statistics
import time
from pathlib import Path

from src.algorithms.a_star import astar
from src.algorithms.best_first import best_first_search
from src.algorithms.bfs import bfs
from src.algorithms.dfs import dfs
from src.algorithms.dijkstra import dijkstra
from src.algorithms.hill_climbing import hill_climbing
from src.geographic import gerar_rede_geografica

# Configurações do experimento
N_VERTICES = 2500
LAMBDAS = [0.01, 0.02, 0.03]
SEED_REDE = 42
REPETICOES = 3

CAMINHO_PARES = Path("outputs/tables/pares_experimentos.csv")
PASTA_SAIDA = Path("outputs/tables")
PASTA_SAIDA.mkdir(parents=True, exist_ok=True)

ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "Best-First": best_first_search,
    "A*": astar,
    "Hill Climbing": hill_climbing,
    "Dijkstra": dijkstra,
}


def carregar_pares():
    """Carrega os pares pré-selecionados de origem e destino a partir do CSV."""
    pares = []
    with open(CAMINHO_PARES, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            pares.append({
                "par": int(linha["par"]),
                "origem": int(linha["origem"]),
                "destino": int(linha["destino"]),
            })
    return pares


def executar_benchmark_rede(grafo, pares, nome_rede):
    """Executa todos os algoritmos para cada par e coleta métricas de desempenho."""
    resultados = []

    for par in pares:
        origem = par["origem"]
        destino = par["destino"]

        print(f"\n[{nome_rede}] Par {par['par']:02d}: {origem} -> {destino}")

        for nome, algoritmo in ALGORITMOS.items():
            tempos = []
            caminho_final = []
            distancia_final = math.inf
            explorados_final = []

            for _ in range(REPETICOES):
                inicio = time.perf_counter()
                caminho, distancia, explorados = algoritmo(grafo, origem, destino)
                fim = time.perf_counter()

                tempos.append(fim - inicio)
                caminho_final = caminho
                distancia_final = distancia
                explorados_final = explorados

            sucesso = bool(caminho_final)
            saltos = len(caminho_final) - 1 if sucesso else None
            tempo_medio = statistics.mean(tempos) if tempos else None

            resultado = {
                "rede": nome_rede,
                "par": par["par"],
                "origem": origem,
                "destino": destino,
                "algoritmo": nome,
                "sucesso": sucesso,
                "distancia": distancia_final if sucesso else None,
                "saltos": saltos,
                "explorados": len(explorados_final),
                "tempo_medio": tempo_medio,
            }
            resultados.append(resultado)

            dist_txt = f"{distancia_final:.2f}" if sucesso else "Sem caminho"
            saltos_txt = str(saltos) if sucesso else "N/A"
            tempo_txt = f"{tempo_medio * 1000:.3f} ms" if tempo_medio is not None else "N/A"

            print(
                f"  {nome:14} | Sucesso: {str(sucesso):5} | Dist: {dist_txt:>10} | "
                f"Saltos: {saltos_txt:>4} | Exp: {len(explorados_final):>5} | Tempo: {tempo_txt:>10}"
            )

    return resultados


def salvar_resultados(resultados):
    """Salva a tabela de resultados individuais por par de vértices."""
    arquivo = PASTA_SAIDA / "resultados_benchmark.csv"
    campos = [
        "rede", "par", "origem", "destino", "algoritmo",
        "sucesso", "distancia", "saltos", "explorados", "tempo_medio",
    ]
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(resultados)
    print(f"\nResultados detalhados salvos em: {arquivo}")


def salvar_estatisticas(resultados):
    """Calcula médias e desvios consolidados por rede e algoritmo, salvando em CSV."""
    arquivo = PASTA_SAIDA / "estatisticas_benchmark.csv"
    campos = [
        "rede", "algoritmo", "taxa_sucesso",
        "distancia_media", "desvio_distancia",
        "saltos_medios", "explorados_medios",
        "tempo_medio_ms", "desvio_tempo_ms",
    ]
    estatisticas = []
    redes = sorted(set(r["rede"] for r in resultados))

    for rede in redes:
        for nome in ALGORITMOS:
            grupo = [r for r in resultados if r["rede"] == rede and r["algoritmo"] == nome]
            sucessos = [r for r in grupo if r["sucesso"]]

            distancias = [r["distancia"] for r in sucessos]
            saltos = [r["saltos"] for r in sucessos]
            explorados = [r["explorados"] for r in grupo if r["explorados"] is not None]
            tempos_ms = [r["tempo_medio"] * 1000 for r in grupo if r["tempo_medio"] is not None]

            estatisticas.append({
                "rede": rede,
                "algoritmo": nome,
                "taxa_sucesso": len(sucessos) / len(grupo) if grupo else 0.0,
                "distancia_media": statistics.mean(distancias) if distancias else None,
                "desvio_distancia": statistics.stdev(distancias) if len(distancias) > 1 else 0.0,
                "saltos_medios": statistics.mean(saltos) if saltos else None,
                "explorados_medios": statistics.mean(explorados) if explorados else None,
                "tempo_medio_ms": statistics.mean(tempos_ms) if tempos_ms else None,
                "desvio_tempo_ms": statistics.stdev(tempos_ms) if len(tempos_ms) > 1 else 0.0,
            })

    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(estatisticas)
    print(f"Estatísticas consolidadas salvas em: {arquivo}")


def main():
    pares = carregar_pares()
    print("=" * 60)
    print("INÍCIO DO BENCHMARK DE BUSCA EM REDES GEOGRÁFICAS")
    print(f"Vértices: {N_VERTICES} | Lambdas: {LAMBDAS} | Pares: {len(pares)} | Repetições: {REPETICOES}")
    print("=" * 60)

    todos_resultados = []

    for lamb in LAMBDAS:
        nome_rede = f"lambda_{lamb:.2f}"
        print("\n" + "=" * 60)
        print(f"Gerando rede geográfica: {nome_rede}...")
        inicio_geracao = time.perf_counter()
        grafo = gerar_rede_geografica(quantidade_vertices=N_VERTICES, lamb=lamb, seed=SEED_REDE)
        tempo_geracao = time.perf_counter() - inicio_geracao

        arestas = sum(len(v) for v in grafo.adjacency.values()) // 2
        grau_medio = 2 * arestas / N_VERTICES
        print(f"Rede construída em {tempo_geracao:.2f}s | Arestas: {arestas} | Grau Médio: {grau_medio:.2f}")

        resultados_rede = executar_benchmark_rede(grafo, pares, nome_rede)
        todos_resultados.extend(resultados_rede)

    salvar_resultados(todos_resultados)
    salvar_estatisticas(todos_resultados)
    print("\nBENCHMARK CONCLUÍDO COM SUCESSO.")


if __name__ == "__main__":
    main()
