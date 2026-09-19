import pandas as pd
import streamlit as st
import random
import matplotlib.pyplot as plt

from core.minhastats import (
    media, mediana, moda, amplitude, variancia, desvio_padrao,
    coeficiente_variacao, quartis, tabela_frequencias, percentil,
    limites_outliers, outliers, densidade_normal, densidade_exponencial,
    covariancia, correlacao_pearson, regressao_linear_simples, r_quadrado,
)

st.set_page_config(page_title="Laboratório de Estatística — Varejo Brasileiro", layout="wide")

COR_ROXA = "#6D4AFF"
COR_ROXA_CLARA = "#C9BFFF"
COR_LARANJA = "#F5A623"
COR_VERMELHA = "#E4572E"
COR_CINZA = "#9CA3AF"

plt.rcParams["font.size"] = 9.5

CSS_DASHBOARD = """
<style>

.bloco-cartoes {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
.cartao-metrica {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    flex: 1;
    min-width: 170px;
}
.cartao-metrica .icone {
    font-size: 20px;
}
.cartao-metrica .rotulo {
    font-size: 13px;
    color: #6B7280;
    margin-top: 6px;
}
.cartao-metrica .valor {
    font-size: 26px;
    font-weight: 700;
    color: #1F2430;
    margin-top: 2px;
}
.cartao-metrica .contexto {
    font-size: 12px;
    color: #9CA3AF;
    margin-top: 6px;
}
[data-testid="stImageContainer"] {
    display: flex;
    justify-content: center;
}
</style>
"""
st.markdown(CSS_DASHBOARD, unsafe_allow_html=True)


def cartao_metrica(icone, rotulo, valor, contexto=""):
    return (
        f'<div class="cartao-metrica">'
        f'<div class="icone">{icone}</div>'
        f'<div class="rotulo">{rotulo}</div>'
        f'<div class="valor">{valor}</div>'
        f'<div class="contexto">{contexto}</div>'
        f'</div>'
    )


def linha_de_cartoes(cartoes):
    html = '<div class="bloco-cartoes">' + "".join(cartoes) + "</div>"
    st.markdown(html, unsafe_allow_html=True)


def novo_eixo(figsize=(6, 3.4), titulo=""):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#D1D5DB")
    ax.spines["bottom"].set_color("#D1D5DB")
    ax.tick_params(colors="#4B5563")
    ax.grid(axis="y", color="#E5E7EB", linewidth=0.8)
    ax.set_axisbelow(True)
    if titulo:
        ax.set_title(titulo, fontsize=11, fontweight="bold", color="#1F2430", pad=10)
    return fig, ax


def grafico_histograma(tabela, titulo="", cor=COR_ROXA):
    fig, ax = novo_eixo(titulo=titulo)
    for classe in tabela:
        largura = classe["limite_superior"] - classe["limite_inferior"]
        ax.bar(
            classe["limite_inferior"], classe["frequencia_absoluta"],
            width=largura, align="edge", color=cor, edgecolor="white", linewidth=0.5,
        )
    ax.set_ylabel("Frequência")
    return fig, ax


df = pd.read_csv("data/varejo_brasileiro.csv")

st.title("Laboratório de Estatística — Varejo Brasileiro")
st.write(df)

COLUNAS_NUMERICAS = [
    "valor_produtos", "valor_frete", "valor_total_pago", "quantidade_itens",
    "parcelas", "peso_produto_g", "volume_produto_cm3", "fotos_anuncio",
    "tamanho_descricao_anuncio", "dias_ate_entrega", "dias_estimados_entrega",
    "dias_de_atraso", "nota_avaliacao",
]

COLUNAS_CATEGORICAS = ["categoria_produto", "estado_cliente", "tipo_pagamento"]

COLUNAS_DISTRIBUICAO = [
    c for c in COLUNAS_NUMERICAS if c not in ("nota_avaliacao", "dias_de_atraso")
]

st.header("Estatística descritiva")
coluna_escolhida = st.selectbox("Escolha uma variável numérica:", COLUNAS_NUMERICAS)

dados = df[coluna_escolhida].tolist()

q1, q2, q3 = quartis(dados)

linha_de_cartoes([
    cartao_metrica("📊", "Média", f"{media(dados):.2f}", "sensível a valores extremos"),
    cartao_metrica("🎯", "Mediana", f"{mediana(dados):.2f}", "valor central, resiste a outliers"),
    cartao_metrica("📉", "Desvio padrão", f"{desvio_padrao(dados):.2f}", "dispersão em torno da média"),
])

linha_de_cartoes([
    cartao_metrica("📈", "Variância", f"{variancia(dados):.2f}", "desvio padrão ao quadrado"),
    cartao_metrica("📏", "Amplitude", f"{amplitude(dados):.2f}", "maior valor menos o menor"),
    cartao_metrica("🔀", "Coef. de variação", f"{coeficiente_variacao(dados):.1f}%", "dispersão relativa à média"),
])

linha_de_cartoes([
    cartao_metrica("🔻", "Q1", f"{q1:.2f}", "25% dos dados abaixo deste valor"),
    cartao_metrica("⏺", "Q2 (mediana)", f"{q2:.2f}", "50% dos dados abaixo deste valor"),
    cartao_metrica("🔺", "Q3", f"{q3:.2f}", "75% dos dados abaixo deste valor"),
])

modas = moda(dados)
if len(modas) > 5:
    st.write("Moda: não há um valor que se destaque, os dados estão muito dispersos, "
             "isso é comum em variáveis contínuas como preço ou peso.")
elif len(modas) == 1:
    linha_de_cartoes([
        cartao_metrica("🔁", "Moda", f"{modas[0]:.2f}", "valor mais frequente"),
    ])
else:
    valores_formatados = ", ".join(f"{v:.2f}" for v in modas)
    st.write(f"Moda: valores empatados — {valores_formatados}")

media_dados = media(dados)
mediana_dados = mediana(dados)
desvio_dados = desvio_padrao(dados)
diferenca_media_mediana = media_dados - mediana_dados

if diferenca_media_mediana > 0.5 * desvio_dados:
    st.write(
        f"Assimetria à direita: a média ({media_dados:.2f}) é maior que a mediana "
        f"({mediana_dados:.2f}), valores altos puxam a média para cima."
    )
elif diferenca_media_mediana < -0.5 * desvio_dados:
    st.write(
        f"Assimetria à esquerda: a média ({media_dados:.2f}) é menor que a mediana "
        f"({mediana_dados:.2f}), valores baixos puxam a média para baixo."
    )
else:
    st.write(
        f"Aproximadamente simétrica: a média ({media_dados:.2f}) e a mediana "
        f"({mediana_dados:.2f}) estão próximas."
    )


st.subheader("Distribuição de frequências")

tabela = tabela_frequencias(dados)

linhas_tabela = []
for classe in tabela:
    linhas_tabela.append({
        "Classe": f"{classe['limite_inferior']:.2f} – {classe['limite_superior']:.2f}",
        "Frequência absoluta": classe["frequencia_absoluta"],
        "Frequência relativa (%)": round(classe["frequencia_relativa"], 1),
        "Frequência acumulada": classe["frequencia_acumulada"],
    })

st.dataframe(pd.DataFrame(linhas_tabela), use_container_width=True)

recortar = st.checkbox(
    "Recortar o 1% superior no gráfico (a tabela acima sempre mostra os dados completos)",
    value=tabela[0]["frequencia_relativa"] > 80,
)

if recortar:
    limite_visual = percentil(dados, 99)
    dados_grafico = [x for x in dados if x <= limite_visual]
    tabela_grafico = tabela_frequencias(dados_grafico)
else:
    tabela_grafico = tabela

fig_hist, ax_hist = grafico_histograma(
    tabela_grafico, titulo=f"Histograma de {coluna_escolhida} (classes pela regra de Sturges)"
)
ax_hist.axvline(media_dados, color=COR_LARANJA, linewidth=2, label=f"média = {media_dados:.1f}")
ax_hist.axvline(mediana_dados, color=COR_VERMELHA, linewidth=2, linestyle="--", label=f"mediana = {mediana_dados:.1f}")
ax_hist.set_xlabel(coluna_escolhida)
ax_hist.legend(frameon=False)
st.pyplot(fig_hist, width=900)


st.subheader("Distribuição de uma variável categórica")
coluna_categorica = st.selectbox("Escolha uma variável categórica:", COLUNAS_CATEGORICAS)

contagens = df[coluna_categorica].value_counts().sort_values(ascending=False).head(10)

fig_cat, ax_cat = novo_eixo(titulo=f"Frequência de {coluna_categorica} (10 mais frequentes)")
ax_cat.barh(contagens.index[::-1], contagens.values[::-1], color=COR_ROXA)
ax_cat.set_xlabel("Frequência")
st.pyplot(fig_cat, width=900)


st.subheader("Boxplot e outliers")

limite_inferior, limite_superior = limites_outliers(dados)
valores_atipicos = outliers(dados)

nao_atipicos = [x for x in dados if limite_inferior <= x <= limite_superior]
bigode_inferior = min(nao_atipicos)
bigode_superior = max(nao_atipicos)

estatisticas_box = {
    "med": mediana_dados,
    "q1": q1,
    "q3": q3,
    "whislo": bigode_inferior,
    "whishi": bigode_superior,
    "fliers": [],
    "mean": media_dados,
}

fig_box, ax_box = novo_eixo(
    figsize=(6, 2.1), titulo=f"Boxplot de {coluna_escolhida} — outliers pela regra do IQR"
)
caixa = ax_box.bxp(
    [estatisticas_box], vert=False, showfliers=False, patch_artist=True, widths=0.5,
)
for elemento in caixa["boxes"]:
    elemento.set_facecolor(COR_ROXA_CLARA)
    elemento.set_edgecolor(COR_ROXA)
for elemento in caixa["medians"]:
    elemento.set_color(COR_ROXA)
if valores_atipicos:
    ax_box.scatter(
        valores_atipicos, [1] * len(valores_atipicos),
        color=COR_VERMELHA, alpha=0.5, s=25, zorder=3,
        label=f"{len(valores_atipicos)} outliers (regra do IQR)",
    )
ax_box.axvline(limite_superior, color=COR_VERMELHA, linestyle=":", linewidth=1.5)
ax_box.set_yticks([])
ax_box.set_xlabel(coluna_escolhida)
if valores_atipicos:
    ax_box.legend(frameon=False, loc="upper right")
st.pyplot(fig_box, width=900)

col_a, col_b, col_c = st.columns(3)
col_a.metric("Limite inferior (IQR)", f"{limite_inferior:.2f}")
col_b.metric("Limite superior (IQR)", f"{limite_superior:.2f}")
col_c.metric("Nº de outliers", f"{len(valores_atipicos)} ({len(valores_atipicos) / len(dados) * 100:.1f}%)")

st.header("Probabilidade e simulação")

aba_lgn, aba_tcl = st.tabs(["Lei dos Grandes Números", "Teorema Central do Limite"])

with aba_lgn:
    st.write(
        "Simulação de lançamentos de moeda. A Lei dos Grandes Números diz que, "
        "quanto mais vezes repetimos um experimento aleatório, mais a proporção "
        "observada se aproxima da probabilidade teórica, que aqui é 50% de chance de cara."
    )

    n_lancamentos = st.slider("Número de lançamentos", min_value=10, max_value=5000, value=300, step=10)

    resultados = [random.randint(0, 1) for _ in range(n_lancamentos)]
    proporcoes = [media(resultados[:i]) for i in range(1, n_lancamentos + 1)]

    fig_lgn, ax_lgn = novo_eixo(titulo="Lei dos Grandes Números — frequência relativa de caras")
    ax_lgn.plot(range(1, n_lancamentos + 1), proporcoes, color=COR_ROXA, linewidth=1.5, label="Proporção de caras")
    ax_lgn.axhline(0.5, color=COR_VERMELHA, linestyle="--", linewidth=1.5, label="probabilidade teórica = 0,5")
    ax_lgn.set_xscale("log")
    ax_lgn.set_xlabel("Número de lançamentos (escala log)")
    ax_lgn.set_ylabel("Proporção acumulada de caras")
    ax_lgn.legend(frameon=False)
    st.pyplot(fig_lgn, width=900)

    proporcao_final = proporcoes[-1]
    distancia = abs(proporcao_final - 0.5)

    col_l1, col_l2 = st.columns(2)
    col_l1.metric("Proporção final de caras", f"{proporcao_final:.4f}")
    col_l2.metric("Distância do valor teórico", f"{distancia:.4f}")


with aba_tcl:
    st.write(
        "O Teorema Central do Limite diz que, mesmo quando a variável original tem uma "
        "distribuição bem torta, a distribuição das médias de amostras repetidas dela se "
        "aproxima de uma Normal (curva de sino) à medida que o tamanho da amostra cresce."
    )

    coluna_tcl = st.selectbox(
        "Escolha a variável a simular:",
        COLUNAS_NUMERICAS,
        index=COLUNAS_NUMERICAS.index("valor_produtos"),
        key="coluna_tcl",
    )
    dados_tcl = df[coluna_tcl].tolist()

    tamanho_amostra = st.slider("Tamanho de cada amostra (n)", min_value=5, max_value=200, value=30, step=5)
    numero_amostras = st.slider("Número de amostras repetidas", min_value=100, max_value=2000, value=500, step=100)

    medias_amostrais = [
        media(random.choices(dados_tcl, k=tamanho_amostra))
        for _ in range(numero_amostras)
    ]

    tabela_original = tabela_frequencias(dados_tcl)
    tabela_medias = tabela_frequencias(medias_amostrais)

    col_original, col_medias = st.columns(2)

    with col_original:
        fig_original, ax_original = grafico_histograma(
            tabela_original, titulo=f"Distribuição original de {coluna_tcl}", cor=COR_LARANJA
        )
        st.pyplot(fig_original, width=630)

    with col_medias:
        media_medias = media(medias_amostrais)
        desvio_medias = desvio_padrao(medias_amostrais)
        fig_medias, ax_medias = grafico_histograma(
            tabela_medias,
            titulo=f"{numero_amostras} médias amostrais (n={tamanho_amostra})",
            cor=COR_ROXA,
        )
        minimo_medias, maximo_medias = min(medias_amostrais), max(medias_amostrais)
        passo_medias = (maximo_medias - minimo_medias) / 199 if maximo_medias > minimo_medias else 1
        pontos_medias = [minimo_medias + i * passo_medias for i in range(200)]
        n_medias = len(medias_amostrais)
        largura_media_classe = (maximo_medias - minimo_medias) / len(tabela_medias)
        fator_escala = n_medias * largura_media_classe
        curva_normal_tcl = [
            densidade_normal(x, media_medias, desvio_medias) * fator_escala for x in pontos_medias
        ]
        ax_medias.plot(pontos_medias, curva_normal_tcl, color=COR_VERMELHA, linewidth=2)
        st.pyplot(fig_medias, width=630)

    erro_padrao_teorico = desvio_padrao(dados_tcl) / (tamanho_amostra ** 0.5)
    desvio_observado = desvio_padrao(medias_amostrais)

    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Média original", f"{media(dados_tcl):.2f}")
    col_t2.metric("Média das médias amostrais", f"{media(medias_amostrais):.2f}")
    col_t3.metric("Erro padrão teórico (σ/√n)", f"{erro_padrao_teorico:.2f}")
    col_t4.metric("Desvio padrão observado", f"{desvio_observado:.2f}")

    st.write(
        f"Com n = {tamanho_amostra}, a distribuição das médias já se aproxima de uma curva "
        f"Normal, mesmo a variável original {coluna_tcl} não sendo simétrica. O desvio padrão "
        f"observado das médias ({desvio_observado:.2f}) fica próximo do erro padrão teórico "
        f"({erro_padrao_teorico:.2f}), que é o desvio padrão original dividido pela raiz de n."
    )


st.header("Distribuições teóricas")

coluna_dist = st.selectbox(
    "Escolha a variável:",
    COLUNAS_DISTRIBUICAO,
    index=COLUNAS_DISTRIBUICAO.index("valor_produtos"),
    key="coluna_dist",
)
dados_dist = df[coluna_dist].tolist()

m = media(dados_dist)
s = desvio_padrao(dados_dist)
taxa = 1 / m if m > 0 else None

tabela_dist = tabela_frequencias(dados_dist)
n = len(dados_dist)

pontos_bins = []
densidade_observada = []
for classe in tabela_dist:
    largura = classe["limite_superior"] - classe["limite_inferior"]
    ponto_medio = (classe["limite_inferior"] + classe["limite_superior"]) / 2
    pontos_bins.append(ponto_medio)
    densidade_observada.append(classe["frequencia_absoluta"] / (n * largura))

minimo, maximo = min(dados_dist), max(dados_dist)
passo = (maximo - minimo) / 199
pontos_curva = [minimo + i * passo for i in range(200)]
curva_normal = [densidade_normal(x, m, s) for x in pontos_curva]

fig_dist, ax_dist = novo_eixo(titulo=f"Ajuste de distribuições sobre {coluna_dist}")
largura_barra = (maximo - minimo) / len(tabela_dist)
ax_dist.bar(pontos_bins, densidade_observada, width=largura_barra, color=COR_CINZA, alpha=0.7, label="Densidade observada")
ax_dist.plot(pontos_curva, curva_normal, color=COR_VERMELHA, linewidth=2.5, label="Curva Normal")
if taxa is not None:
    curva_exponencial = [densidade_exponencial(x, taxa) for x in pontos_curva]
    ax_dist.plot(pontos_curva, curva_exponencial, color=COR_LARANJA, linewidth=2.5, linestyle="--", label="Curva Exponencial")
ax_dist.set_xlabel(coluna_dist)
ax_dist.set_ylabel("Densidade")
ax_dist.legend(frameon=False)
st.pyplot(fig_dist, width=900)

erro_normal = sum(
    (classe["frequencia_relativa"] / 100) * (obs - densidade_normal(x, m, s)) ** 2
    for x, obs, classe in zip(pontos_bins, densidade_observada, tabela_dist)
)

col_d1, col_d2, col_d3 = st.columns(3)
col_d1.metric("Erro (Normal)", f"{erro_normal:.6f}")
if taxa is not None:
    erro_exponencial = sum(
        (classe["frequencia_relativa"] / 100) * (obs - densidade_exponencial(x, taxa)) ** 2
        for x, obs, classe in zip(pontos_bins, densidade_observada, tabela_dist)
    )
    col_d2.metric("Erro (Exponencial)", f"{erro_exponencial:.6f}")
    col_d3.metric("Melhor ajuste", "Normal" if erro_normal < erro_exponencial else "Exponencial")
else:
    col_d2.metric("Erro (Exponencial)", "não aplicável (média ≤ 0)")

st.write(
    f"A Normal estimada usa μ = {m:.2f} e σ = {s:.2f}, os próprios média e desvio padrão dos "
    f"dados. Quando a curva Normal (vermelha) se afasta muito das barras cinza, principalmente "
    f"na cauda direita, é sinal de que a variável é assimétrica e uma distribuição como a "
    f"Exponencial pode descrever melhor esse comportamento."
)

st.header("Correlação e regressão")

col_x, col_y = st.columns(2)
with col_x:
    coluna_x = st.selectbox("Variável X:", COLUNAS_NUMERICAS, index=COLUNAS_NUMERICAS.index("peso_produto_g"), key="coluna_x")
with col_y:
    coluna_y = st.selectbox("Variável Y:", COLUNAS_NUMERICAS, index=COLUNAS_NUMERICAS.index("valor_frete"), key="coluna_y")

dados_x = df[coluna_x].tolist()
dados_y = df[coluna_y].tolist()

cov = covariancia(dados_x, dados_y)
r = correlacao_pearson(dados_x, dados_y)
a, b = regressao_linear_simples(dados_x, dados_y)
r2 = r_quadrado(dados_x, dados_y)


def classificar_correlacao(r):
    r_abs = abs(r)
    if r_abs < 0.3:
        return "fraca"
    elif r_abs < 0.6:
        return "moderada"
    else:
        return "forte"


def grafico_regressao(x, y, a, b, coluna_x, coluna_y, titulo=""):
    fig, ax = novo_eixo(titulo=titulo)
    ax.scatter(x, y, color=COR_ROXA_CLARA, s=6, alpha=0.35, edgecolors="none")
    x_min, x_max = min(x), max(x)
    ax.plot([x_min, x_max], [a + b * x_min, a + b * x_max], color=COR_LARANJA, linewidth=2.5)
    ax.set_xlabel(coluna_x)
    ax.set_ylabel(coluna_y)
    r2_local = r_quadrado(x, y)
    ax.text(
        0.03, 0.95, f"ŷ = {a:.2f} + {b:.4f}·x   (R² = {r2_local:.3f})",
        transform=ax.transAxes, va="top", fontsize=10, color="#1F2430",
        bbox=dict(facecolor="white", edgecolor="#D1D5DB", boxstyle="round,pad=0.4"),
    )
    return fig, ax


fig_disp, ax_disp = grafico_regressao(dados_x, dados_y, a, b, coluna_x, coluna_y, titulo="Dispersão e reta de regressão")
st.pyplot(fig_disp, width=900)

col_r1, col_r2, col_r3, col_r4 = st.columns(4)
col_r1.metric("Covariância", f"{cov:.4f}")
col_r2.metric("Correlação (r)", f"{r:.4f}")
col_r3.metric("Força da correlação", classificar_correlacao(r))
col_r4.metric("R²", f"{r2:.4f}")

st.write(f"{r2 * 100:.1f}% da variação de {coluna_y} é explicada por {coluna_x}.")
st.latex(f"\\hat{{y}} = {a:.4f} + {b:.4f} \\cdot x")

direcao_b = "a mais" if b >= 0 else "a menos"
st.write(
    f"Interpretação de b1: cada unidade a mais de {coluna_x} está associada, em média, a "
    f"{abs(b):.4f} unidades {direcao_b} de {coluna_y}."
)

st.warning("Correlação não implica causalidade: mesmo que duas variáveis se movam juntas, "
           "isso não prova que uma cause a outra.")

st.subheader("Previsão interativa")
minimo_x, maximo_x = min(dados_x), max(dados_x)
valor_x_previsto = st.number_input(
    f"Digite um valor de {coluna_x} (entre {minimo_x:.2f} e {maximo_x:.2f}):",
    value=float(media(dados_x)),
    min_value=float(minimo_x),
    max_value=float(maximo_x),
)
st.caption("O campo é limitado ao intervalo observado dos dados: prever fora dele seria extrapolação, e a reta não foi validada ali.")
valor_y_previsto = a + b * valor_x_previsto
st.metric(f"{coluna_y} previsto", f"{valor_y_previsto:.2f}")


st.header("Descobertas")
st.caption("Amostra de pedidos entre outubro de 2016 e agosto de 2018. As descobertas abaixo mostram associação, não causa.")

st.subheader("1. Frete pesa mais pra quem mora longe")
MIN_PEDIDOS_ESTADO = 300
frete_pct_lista = (df["valor_frete"] / df["valor_produtos"] * 100).tolist()
estados_lista = df["estado_cliente"].tolist()

frete_pct_por_estado = {}
for estado, pct in zip(estados_lista, frete_pct_lista):
    frete_pct_por_estado.setdefault(estado, []).append(pct)

media_frete_pct_por_estado = {
    estado: media(pcts)
    for estado, pcts in frete_pct_por_estado.items()
    if len(pcts) >= MIN_PEDIDOS_ESTADO
}
estados_ordenados = sorted(media_frete_pct_por_estado, key=media_frete_pct_por_estado.get)

estado_menor = estados_ordenados[0]
estado_maior = estados_ordenados[-1]
pct_menor = media_frete_pct_por_estado[estado_menor]
pct_maior = media_frete_pct_por_estado[estado_maior]

col_1a, col_1b, col_1c = st.columns(3)
col_1a.metric(f"Frete médio — {estado_menor}", f"{pct_menor:.1f}% do valor do produto")
col_1b.metric(f"Frete médio — {estado_maior}", f"{pct_maior:.1f}% do valor do produto")
col_1c.metric("Quantas vezes maior", f"{pct_maior / pct_menor:.1f}x")

fig_d1, ax_d1 = novo_eixo(figsize=(6, 3.4), titulo="Frete como % do valor do produto, por estado do cliente")
ax_d1.barh(estados_ordenados, [media_frete_pct_por_estado[e] for e in estados_ordenados], color=COR_ROXA)
ax_d1.set_xlabel("Frete médio (% do valor do produto)")
st.pyplot(fig_d1, width=900)

st.write(
    f"Em {estado_menor}, o frete representa em média {pct_menor:.1f}% do valor do produto "
    f"comprado. Em {estado_maior}, chega a {pct_maior:.1f}%, quase {pct_maior / pct_menor:.1f} "
    f"vezes mais. A diferença acompanha a distância até os centros de distribuição, "
    f"concentrados no Sudeste, quem compra mais longe paga proporcionalmente mais caro pelo "
    f"frete, mesmo em produtos de valor parecido. Considerando apenas estados com pelo menos "
    f"{MIN_PEDIDOS_ESTADO} pedidos na amostra, {len(media_frete_pct_por_estado)} dos 27 estados."
)

st.subheader("2. Frete tem parte fixa e parte por peso")
peso_lista = df["peso_produto_g"].tolist()
frete_lista = df["valor_frete"].tolist()

r_frete = correlacao_pearson(peso_lista, frete_lista)
a_frete, b_frete = regressao_linear_simples(peso_lista, frete_lista)
r2_frete = r_quadrado(peso_lista, frete_lista)

col_2a, col_2b, col_2c = st.columns(3)
col_2a.metric("Correlação (r)", f"{r_frete:.4f}")
col_2b.metric("R²", f"{r2_frete:.4f}")
col_2c.metric("Parte fixa (R$)", f"{a_frete:.2f}")

fig_d2, ax_d2 = grafico_regressao(
    peso_lista, frete_lista, a_frete, b_frete, "peso_produto_g", "valor_frete",
    titulo="Peso do produto x valor do frete",
)
st.pyplot(fig_d2, width=900)

st.write(
    f"A correlação entre peso do produto e valor do frete é {classificar_correlacao(r_frete)}, "
    f"com r = {r_frete:.4f}. A regressão estima que o frete tem uma parte fixa de "
    f"R\\$ {a_frete:.2f}, mais R\\$ {b_frete * 1000:.4f} por quilo do produto. O R² de "
    f"{r2_frete:.4f} mostra que {r2_frete * 100:.1f}% da variação do frete é explicada só pelo "
    f"peso, o restante vem de outros fatores, como distância e transportadora."
)

st.subheader("3. Atraso na entrega está associado a nota mais baixa")
no_prazo = df[df["dias_de_atraso"] <= 0]["nota_avaliacao"].tolist()
atrasado = df[df["dias_de_atraso"] > 0]["nota_avaliacao"].tolist()

media_no_prazo = media(no_prazo)
media_atrasado = media(atrasado)
pct_atrasado = len(atrasado) / len(df) * 100

col_3a, col_3b, col_3c = st.columns(3)
col_3a.metric("Nota média — no prazo", f"{media_no_prazo:.2f}")
col_3b.metric("Nota média — atrasado", f"{media_atrasado:.2f}")
col_3c.metric("% de pedidos atrasados", f"{pct_atrasado:.1f}%")

fig_d3, ax_d3 = novo_eixo(figsize=(4.5, 3), titulo="Nota média de avaliação por situação de entrega")
ax_d3.bar(["No prazo", "Atrasado"], [media_no_prazo, media_atrasado], color=[COR_ROXA, COR_VERMELHA], width=0.5)
ax_d3.set_ylabel("Nota média (1 a 5)")
ax_d3.set_ylim(0, 5)
st.pyplot(fig_d3, width=525)

st.write(
    f"Pedidos entregues no prazo ou antes recebem nota média {media_no_prazo:.2f}, contra "
    f"{media_atrasado:.2f} para pedidos entregues com atraso, uma diferença de "
    f"{media_no_prazo - media_atrasado:.2f} pontos numa escala de 1 a 5. Apenas "
    f"{pct_atrasado:.1f}% dos pedidos atrasam, mas essa associação é forte o bastante para "
    f"impactar a satisfação do cliente. Não dá pra afirmar que o atraso é a única causa da nota "
    f"baixa, outros problemas do pedido podem coincidir com o atraso."
)
