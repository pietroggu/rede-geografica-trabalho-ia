"""Gerador automatizado de apresentação em formato PowerPoint (.pptx).

Cria uma apresentação widescreen 16:9 com padrão visual profissional,
contendo gráficos, tabelas e sínteses para a apresentação de 15 minutos da disciplina SCC0230.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Paleta de cores moderna (Corporate Navy & Slate)
COR_NAVY_ESCURO = RGBColor(15, 23, 42)    # #0F172A
COR_NAVY_MEDIO = RGBColor(30, 41, 59)     # #1E293B
COR_AZUL_ACCENT = RGBColor(37, 99, 235)   # #2563EB
COR_AZUL_CLARO = RGBColor(239, 246, 255)  # #EFF6FF
COR_CINZA_TEXTO = RGBColor(51, 65, 85)    # #334155
COR_CINZA_BORDA = RGBColor(226, 232, 240) # #E2E8F0
COR_BRANCO = RGBColor(255, 255, 255)
COR_VERDE = RGBColor(22, 101, 52)         # #166534
COR_VERMELHO = RGBColor(153, 27, 27)      # #991B1B


def criar_apresentacao():
    prs = Presentation()
    # Padrão widescreen 16:9 (13.333 x 7.5 polegadas)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    pasta_figuras = Path("outputs/figures")
    caminho_saida = Path("outputs/apresentacao_busca_redes.pptx")

    def adicionar_slide_base(titulo, subtitulo=None):
        slide = prs.slides.add_slide(blank_layout)

        # Barra de topo / cabeçalho
        topo = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        topo.fill.solid()
        topo.fill.fore_color.rgb = COR_NAVY_ESCURO
        topo.line.color.rgb = COR_NAVY_ESCURO

        # Linha de acento azul sob o cabeçalho
        linha = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        linha.fill.solid()
        linha.fill.fore_color.rgb = COR_AZUL_ACCENT
        linha.line.color.rgb = COR_AZUL_ACCENT

        # Caixa de texto do cabeçalho
        txbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.95))
        tf = txbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = titulo
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COR_BRANCO

        if subtitulo:
            p2 = tf.add_paragraph()
            p2.text = subtitulo
            p2.font.size = Pt(12)
            p2.font.color.rgb = RGBColor(148, 163, 184) # Cinza azulado claro

        # Rodapé
        rodape = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.35))
        tf_rod = rodape.text_frame
        p_rod = tf_rod.paragraphs[0]
        p_rod.text = "SCC0230 — Inteligência Artificial (ICMC-USP) | Abordagem A: Busca em Redes Geográficas"
        p_rod.font.size = Pt(9)
        p_rod.font.color.rgb = RGBColor(100, 116, 139)

        return slide

    # =========================================================================
    # SLIDE 1: Capa
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COR_NAVY_ESCURO
    bg.line.color.rgb = COR_NAVY_ESCURO

    faixa = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(4.3), Inches(13.333), Inches(0.08))
    faixa.fill.solid()
    faixa.fill.fore_color.rgb = COR_AZUL_ACCENT
    faixa.line.color.rgb = COR_AZUL_ACCENT

    # Título da Capa
    tx_capa = slide1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(10.9), Inches(2.4))
    tf_capa = tx_capa.text_frame
    tf_capa.word_wrap = True
    p = tf_capa.paragraphs[0]
    p.text = "Busca em Redes Geográficas"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COR_BRANCO

    p_sub = tf_capa.add_paragraph()
    p_sub.text = "Implementação, Visualização e Avaliação Comparativa de Algoritmos de Busca"
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = RGBColor(147, 197, 253)

    # Detalhes e Integrantes
    tx_det = slide1.shapes.add_textbox(Inches(1.2), Inches(4.6), Inches(10.9), Inches(2.2))
    tf_det = tx_det.text_frame
    p_disc = tf_det.paragraphs[0]
    p_disc.text = "SCC0230 — Inteligência Artificial | ICMC - USP"
    p_disc.font.size = Pt(14)
    p_disc.font.bold = True
    p_disc.font.color.rgb = COR_BRANCO

    p_int = tf_det.add_paragraph()
    p_int.text = "Abordagem A — Projeto de Busca em Redes (Rede Geográfica)\nEquipe: 4 Integrantes | Novembro de 2026"
    p_int.font.size = Pt(13)
    p_int.font.color.rgb = RGBColor(203, 213, 225)

    # =========================================================================
    # SLIDE 2: Contexto e Motivação
    # =========================================================================
    slide2 = adicionar_slide_base("1. Contexto e Motivação", "Por que avaliar buscas em redes espaciais e geográficas?")

    def criar_card(slide, left, top, width, height, titulo, pontos, cor_fundo=COR_AZUL_CLARO, cor_borda=COR_AZUL_ACCENT):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = cor_fundo
        card.line.color.rgb = cor_borda
        card.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = titulo
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = COR_NAVY_ESCURO

        for pt in pontos:
            p_pt = tf.add_paragraph()
            p_pt.text = f"• {pt}"
            p_pt.font.size = Pt(12)
            p_pt.font.color.rgb = COR_CINZA_TEXTO
            p_pt.space_before = Pt(6)

    criar_card(
        slide2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.1),
        "Redes no Mundo Real",
        [
            "Redes de transporte urbano e rodovias.",
            "Infraestrutura de telecomunicações e fibra óptica.",
            "Malhas de sensores sem fio (IoT) e distribuição de energia.",
            "A proximidade geográfica dita a conectividade física."
        ]
    )

    criar_card(
        slide2, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.1),
        "O Desafio Computacional",
        [
            "Espaço de estados contínuo mapeado em topologia discreta.",
            "Arestas possuem custos geométricos variáveis.",
            "A presença de obstáculos ou vazios espaciais gera mínimos locais.",
            "Necessidade de balancear tempo de resposta e otimalidade."
        ]
    )

    criar_card(
        slide2, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.1),
        "Objetivos do Projeto",
        [
            "Implementar gerador estocástico fiel de Redes Geográficas.",
            "Avaliar 6 algoritmos de busca (cegos, gulosos e ótimos).",
            "Visualizar o espaço de exploração dos algoritmos (Item 4.4.i).",
            "Analisar o impacto da densidade espacial (Item 4.4.ii).",
            "Comparar formalmente A* versus Dijkstra (Item 4.4.iii)."
        ]
    )

    # =========================================================================
    # SLIDE 3: Modelo Matemático da Rede Geográfica
    # =========================================================================
    slide3 = adicionar_slide_base("2. Modelagem da Rede Geográfica", "Especificação rigorosa conforme Apêndice A do enunciado")

    # Caixa esquerda com formulação
    caixa_formula = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.1))
    caixa_formula.fill.solid()
    caixa_formula.fill.fore_color.rgb = COR_BRANCO
    caixa_formula.line.color.rgb = COR_CINZA_BORDA
    caixa_formula.line.width = Pt(1.5)

    tx_f = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.7))
    tf_f = tx_f.text_frame
    tf_f.word_wrap = True

    p = tf_f.paragraphs[0]
    p.text = "Definição Estocástica Espacial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COR_NAVY_ESCURO

    itens_f = [
        ("Distribuição dos Vértices:", "Para cada vértice v in V, suas coordenadas (x, y) são sorteadas uniformemente no plano limitado [0, n] x [0, n], onde n é o total de nós."),
        ("Probabilidade de Conexão:", "Para todo par de vértices (u, v), a existência de uma aresta obedece à distribuição exponencial decrescente:"),
        ("P(u -> v) = exp(-λ * s_uv)", "onde s_uv é a distância euclidiana euclidiana euclidiana."),
        ("Peso da Aresta:", "w(u, v) = s_uv (distância geométrica real)."),
        ("Papel do Parâmetro λ:", "λ pequeno (0.01) gera conexões de longo alcance (rede densa). λ maior (0.03) restringe arestas a vizinhos estritamente próximos (rede esparsa).")
    ]
    for tit, desc in itens_f:
        p_i = tf_f.add_paragraph()
        p_i.text = f"{tit} {desc}"
        p_i.font.size = Pt(11.5)
        p_i.font.color.rgb = COR_CINZA_TEXTO
        p_i.space_before = Pt(8)

    # Imagem da topologia à direita
    img_topo = pasta_figuras / "topologia_rede_250.png"
    if img_topo.exists():
        slide3.shapes.add_picture(str(img_topo), Inches(7.1), Inches(1.6), width=Inches(5.4))

    # =========================================================================
    # SLIDE 4: Algoritmos de Busca Comparados
    # =========================================================================
    slide4 = adicionar_slide_base("3. Algoritmos de Busca em Análise", "Comparação de estratégias cegas, heurísticas e ótimas")

    # Tabela comparativa dos 6 algoritmos
    linhas, colunas = 7, 5
    tabela_shape = slide4.shapes.add_table(linhas, colunas, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.9))
    tbl = tabela_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(2.0)
    tbl.columns[2].width = Inches(2.5)
    tbl.columns[3].width = Inches(2.5)
    tbl.columns[4].width = Inches(2.5)

    cabecalhos = ["Algoritmo", "Tipo de Busca", "Critério de Seleção", "Garantia de Custo", "Vulnerabilidade / Obs."]
    dados_algos = [
        ["BFS (Largura)", "Cega (Não informada)", "Fila FIFO (ordem de chegada)", "Ótimo em saltos (arestas)", "Ignora pesos; alto consumo de memória"],
        ["DFS (Profundidade)", "Cega (Não informada)", "Pilha LIFO (profundidade)", "Não ótimo (subótimo)", "Gera caminhos quilométricos aberrantes"],
        ["Best-First", "Informada (Heurística)", "Fila de Prioridade: min h(n)", "Não ótimo", "Rápido, mas suscetível a desvios locais"],
        ["Hill Climbing", "Otimização Local", "Melhor vizinho imediato", "Não ótimo", "Falha fatal em mínimos locais (sem backtracking)"],
        ["Dijkstra", "Cega com Custo", "Fila de Prioridade: min g(n)", "Ótimo em distância acumulada", "Explora todas as direções isotropicamente"],
        ["A* (A-Estrela)", "Informada e Ótima", "Fila de Prioridade: f(n)=g(n)+h(n)", "Ótimo em distância acumulada", "Poda drástica guiada por heurística admissível"]
    ]

    for col_idx, texto in enumerate(cabecalhos):
        cell = tbl.cell(0, col_idx)
        cell.text = texto
        cell.fill.solid()
        cell.fill.fore_color.rgb = COR_NAVY_ESCURO
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COR_BRANCO
        p.alignment = PP_ALIGN.CENTER

    for row_idx, linha in enumerate(dados_algos, start=1):
        for col_idx, valor in enumerate(linha):
            cell = tbl.cell(row_idx, col_idx)
            cell.text = valor
            cell.fill.solid()
            cell.fill.fore_color.rgb = COR_AZUL_CLARO if row_idx % 2 == 1 else COR_BRANCO
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = COR_CINZA_TEXTO
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COR_AZUL_ACCENT

    # =========================================================================
    # SLIDE 5: Visualização da Exploração (Item 4.4.i)
    # =========================================================================
    slide5 = adicionar_slide_base("4. Visualização do Espaço de Busca (Item 4.4.i)", "Rede de pequeno porte (n=250, λ=0.05) ilustrando nós explorados e caminho percorrido")

    img_vis = pasta_figuras / "visualizacao_buscas_250.png"
    if img_vis.exists():
        slide5.shapes.add_picture(str(img_vis), Inches(0.8), Inches(1.5), width=Inches(8.4))

    # Painel lateral explicativo
    criar_card(
        slide5, Inches(9.4), Inches(1.5), Inches(3.1), Inches(5.3),
        "Destaques Visuais",
        [
            "BFS e Dijkstra: Exploram uniformemente em círculos, expandindo 244 de 250 nós.",
            "DFS: Caminha errante por ramos profundos com 136 saltos (custo 4952 vs ótimo 294).",
            "Best-First: Vai em linha reta até o alvo explorando apenas 8 nós (custo 382.9).",
            "A*: Equilibra custo e heurística, explorando 74 nós e encontrando a rota ÓTIMA (294.2).",
            "Hill Climbing: Sucesso nesta instância (8 nós explorados)."
        ],
        cor_fundo=COR_BRANCO,
        cor_borda=COR_AZUL_ACCENT
    )

    # =========================================================================
    # SLIDE 6: Metodologia Experimental (Item 4.4.ii)
    # =========================================================================
    slide6 = adicionar_slide_base("5. Metodologia Experimental (Item 4.4.ii)", "Bateria de testes em redes de grande porte (n=2500) com variação de parâmetros")

    criar_card(
        slide6, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.1),
        "Parâmetros da Rede",
        [
            "Dimensão: n = 2500 vértices.",
            "Espaço: [0, 2500] x [0, 2500].",
            "Variações de Lambda:",
            "  • λ = 0.01: Densa (Grau 22.7)",
            "  • λ = 0.02: Intermediária (Grau 5.95)",
            "  • λ = 0.03: Esparsa (Grau 2.72)",
            "Semente fixa (seed=42) para reprodutibilidade."
        ]
    )

    criar_card(
        slide6, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.1),
        "Seleção de Pares de Teste",
        [
            "10 pares distintos de (origem, destino).",
            "Critério de Seleção Rigoroso: Pares pertencentes à interseção das maiores componentes conexas.",
            "Garante viabilidade de caminho comum entre todas as 3 redes.",
            "Semente independente (seed_pares=2026)."
        ]
    )

    criar_card(
        slide6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.1),
        "Métricas Coletadas",
        [
            "Distância média percorrida e desvio padrão.",
            "Número médio de saltos (arestas).",
            "Vértices explorados (esforço computacional).",
            "Tempo de execução (time.perf_counter) com 3 repetições.",
            "Taxa de sucesso na obtenção de caminho."
        ]
    )

    # =========================================================================
    # SLIDE 7: Resultados de Distância Percorrida
    # =========================================================================
    slide7 = adicionar_slide_base("6. Resultados: Distância Percorrida", "Equivalência formal de otimalidade e comportamento das heurísticas")

    img_dist = pasta_figuras / "benchmark_distancia.png"
    if img_dist.exists():
        slide7.shapes.add_picture(str(img_dist), Inches(0.8), Inches(1.6), width=Inches(7.2))

    criar_card(
        slide7, Inches(8.2), Inches(1.6), Inches(4.3), Inches(5.1),
        "Principais Observações",
        [
            "A* e Dijkstra Idênticos: Comprovam formalmente a otimalidade de distância em todas as redes (1028.58 em λ=0.01; 1116.98 em λ=0.02; 1581.41 em λ=0.03).",
            "Best-First: Distância ligeiramente superior (~19% a 30% maior), porém obtida com muito menos expansões.",
            "BFS: Prioriza menor número de saltos, resultando em distâncias intermediárias não ótimas.",
            "DFS Omitido do Gráfico: Distância média de 308.938 em λ=0.01 (~300x o ótimo). Totalmente inviável."
        ]
    )

    # =========================================================================
    # SLIDE 8: Esforço Computacional
    # =========================================================================
    slide8 = adicionar_slide_base("7. Esforço Computacional: Nós Explorados e Tempo", "A heurística como mecanismo multiplicador de eficiência")

    img_exp = pasta_figuras / "benchmark_explorados.png"
    img_tmp = pasta_figuras / "benchmark_tempo.png"

    if img_exp.exists() and img_tmp.exists():
        slide8.shapes.add_picture(str(img_exp), Inches(0.8), Inches(1.6), width=Inches(5.6))
        slide8.shapes.add_picture(str(img_tmp), Inches(6.8), Inches(1.6), width=Inches(5.7))

    # =========================================================================
    # SLIDE 9: Comparação A* vs Dijkstra (Item 4.4.iii)
    # =========================================================================
    slide9 = adicionar_slide_base("8. Comparativo Detalhado: A* vs. Dijkstra (Item 4.4.iii)", "O impacto direto da heurística admissível e consistente na redução da busca")

    img_comp = pasta_figuras / "comparativo_astar_dijkstra.png"
    if img_comp.exists():
        slide9.shapes.add_picture(str(img_comp), Inches(0.8), Inches(1.5), width=Inches(8.2))

    criar_card(
        slide9, Inches(9.2), Inches(1.5), Inches(3.3), Inches(5.3),
        "Conclusões do Item 4.4.iii",
        [
            "Mesma Solução Ótima: Ambas as abordagens encontram rigorosamente o mesmo caminho.",
            "Redução de Nós Explorados:",
            "  • λ=0.01: A* explorou 27.4 nós vs 1026.9 do Dijkstra (37.5x menos).",
            "  • λ=0.02: A* explorou 102.3 nós vs 1017.7 do Dijkstra (10.0x menos).",
            "  • λ=0.03: A* explorou 295.7 nós vs 897.0 do Dijkstra (3.0x menos).",
            "Tempo de CPU:",
            "A* foi até 14.8x mais rápido graças à poda pelo cone euclidiano."
        ]
    )

    # =========================================================================
    # SLIDE 10: O Caso do Hill Climbing
    # =========================================================================
    slide10 = adicionar_slide_base("9. Análise Crítica: O Colapso do Hill Climbing", "Sensibilidade da otimização local estrita em função da esparsidade da rede")

    img_suc = pasta_figuras / "benchmark_sucesso.png"
    if img_suc.exists():
        slide10.shapes.add_picture(str(img_suc), Inches(0.8), Inches(1.6), width=Inches(6.4))

    criar_card(
        slide10, Inches(7.4), Inches(1.6), Inches(5.1), Inches(5.1),
        "Mecânica do Fenômeno",
        [
            "Sem Backtracking: O algoritmo só avança se o vizinho tiver h estritamente menor que o nó atual.",
            "Rede Densa (λ=0.01, Grau 22.7): 100% de sucesso. A multiplicidade de conexões garante gradiente contínuo até a meta.",
            "Rede Média (λ=0.02, Grau 5.95): 50% de sucesso. Surgem vazios espaciais onde o nó é o mais próximo da meta no seu cluster.",
            "Rede Esparsa (λ=0.03, Grau 2.72): 0% de sucesso. Todos os 10 pares caem invariavelmente em mínimos locais.",
            "Lição Teórica: Otimização local pura é frágil em grafos sem propriedades de convexidade."
        ]
    )

    # =========================================================================
    # SLIDE 11: Síntese dos Resultados e Matriz de Decisão
    # =========================================================================
    slide11 = adicionar_slide_base("10. Síntese dos Resultados e Matriz de Decisão", "Guia prático para seleção de algoritmos em aplicações de engenharia")

    linhas, colunas = 7, 5
    tabela_s = slide11.shapes.add_table(linhas, colunas, Inches(0.8), Inches(1.6), Inches(11.7), Inches(4.9))
    tbl_s = tabela_s.table
    tbl_s.columns[0].width = Inches(2.2)
    tbl_s.columns[1].width = Inches(2.3)
    tbl_s.columns[2].width = Inches(2.3)
    tbl_s.columns[3].width = Inches(2.4)
    tbl_s.columns[4].width = Inches(2.5)

    cab_s = ["Algoritmo", "Qualidade da Rota", "Esforço / Memória", "Robustez / Sucesso", "Indicação Prática"]
    dados_s = [
        ["A* (A-Estrela)", "Excelente (Ótimo)", "Excelente (Podado)", "100% (Completo)", "Padrão-ouro em roteamento físico e mapas"],
        ["Dijkstra", "Excelente (Ótimo)", "Moderado (Isotrópico)", "100% (Completo)", "Útil sem heurística ou para 1-para-todos"],
        ["Best-First", "Boa (~20% subótimo)", "Mínimo (Ultra veloz)", "100% (Completo)", "Sistemas em tempo real com recursos limitados"],
        ["BFS (Largura)", "Moderada (Ótimo em saltos)", "Alto (Fila grande)", "100% (Completo)", "Grafos não ponderados (saltos de rede)"],
        ["Hill Climbing", "Variável (Subótimo)", "Mínimo", "Instável (0% a 100%)", "Não recomendado sem reinícios ou recozimento"],
        ["DFS (Profundidade)", "Péssima (~300x pior)", "Moderado", "100% (Completo)", "Inadequado para cálculo de menor custo"]
    ]

    for col_idx, texto in enumerate(cab_s):
        cell = tbl_s.cell(0, col_idx)
        cell.text = texto
        cell.fill.solid()
        cell.fill.fore_color.rgb = COR_NAVY_ESCURO
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COR_BRANCO
        p.alignment = PP_ALIGN.CENTER

    for row_idx, linha in enumerate(dados_s, start=1):
        for col_idx, valor in enumerate(linha):
            cell = tbl_s.cell(row_idx, col_idx)
            cell.text = valor
            cell.fill.solid()
            cell.fill.fore_color.rgb = COR_AZUL_CLARO if row_idx % 2 == 1 else COR_BRANCO
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = COR_CINZA_TEXTO
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COR_AZUL_ACCENT

    # =========================================================================
    # SLIDE 12: Conclusões e Encerramento
    # =========================================================================
    slide12 = adicionar_slide_base("11. Conclusões", "Principais contribuições acadêmicas e lições do projeto")

    criar_card(
        slide12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(4.3),
        "Conclusões Técnicas",
        [
            "O modelo de Rede Geográfica capturou com fidelidade restrições de proximidade física e formação de agrupamentos.",
            "A heurística euclidiana provou-se altamente eficaz: reduziu em até 97% os nós explorados pelo A* em relação ao Dijkstra.",
            "O Hill Climbing sem backtracking mostrou-se dependente da densidade da rede, falhando categoricamente em topologias esparsas.",
            "O A* destacou-se como o algoritmo mais equilibrado entre custo ótimo e economia de recursos computacionais."
        ],
        cor_fundo=COR_BRANCO,
        cor_borda=COR_AZUL_ACCENT
    )

    criar_card(
        slide12, Inches(6.8), Inches(1.6), Inches(5.7), Inches(4.3),
        "Perguntas & Agradecimentos",
        [
            "Código-fonte e experimentos disponibilizados no repositório.",
            "Relatório técnico completo em formato de artigo estruturado.",
            "Agradecemos à equipe docente de SCC0230 pelo suporte.",
            "Estamos à disposição para arguição e dúvidas da banca."
        ],
        cor_fundo=COR_NAVY_ESCURO,
        cor_borda=COR_AZUL_ACCENT
    )
    # Ajuste de cores para o card de encerramento escuro
    # Atualiza textos do card escuro
    for shape in slide12.shapes:
        if shape.has_text_frame and "Perguntas & Agradecimentos" in shape.text_frame.text:
            for p_elem in shape.text_frame.paragraphs:
                p_elem.font.color.rgb = COR_BRANCO

    # Salva a apresentação
    prs.save(str(caminho_saida))
    print(f"\nApresentação salva com sucesso em: {caminho_saida}")


if __name__ == "__main__":
    criar_apresentacao()
