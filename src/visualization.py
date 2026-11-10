"""Módulo de visualização para topologia de redes e exploração dos algoritmos de busca."""

import math
import matplotlib.pyplot as plt


def visualizar_topologia_rede(grafo, componentes=None, titulo="Rede Geográfica", salvar_em=None):
    """Gera visualização da estrutura da rede e suas componentes conexas.

    Args:
        grafo: Instância de Graph.
        componentes: Lista de conjuntos/listas de vértices por componente conexa.
        titulo: Título da figura.
        salvar_em: Caminho opcional para salvar o arquivo de imagem.
    """
    fig, ax = plt.subplots(figsize=(9, 8))

    cores = {}
    if componentes:
        maior_componente = set(max(componentes, key=len))
        for comp in componentes:
            for v in comp:
                cores[v] = "#1f77b4" if v in maior_componente else "#ff7f0e"
    else:
        for v in grafo.adjacency:
            cores[v] = "#1f77b4"

    # Arestas
    for u in grafo.adjacency:
        x1, y1 = grafo.get_position(u)
        for v in grafo.neighbors(u):
            if u < v:
                x2, y2 = grafo.get_position(v)
                ax.plot([x1, x2], [y1, y2], color="#cccccc", alpha=0.4, linewidth=0.7, zorder=1)

    # Vértices
    xs = [grafo.get_position(v)[0] for v in grafo.adjacency]
    ys = [grafo.get_position(v)[1] for v in grafo.adjacency]
    c_list = [cores[v] for v in grafo.adjacency]

    ax.scatter(xs, ys, c=c_list, s=28, edgecolors="none", zorder=2)

    ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xlabel("Coordenada X")
    ax.set_ylabel("Coordenada Y")
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    if salvar_em:
        plt.savefig(salvar_em, dpi=300, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()


def visualizar_comparacao_buscas(grafo, origem, destino, resultados, titulo="Comparação dos Algoritmos de Busca", salvar_em=None):
    """Gera painel comparativo (2x3) ilustrando o espaço explorado e o caminho solução de cada algoritmo.

    Args:
        grafo: Instância de Graph.
        origem: Vértice de partida.
        destino: Vértice de chegada.
        resultados: Dicionário no formato:
            {nome_algoritmo: (caminho, distancia, explorados)}
        titulo: Título geral da figura.
        salvar_em: Caminho opcional para salvar a imagem gerada.
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()

    algoritmos = list(resultados.items())

    for idx, (nome, (caminho, distancia, explorados)) in enumerate(algoritmos):
        ax = axes[idx]

        # 1. Desenho das arestas da rede em fundo suave
        for u in grafo.adjacency:
            x1, y1 = grafo.get_position(u)
            for v in grafo.neighbors(u):
                if u < v:
                    x2, y2 = grafo.get_position(v)
                    ax.plot([x1, x2], [y1, y2], color="#e0e0e0", alpha=0.35, linewidth=0.6, zorder=1)

        # 2. Todos os vértices do grafo
        all_x = [grafo.get_position(v)[0] for v in grafo.adjacency]
        all_y = [grafo.get_position(v)[1] for v in grafo.adjacency]
        ax.scatter(all_x, all_y, color="#c7c7c7", s=15, alpha=0.5, zorder=2)

        # 3. Vértices explorados pelo algoritmo
        if explorados:
            exp_x = [grafo.get_position(v)[0] for v in explorados]
            exp_y = [grafo.get_position(v)[1] for v in explorados]
            ax.scatter(exp_x, exp_y, color="#ff9800", s=30, alpha=0.65, label=f"Explorados ({len(explorados)})", zorder=3)

        # 4. Caminho final percorrido
        if caminho:
            caminho_x = [grafo.get_position(v)[0] for v in caminho]
            caminho_y = [grafo.get_position(v)[1] for v in caminho]
            ax.plot(caminho_x, caminho_y, color="#d32f2f", linewidth=2.8, alpha=0.9, label="Caminho Solução", zorder=4)
            ax.scatter(caminho_x, caminho_y, color="#b71c1c", s=40, zorder=5)

        # 5. Origem e Destino
        xo, yo = grafo.get_position(origem)
        xd, yd = grafo.get_position(destino)
        ax.scatter([xo], [yo], color="#2e7d32", s=130, marker="^", label="Origem", edgecolors="black", linewidth=1.2, zorder=6)
        ax.scatter([xd], [yd], color="#6a1b9a", s=130, marker="*", label="Destino", edgecolors="black", linewidth=1.2, zorder=6)

        # Configuração do subtítulo com métricas
        if math.isinf(distancia) or not caminho:
            subtitulo = f"{nome}\nFalha / Mínimo Local | Explorados: {len(explorados)}"
        else:
            saltos = len(caminho) - 1
            subtitulo = f"{nome}\nDistância: {distancia:.2f} | Saltos: {saltos} | Explorados: {len(explorados)}"

        ax.set_title(subtitulo, fontsize=11, fontweight="bold", pad=8)
        ax.set_aspect("equal", adjustable="datalim")
        ax.grid(True, linestyle=":", alpha=0.4)
        ax.legend(loc="upper right", fontsize=8, framealpha=0.85)

    # Ocultar eixos excedentes se houver
    for j in range(len(algoritmos), len(axes)):
        axes[j].axis("off")

    fig.suptitle(titulo, fontsize=15, fontweight="bold", y=0.99)
    plt.tight_layout()

    if salvar_em:
        plt.savefig(salvar_em, dpi=300, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()
