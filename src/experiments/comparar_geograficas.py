
from src.geographic import gerar_rede_geografica


def encontrar_componentes(grafo):
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


N = 2500
LAMBDA = 0.03
SEED = 42

grafo = gerar_rede_geografica(
    quantidade_vertices=N,
    lamb=LAMBDA,
    seed=SEED
)

arestas = sum(
    len(vizinhos)
    for vizinhos in grafo.adjacency.values()
) // 2

componentes = encontrar_componentes(grafo)

maior = max(componentes, key=len)

grau_medio = 2 * arestas / N

densidade = 2 * arestas / (N * (N - 1))

print("===== REDE GEOGRÁFICA DEFINITIVA =====")
print("Vértices:", N)
print("Lambda:", LAMBDA)
print("Arestas:", arestas)
print("Grau médio:", round(grau_medio, 4))
print("Densidade:", round(densidade, 6))
print("Componentes conexas:", len(componentes))
print("Maior componente:", len(maior))
print(
    "Percentual na maior componente:",
    round(100 * len(maior) / N, 2),
    "%"
)
