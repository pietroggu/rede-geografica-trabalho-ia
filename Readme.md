# SCC0230 — Inteligência Artificial: Busca em Redes Geográficas

Este repositório contém a implementação completa do trabalho prático da disciplina **SCC0230 — Inteligência Artificial (ICMC-USP)**. O projeto segue a **Abordagem A (Projeto de Busca em Redes)**, aplicando e avaliando seis algoritmos de busca clássicos e heurísticos sobre o modelo de **Redes Geográficas**.

---

## 1. Visão Geral da Modelagem

### 1.1 Rede Geográfica (Apêndice A)
Diferente de modelos de grafos aleatórios clássicos (Erdős–Rényi), a rede geográfica modela restrições espaciais reais:
- Cada vértice $v \in V$ recebe coordenadas $(x, y)$ uniformemente distribuídas no plano bidimensional $[0, n] \times [0, n]$, onde $n$ é o número total de vértices.
- Para cada par de vértices $(u, v)$, a probabilidade de conexão decai exponencialmente em função da distância geométrica euclidiana $s_{uv}$:
  $$P(u \to v) = e^{-\lambda s_{uv}}$$
- O peso de cada aresta estabelecida corresponde à própria distância geométrica $s_{uv}$.
- Parâmetro $\lambda$: controla a taxa de decaimento espacial. Valores menores geram redes densas com arestas de longo alcance; valores maiores favorecem conexões estritamente locais (redes esparsas).

### 1.2 Algoritmos de Busca Avaliados
1. **Busca em Largura (BFS):** Busca cega que garante o caminho ótimo em número de saltos (arestas).
2. **Busca em Profundidade (DFS):** Busca cega iterativa que explora ramos até a profundidade máxima antes do retrocesso.
3. **Busca Gulosa pela Melhor Escolha (Best-First):** Busca informada orientada estritamente pela estimativa heurística $h(n)$ da distância em linha reta até o destino.
4. **Algoritmo A\* (A-Estrela):** Busca heurística com função de avaliação $f(n) = g(n) + h(n)$, garantindo otimalidade de custo acumulado com heurística euclidiana admissível e consistente.
5. **Hill Climbing (sem backtracking):** Otimização local estrita que transita unicamente para o vizinho com menor distância euclidiana ao destino, falhando em mínimos locais e platôs.
6. **Algoritmo de Dijkstra (Opcional):** Algoritmo de caminho de custo mínimo ótimo, implementado com fila de prioridade (*min-heap*) para comparação justa com o A\*.

---

## 2. Estrutura do Projeto

```text
projeto IA/
├── README.md                          # Documentação técnica e instruções
├── requirements.txt                   # Dependências do projeto
├── Trabalho IA.pdf                    # Especificação oficial do trabalho
├── src/
│   ├── main.py                        # Ponto de entrada e interface CLI
│   ├── geographic.py                  # Gerador estocástico da rede geográfica
│   ├── visualization.py               # Módulo de renderização gráfica
│   ├── core/
│   │   ├── graph.py                   # Estrutura de dados do Grafo
│   │   └── result.py                  # Dataclass de resultados de busca
│   ├── algorithms/                    # Implementações dos 6 algoritmos de busca
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── best_first.py
│   │   ├── a_star.py
│   │   ├── hill_climbing.py
│   │   └── dijkstra.py
│   └── experiments/                   # Scripts de benchmarking e análise
│       ├── selecionar_vertices.py     # Seleção dos 10 pares na maior componente
│       ├── executar_buscas.py         # Execução das baterias de testes em n=2500
│       ├── gerar_visualizacao_busca.py# Visualização do espaço de busca em n=250
│       └── gerar_graficos.py          # Geração dos gráficos comparativos
└── outputs/
    ├── figures/                       # Imagens e plots gerados (300 DPI)
    └── tables/                        # Tabelas CSV com métricas e estatísticas
```

---

## 3. Instalação e Requisitos

O projeto requer **Python 3.10+**.

```bash
# Instalação das dependências
pip install -r requirements.txt
```

---

## 4. Reprodução dos Experimentos

O arquivo `src/main.py` provê comandos para reproduzir cada etapa:

```bash
# 1. Demonstração rápida dos 6 algoritmos em grafo de teste
python -m src.main --demo

# 2. Experimento 4.4.i: Gerar visualização dos caminhos e nós explorados (n=250)
python -m src.main --visualizar

# 3. Experimentos 4.4.ii e 4.4.iii: Executar benchmark completo (n=2500) e gerar gráficos
python -m src.main --benchmark

# 4. Execução completa automatizada de todo o fluxo
python -m src.main --tudo
```

---

## 5. Resumo dos Resultados Experimentais

### 5.1 Comparativo Geral (Rede com $n = 2500$ vértices, 10 pares de teste)

| Rede | Algoritmo | Sucesso (%) | Distância Média | Saltos Médios | Vértices Explorados | Tempo Médio (ms) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **$\lambda = 0.01$**<br>(Densa, grau 22.7) | **A\*** | 100% | **1028.58** | 6.3 | **27.4** | 0.66 ms |
| | **Dijkstra** | 100% | **1028.58** | 6.3 | 1026.9 | 9.81 ms |
| | **Best-First** | 100% | 1227.75 | 4.5 | **5.5** | 0.17 ms |
| | **BFS** | 100% | 1175.79 | **3.7** | 1022.4 | 3.01 ms |
| | **Hill Climbing** | 100% | 1227.75 | 4.5 | 5.5 | 0.07 ms |
| | **DFS** | 100% | 308938.49 | 1590.5 | 1611.1 | 4.87 ms |
| **$\lambda = 0.02$**<br>(Média, grau 5.95) | **A\*** | 100% | **1116.98** | 11.8 | **102.3** | 0.70 ms |
| | **Dijkstra** | 100% | **1116.98** | 11.8 | 1017.7 | 3.70 ms |
| | **Best-First** | 100% | 1353.33 | 11.7 | **13.9** | 0.12 ms |
| | **BFS** | 100% | 1416.36 | **8.6** | 1034.9 | 1.30 ms |
| | **Hill Climbing** | 50% | 1184.41 | 10.4 | 10.7 | 0.06 ms |
| | **DFS** | 100% | 129370.72 | 1279.1 | 1612.3 | 2.79 ms |
| **$\lambda = 0.03$**<br>(Esparsa, grau 2.72) | **A\*** | 100% | **1581.41** | 21.4 | **295.7** | 1.23 ms |
| | **Dijkstra** | 100% | **1581.41** | 21.4 | 897.0 | 2.57 ms |
| | **Best-First** | 100% | 2052.19 | 26.3 | **49.1** | 0.24 ms |
| | **BFS** | 100% | 1687.67 | **19.3** | 844.7 | 1.05 ms |
| | **Hill Climbing** | 0% | — | — | 5.2 | 0.02 ms |
| | **DFS** | 100% | 17373.82 | 244.6 | 1221.3 | 2.52 ms |

### 5.2 Principais Conclusões
- **Otimalidade:** A\* e Dijkstra comprovaram formalmente a otimalidade de distância em todas as topologias, com distâncias idênticas para todos os pares.
- **Poda Heurística (A\* vs. Dijkstra):** O A\* explorou até **37 vezes menos vértices** que o Dijkstra ($\lambda = 0.01$), reduzindo drasticamente o tempo de processamento graças à heurística euclidiana admissível e consistente.
- **Vulnerabilidade do Hill Climbing:** Conforme a rede se torna mais esparsa ($\lambda = 0.03$), o número de rotas alternativas diminui, fazendo a taxa de sucesso do Hill Climbing despencar de 100% para 0% devido a armadilhas de mínimos locais.
- **Ineficiência do DFS:** O DFS apresentou caminhos de custo centenas de vezes superiores ao ótimo, provando-se totalmente inadequado para busca de rotas ponderadas em redes espaciais.
