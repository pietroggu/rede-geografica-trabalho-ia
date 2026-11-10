# Roteiro da Apresentação de 15 Minutos

**Disciplina:** SCC0230 — Inteligência Artificial (ICMC-USP)  
**Tema:** Abordagem A — Projeto de Busca em Redes (Rede Geográfica)  
**Duração Máxima:** 15 minutos (com participação obrigatória de todos os integrantes)  
**Arquivo de Slides:** [`outputs/apresentacao_busca_redes.pptx`](outputs/apresentacao_busca_redes.pptx)

---

## Divisão Sugerida Entre os 4 Integrantes

| Integrante | Slides | Tópicos Principais | Tempo Alocado |
| :--- | :---: | :--- | :---: |
| **Integrante 1** | Slides 1 a 3 | Capa, Contexto/Motivação e Modelagem Matemática da Rede Geográfica | ~3 min 30 s |
| **Integrante 2** | Slides 4 e 5 | Algoritmos de Busca Comparados e Visualização da Exploração (Item 4.4.i) | ~4 min |
| **Integrante 3** | Slides 6 a 8 | Metodologia Experimental (Item 4.4.ii), Distância Percorrida e Esforço Computacional | ~3 min 30 s |
| **Integrante 4** | Slides 9 a 12 | Comparativo A* vs. Dijkstra (Item 4.4.iii), Colapso do Hill Climbing, Matriz de Decisão e Conclusões | ~4 min |

---

## Roteiro Slide a Slide

### Bloco 1 — Integrante 1 (Slides 1 a 3 | ~3:30 min)

#### Slide 1 — Capa
- **Fala:** *"Boa tarde a todos, professor e colegas. Nosso grupo escolheu a Abordagem A da disciplina de Inteligência Artificial, focando na implementação e análise comparativa de algoritmos de busca clássicos e heurísticos aplicados ao modelo de Redes Geográficas."*

#### Slide 2 — Contexto e Motivação
- **Fala:** *"No mundo real, muitos dos problemas mais desafiadores de busca ocorrem em estruturas espaciais: rotas de transporte, redes elétricas e malhas de sensores. Diferente de grafos teóricos puramente abstratos, redes geográficas possuem restrições físicas: a distância geométrica impõe custos reais às conexões. Nosso objetivo foi construir um ambiente rigoroso para avaliar como diferentes algoritmos lidam com distâncias ponderadas e vazios topológicos."*

#### Slide 3 — Modelagem da Rede Geográfica (Apêndice A)
- **Fala:** *"Seguindo estritamente a especificação do Apêndice A do trabalho, geramos redes não-direcionadas onde $n$ vértices são distribuídos aleatoriamente no quadrado $[0, n] \times [0, n]$. A formação de arestas é probabilística e decai exponencialmente conforme a distância euclidiana $s_{uv}$, com $P(u \to v) = e^{-\lambda s_{uv}}$. O parâmetro $\lambda$ é crucial: quanto menor o $\lambda$, mais densa a rede com atalhos de longo alcance; quanto maior o $\lambda$, mais esparso e local se torna o grafo."*

---

### Bloco 2 — Integrante 2 (Slides 4 e 5 | ~4:00 min)

#### Slide 4 — Algoritmos de Busca em Análise
- **Fala:** *"Implementamos 6 algoritmos contemplando diferentes paradigmas: as buscas cegas BFS e DFS; as heurísticas Best-First e Hill Climbing; e as buscas ótimas Dijkstra e A\*. Todos os algoritmos informados utilizaram a distância euclidiana em linha reta como heurística $h(n)$, que é comprovadamente admissível e consistente no plano euclidiano."*

#### Slide 5 — Visualização da Exploração do Espaço de Busca (Item 4.4.i)
- **Fala:** *"Para atender ao Item 4.4.i, construímos uma visualização em uma rede com $n = 250$ nós. Neste slide, vemos claramente o comportamento de cada estratégia:
  - O **BFS** e o **Dijkstra** expandem isotropicamente em círculos, visitando praticamente todo o grafo (244 nós) até alcançar a meta.
  - O **DFS** perde-se em ramos profundos, gerando um caminho aberrante de 136 saltos e custo quase 17 vezes superior ao ótimo.
  - O **Best-First** e o **Hill Climbing** correm diretamente ao destino expandindo apenas 8 nós, mas aceitando uma rota ligeiramente subótima.
  - O **A\*** equilibra perfeitamente custo acumulado e heurística: expandiu apenas 74 nós e garantiu a rota ótima absoluta de distância 294.2."*

---

### Bloco 3 — Integrante 3 (Slides 6 a 8 | ~3:30 min)

#### Slide 6 — Metodologia Experimental (Item 4.4.ii)
- **Fala:** *"Para os experimentos quantitativos do Item 4.4.ii, geramos redes de grande porte com $n = 2500$ vértices nas três configurações exigidas: $\lambda = 0.01$ (grau médio 22.7), $\lambda = 0.02$ (grau médio 5.95) e $\lambda = 0.03$ (grau médio 2.72). Para garantir comparabilidade justa, identificamos a interseção das maiores componentes conexas e sorteamos 10 pares determinísticos de origem e destino avaliados em todas as redes, com 3 repetições cronometradas com `time.perf_counter`."*

#### Slide 7 — Análise de Distância Percorrida
- **Fala:** *"No gráfico de distâncias, observamos a primeira grande comprovação empírica: **o A\* e o Dijkstra obtiveram exatamente as mesmas distâncias médias em todas as instâncias** (1028 no denso, 1116 no intermediário e 1581 no esparso). O Best-First encontrou rotas de 15% a 30% maiores, enquanto o DFS gerou caminhos quilométricos na casa de centenas de milhares de unidades, confirmando sua completa inadequação para redes ponderadas."*

#### Slide 8 — Esforço Computacional: Nós Explorados e Tempo
- **Fala:** *"Avaliando os nós explorados em escala logarítmica, a diferença de eficiência é brutal. O Best-First e o A\* operam ordens de magnitude abaixo das buscas cegas. Em termos de tempo de execução, todos os algoritmos rodaram na faixa de milissegundos graças à implementação otimizada com min-heap."*

---

### Bloco 4 — Integrante 4 (Slides 9 a 12 | ~4:00 min)

#### Slide 9 — Comparativo Detalhado: A\* vs. Dijkstra (Item 4.4.iii)
- **Fala:** *"O Item 4.4.iii solicitou uma comparação aprofundada entre A\* e Dijkstra. Como ambos utilizam filas de prioridade e garantem o menor caminho, o diferencial está na **poda heurística**:
  - Na rede densa ($\lambda = 0.01$), o Dijkstra expandiu 1026.9 nós, enquanto o A\* expandiu apenas 27.4 nós — **uma redução de 37.5 vezes no espaço de busca**.
  - Esse afunilamento reduziu o tempo médio de 9.8 ms para apenas 0.66 ms, demonstrando o poder da informação heurística guiando a exploração."*

#### Slide 10 — O Caso Crítico do Hill Climbing
- **Fala:** *"O experimento revelou um fenômeno fascinante no Hill Climbing sem backtracking:
  - Na rede densa ($\lambda = 0.01$), ele teve 100% de sucesso porque a abundância de vizinhos permitiu contornar obstáculos.
  - Na rede média ($\lambda = 0.02$), sua taxa caiu para 50%.
  - Na rede esparsa ($\lambda = 0.03$), **sua taxa de sucesso desabou para 0%**. Sem backtracking, qualquer vazio espacial cria um mínimo local onde nenhum vizinho aproxima o agente do destino, travando o algoritmo."*

#### Slide 11 — Síntese dos Resultados e Matriz de Decisão
- **Fala:** *"Sintetizamos os resultados nesta matriz de trade-offs. Se a aplicação exige caminho mínimo absoluto com eficiência computacional, o **A\*** é a escolha definitiva. Se a meta é tempo de resposta imediato e tolera-se pequena subotimalidade, o **Best-First** se destaca. O Hill Climbing puro só é viável sob alta densidade ou se enriquecido com reinícios aleatórios."*

#### Slide 12 — Conclusões e Encerramento
- **Fala:** *"Concluímos validando todas as hipóteses teóricas em uma rede espacial estocástica realista. O código, os dados e a documentação completa estão disponíveis no repositório. Agradecemos a atenção de todos e estamos prontos para as perguntas."*
