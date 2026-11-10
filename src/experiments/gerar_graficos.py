"""Gera gráficos consolidados das métricas de benchmark para slides e relatório."""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

PASTA_TABELAS = Path("outputs/tables")
PASTA_FIGURAS = Path("outputs/figures")
PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)


def carregar_estatisticas():
    arquivo = PASTA_TABELAS / "estatisticas_benchmark.csv"
    dados = []
    with open(arquivo, newline="", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados.append({
                "rede": linha["rede"],
                "algoritmo": linha["algoritmo"],
                "taxa_sucesso": float(linha["taxa_sucesso"]),
                "distancia_media": float(linha["distancia_media"]) if linha["distancia_media"] else 0.0,
                "desvio_distancia": float(linha["desvio_distancia"]) if linha["desvio_distancia"] else 0.0,
                "saltos_medios": float(linha["saltos_medios"]) if linha["saltos_medios"] else 0.0,
                "explorados_medios": float(linha["explorados_medios"]) if linha["explorados_medios"] else 0.0,
                "tempo_medio_ms": float(linha["tempo_medio_ms"]) if linha["tempo_medio_ms"] else 0.0,
                "desvio_tempo_ms": float(linha["desvio_tempo_ms"]) if linha["desvio_tempo_ms"] else 0.0,
            })
    return dados


def plot_distancia(dados):
    """Gráfico de distância média com desvio padrão (sem DFS para não estourar a escala)."""
    fig, ax = plt.subplots(figsize=(10, 6))

    redes = sorted(set(d["rede"] for d in dados))
    # Exclui DFS devido à escala quilométrica de caminhos desnecessários
    algoritmos = ["BFS", "Best-First", "A*", "Hill Climbing", "Dijkstra"]
    cores = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e"]

    x = np.arange(len(redes))
    width = 0.15

    for i, algo in enumerate(algoritmos):
        valores = []
        erros = []
        for r in redes:
            item = next((d for d in dados if d["rede"] == r and d["algoritmo"] == algo), None)
            valores.append(item["distancia_media"] if item and item["distancia_media"] > 0 else 0)
            erros.append(item["desvio_distancia"] if item and item["distancia_media"] > 0 else 0)

        offset = (i - len(algoritmos) / 2 + 0.5) * width
        ax.bar(x + offset, valores, width, yerr=erros, capsize=4, label=algo, color=cores[i], alpha=0.9)

    rotulos_redes = ["λ = 0.01 (Densa)", "λ = 0.02 (Média)", "λ = 0.03 (Esparsa)"]
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos_redes, fontsize=11, fontweight="bold")
    ax.set_ylabel("Distância Euclidiana Média", fontsize=11, fontweight="bold")
    ax.set_title("Distância Média Percorrida por Algoritmo (n=2500)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")

    plt.tight_layout()
    caminho = PASTA_FIGURAS / "benchmark_distancia.png"
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    print(f"Gráfico de distância salvo em: {caminho}")


def plot_explorados(dados):
    """Gráfico de nós explorados (escala logarítmica)."""
    fig, ax = plt.subplots(figsize=(10, 6))

    redes = sorted(set(d["rede"] for d in dados))
    algoritmos = ["BFS", "DFS", "Best-First", "A*", "Hill Climbing", "Dijkstra"]
    cores = ["#1f77b4", "#8c564b", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e"]

    x = np.arange(len(redes))
    width = 0.13

    for i, algo in enumerate(algoritmos):
        valores = []
        for r in redes:
            item = next((d for d in dados if d["rede"] == r and d["algoritmo"] == algo), None)
            valores.append(item["explorados_medios"] if item else 1)

        offset = (i - len(algoritmos) / 2 + 0.5) * width
        ax.bar(x + offset, valores, width, label=algo, color=cores[i], alpha=0.9)

    rotulos_redes = ["λ = 0.01 (Densa)", "λ = 0.02 (Média)", "λ = 0.03 (Esparsa)"]
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos_redes, fontsize=11, fontweight="bold")
    ax.set_yscale("log")
    ax.set_ylabel("Nós Explorados Médios (Escala Logarítmica)", fontsize=11, fontweight="bold")
    ax.set_title("Eficiência de Espaço de Busca: Vértices Explorados (n=2500)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", linestyle="--", alpha=0.4, axis="y")

    plt.tight_layout()
    caminho = PASTA_FIGURAS / "benchmark_explorados.png"
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    print(f"Gráfico de nós explorados salvo em: {caminho}")


def plot_tempo(dados):
    """Gráfico de tempo de execução médio em milissegundos."""
    fig, ax = plt.subplots(figsize=(10, 6))

    redes = sorted(set(d["rede"] for d in dados))
    algoritmos = ["BFS", "DFS", "Best-First", "A*", "Hill Climbing", "Dijkstra"]
    cores = ["#1f77b4", "#8c564b", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e"]

    x = np.arange(len(redes))
    width = 0.13

    for i, algo in enumerate(algoritmos):
        valores = []
        for r in redes:
            item = next((d for d in dados if d["rede"] == r and d["algoritmo"] == algo), None)
            valores.append(item["tempo_medio_ms"] if item else 0)

        offset = (i - len(algoritmos) / 2 + 0.5) * width
        ax.bar(x + offset, valores, width, label=algo, color=cores[i], alpha=0.9)

    rotulos_redes = ["λ = 0.01 (Densa)", "λ = 0.02 (Média)", "λ = 0.03 (Esparsa)"]
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos_redes, fontsize=11, fontweight="bold")
    ax.set_ylabel("Tempo de Execução Médio (ms)", fontsize=11, fontweight="bold")
    ax.set_title("Desempenho Temporal Médio por Algoritmo (n=2500)", fontsize=13, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")

    plt.tight_layout()
    caminho = PASTA_FIGURAS / "benchmark_tempo.png"
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    print(f"Gráfico de tempo salvo em: {caminho}")


def plot_taxa_sucesso(dados):
    """Gráfico de taxa de sucesso enfatizando as limitações do Hill Climbing."""
    fig, ax = plt.subplots(figsize=(8, 5))

    redes = sorted(set(d["rede"] for d in dados))
    rotulos_redes = ["λ = 0.01\n(Densa)", "λ = 0.02\n(Média)", "λ = 0.03\n(Esparsa)"]
    hc_sucesso = []

    for r in redes:
        item = next(d for d in dados if d["rede"] == r and d["algoritmo"] == "Hill Climbing")
        hc_sucesso.append(item["taxa_sucesso"] * 100)

    x = np.arange(len(redes))
    barras = ax.bar(x, hc_sucesso, width=0.45, color="#9467bd", alpha=0.9, edgecolor="black")

    ax.axhline(100, color="#2ca02c", linestyle="--", linewidth=1.5, label="Outros Algoritmos (100% Sucesso)")

    for barra in barras:
        altura = barra.get_height()
        ax.annotate(f"{altura:.0f}%",
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontweight="bold", fontsize=11)

    ax.set_xticks(x)
    ax.set_xticklabels(rotulos_redes, fontsize=11)
    ax.set_ylabel("Taxa de Sucesso (%)", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 115)
    ax.set_title("Taxa de Sucesso do Hill Climbing sem Backtracking (n=2500)", fontsize=12, fontweight="bold", pad=12)
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")

    plt.tight_layout()
    caminho = PASTA_FIGURAS / "benchmark_sucesso.png"
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    print(f"Gráfico de taxa de sucesso salvo em: {caminho}")


def plot_comparativo_astar_dijkstra(dados):
    """Comparação direta entre A* e Dijkstra (Item 4.4.iii)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    redes = sorted(set(d["rede"] for d in dados))
    rotulos = ["λ = 0.01 (Densa)", "λ = 0.02 (Média)", "λ = 0.03 (Esparsa)"]
    x = np.arange(len(redes))
    width = 0.35

    astar_exp = [next(d for d in dados if d["rede"] == r and d["algoritmo"] == "A*")["explorados_medios"] for r in redes]
    dijk_exp = [next(d for d in dados if d["rede"] == r and d["algoritmo"] == "Dijkstra")["explorados_medios"] for r in redes]

    # Subplot 1: Nós explorados
    ax1.bar(x - width/2, astar_exp, width, label="A*", color="#d62728", alpha=0.9)
    ax1.bar(x + width/2, dijk_exp, width, label="Dijkstra", color="#ff7f0e", alpha=0.9)
    ax1.set_xticks(x)
    ax1.set_xticklabels(rotulos, fontsize=10, fontweight="bold")
    ax1.set_ylabel("Vértices Explorados Médios", fontsize=11, fontweight="bold")
    ax1.set_title("Espaço de Busca Explorado (Poda Heurística)", fontsize=12, fontweight="bold")
    ax1.legend(fontsize=11)
    ax1.grid(True, linestyle="--", alpha=0.4, axis="y")

    for i in range(len(redes)):
        fator = dijk_exp[i] / astar_exp[i]
        ax1.annotate(f"{fator:.1f}x menos", xy=(x[i] - width/2, astar_exp[i]),
                     xytext=(0, 5), textcoords="offset points", ha="center", fontsize=9, fontweight="bold", color="#b71c1c")

    # Subplot 2: Tempo médio
    astar_tempo = [next(d for d in dados if d["rede"] == r and d["algoritmo"] == "A*")["tempo_medio_ms"] for r in redes]
    dijk_tempo = [next(d for d in dados if d["rede"] == r and d["algoritmo"] == "Dijkstra")["tempo_medio_ms"] for r in redes]

    ax2.bar(x - width/2, astar_tempo, width, label="A*", color="#d62728", alpha=0.9)
    ax2.bar(x + width/2, dijk_tempo, width, label="Dijkstra", color="#ff7f0e", alpha=0.9)
    ax2.set_xticks(x)
    ax2.set_xticklabels(rotulos, fontsize=10, fontweight="bold")
    ax2.set_ylabel("Tempo de Execução Médio (ms)", fontsize=11, fontweight="bold")
    ax2.set_title("Tempo de Processamento (Heap)", fontsize=12, fontweight="bold")
    ax2.legend(fontsize=11)
    ax2.grid(True, linestyle="--", alpha=0.4, axis="y")

    fig.suptitle("Item 4.4.iii: Comparativo Detalhado A* vs. Dijkstra", fontsize=14, fontweight="bold")
    plt.tight_layout()
    caminho = PASTA_FIGURAS / "comparativo_astar_dijkstra.png"
    plt.savefig(caminho, dpi=300)
    plt.close(fig)
    print(f"Comparativo A* vs Dijkstra salvo em: {caminho}")


def main():
    dados = carregar_estatisticas()
    plot_distancia(dados)
    plot_explorados(dados)
    plot_tempo(dados)
    plot_taxa_sucesso(dados)
    plot_comparativo_astar_dijkstra(dados)
    print("Todos os gráficos foram gerados com sucesso!")


if __name__ == "__main__":
    main()
