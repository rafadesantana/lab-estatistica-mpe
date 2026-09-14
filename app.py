import pandas as pd
import streamlit as st
import random

from core.minhastats import (
    media, mediana, moda, amplitude, variancia, desvio_padrao,
    coeficiente_variacao, quartis, tabela_frequencias, percentil,
    limites_outliers, outliers, densidade_normal, densidade_exponencial,
    covariancia, correlacao_pearson, regressao_linear_simples, r_quadrado,
)

import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Laboratório de Estatística — Varejo Brasileiro", layout="wide")

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


df = pd.read_csv("data/varejo_brasileiro.csv")

st.title("Laboratório de Estatística — Varejo Brasileiro")
st.write(df)

COLUNAS_NUMERICAS = [
    "valor_produtos", "valor_frete", "valor_total_pago", "quantidade_itens",
    "parcelas", "peso_produto_g", "volume_produto_cm3", "fotos_anuncio",
    "tamanho_descricao_anuncio", "dias_ate_entrega", "dias_estimados_entrega",
    "dias_de_atraso", "nota_avaliacao",
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
    st.write("Moda: não há um valor que se destaque — os dados estão muito dispersos "
             "(comum em variáveis contínuas como preço ou peso).")
elif len(modas) == 1:
    linha_de_cartoes([
        cartao_metrica("🔁", "Moda", f"{modas[0]:.2f}", "valor mais frequente"),
    ])
else:
    valores_formatados = ", ".join(f"{v:.2f}" for v in modas)
    st.write(f"Moda: valores empatados — {valores_formatados}")


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

fig = px.bar(
    x=[f"{c['limite_inferior']:.2f} – {c['limite_superior']:.2f}" for c in tabela_grafico],
    y=[c["frequencia_absoluta"] for c in tabela_grafico],
    labels={"x": "Classe", "y": "Frequência"},
)
fig.update_traces(marker_color="#4F46E5")
fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", bargap=0.15)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Boxplot e outliers")

limite_inferior, limite_superior = limites_outliers(dados)
valores_atipicos = outliers(dados)

nao_atipicos = [x for x in dados if limite_inferior <= x <= limite_superior]
bigode_inferior = min(nao_atipicos)
bigode_superior = max(nao_atipicos)

fig_box = go.Figure()
fig_box.add_trace(go.Box(
    q1=[q1], median=[q2], q3=[q3],
    lowerfence=[bigode_inferior],
    upperfence=[bigode_superior],
    name=coluna_escolhida,
    marker_color="#4F46E5",
    boxpoints=False,
))
if valores_atipicos:
    fig_box.add_trace(go.Scatter(
        x=[coluna_escolhida] * len(valores_atipicos),
        y=valores_atipicos,
        mode="markers",
        marker=dict(color="#C2603B", size=5, opacity=0.5),
        name="Outliers",
    ))
fig_box.update_layout(plot_bgcolor="white", paper_bgcolor="white", showlegend=False)
st.plotly_chart(fig_box, use_container_width=True)

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
        "observada se aproxima da probabilidade teórica — aqui, 50% de chance de cara."
    )

    n_lancamentos = st.slider("Número de lançamentos", min_value=10, max_value=5000, value=300, step=10)

    resultados = [random.randint(0, 1) for _ in range(n_lancamentos)]
    proporcoes = [media(resultados[:i]) for i in range(1, n_lancamentos + 1)]

    fig_lgn = go.Figure()
    fig_lgn.add_trace(go.Scatter(
        x=list(range(1, n_lancamentos + 1)),
        y=proporcoes,
        mode="lines",
        name="Proporção de caras",
        line=dict(color="#4F46E5"),
    ))
    fig_lgn.add_hline(y=0.5, line_dash="dash", line_color="#C2603B",
                       annotation_text="valor teórico (0,5)")
    fig_lgn.update_layout(
        xaxis_title="Número de lançamentos",
        yaxis_title="Proporção acumulada de caras",
        plot_bgcolor="white", paper_bgcolor="white",
    )
    st.plotly_chart(fig_lgn, use_container_width=True)

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
        st.caption(f"Distribuição original de {coluna_tcl}")
        fig_original = px.bar(
            x=[f"{c['limite_inferior']:.1f}–{c['limite_superior']:.1f}" for c in tabela_original],
            y=[c["frequencia_absoluta"] for c in tabela_original],
            labels={"x": "Classe", "y": "Frequência"},
        )
        fig_original.update_traces(marker_color="#C2603B")
        fig_original.update_layout(plot_bgcolor="white", paper_bgcolor="white", bargap=0.15)
        st.plotly_chart(fig_original, use_container_width=True)

    with col_medias:
        st.caption(f"Distribuição das {numero_amostras} médias amostrais (n={tamanho_amostra})")
        fig_medias = px.bar(
            x=[f"{c['limite_inferior']:.1f}–{c['limite_superior']:.1f}" for c in tabela_medias],
            y=[c["frequencia_absoluta"] for c in tabela_medias],
            labels={"x": "Classe", "y": "Frequência"},
        )
        fig_medias.update_traces(marker_color="#4F46E5")
        fig_medias.update_layout(plot_bgcolor="white", paper_bgcolor="white", bargap=0.15)
        st.plotly_chart(fig_medias, use_container_width=True)

    erro_padrao_teorico = desvio_padrao(dados_tcl) / (tamanho_amostra ** 0.5)
    desvio_observado = desvio_padrao(medias_amostrais)

    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Média original", f"{media(dados_tcl):.2f}")
    col_t2.metric("Média das médias amostrais", f"{media(medias_amostrais):.2f}")
    col_t3.metric("Erro padrão teórico (σ/√n)", f"{erro_padrao_teorico:.2f}")
    col_t4.metric("Desvio padrão observado", f"{desvio_observado:.2f}")


    st.header("Distribuições teóricas")

coluna_dist = st.selectbox(
    "Escolha a variável:",
    COLUNAS_NUMERICAS,
    index=COLUNAS_NUMERICAS.index("valor_produtos"),
    key="coluna_dist",
)
dados_dist = df[coluna_dist].tolist()

m = media(dados_dist)
s = desvio_padrao(dados_dist)
taxa = 1 / m

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
curva_exponencial = [densidade_exponencial(x, taxa) for x in pontos_curva]

fig_dist = go.Figure()
fig_dist.add_trace(go.Bar(
    x=pontos_bins, y=densidade_observada, name="Densidade observada",
    marker_color="#B9C2CB",
))
fig_dist.add_trace(go.Scatter(
    x=pontos_curva, y=curva_normal, mode="lines", name="Curva Normal",
    line=dict(color="#4F46E5", width=3),
))
fig_dist.add_trace(go.Scatter(
    x=pontos_curva, y=curva_exponencial, mode="lines", name="Curva Exponencial",
    line=dict(color="#C2603B", width=3),
))
fig_dist.update_layout(
    xaxis_title=coluna_dist, yaxis_title="Densidade",
    plot_bgcolor="white", paper_bgcolor="white",
)
st.plotly_chart(fig_dist, use_container_width=True)

erro_normal = sum(
    (classe["frequencia_relativa"] / 100) * (obs - densidade_normal(x, m, s)) ** 2
    for x, obs, classe in zip(pontos_bins, densidade_observada, tabela_dist)
)
erro_exponencial = sum(
    (classe["frequencia_relativa"] / 100) * (obs - densidade_exponencial(x, taxa)) ** 2
    for x, obs, classe in zip(pontos_bins, densidade_observada, tabela_dist)
)

col_d1, col_d2, col_d3 = st.columns(3)
col_d1.metric("Erro (Normal)", f"{erro_normal:.6f}")
col_d2.metric("Erro (Exponencial)", f"{erro_exponencial:.6f}")
col_d3.metric("Melhor ajuste", "Normal" if erro_normal < erro_exponencial else "Exponencial")

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


fig_disp = go.Figure()
fig_disp.add_trace(go.Scatter(
    x=dados_x, y=dados_y, mode="markers",
    marker=dict(color="#B9C2CB", size=4, opacity=0.4),
    name="Pedidos",
))

x_min, x_max = min(dados_x), max(dados_x)
fig_disp.add_trace(go.Scatter(
    x=[x_min, x_max], y=[a + b * x_min, a + b * x_max],
    mode="lines", line=dict(color="#4F46E5", width=3),
    name="Reta de regressão",
))
fig_disp.update_layout(
    xaxis_title=coluna_x, yaxis_title=coluna_y,
    plot_bgcolor="white", paper_bgcolor="white",
)
st.plotly_chart(fig_disp, use_container_width=True)

col_r1, col_r2, col_r3, col_r4 = st.columns(4)
col_r1.metric("Covariância", f"{cov:.4f}")
col_r2.metric("Correlação (r)", f"{r:.4f}")
col_r3.metric("Força da correlação", classificar_correlacao(r))
col_r4.metric("R²", f"{r2:.4f}")

st.write(f"{r2 * 100:.1f}% da variação de {coluna_y} é explicada por {coluna_x}.")
st.latex(f"\\hat{{y}} = {a:.4f} + {b:.4f} \\cdot x")

st.warning("Correlação não implica causalidade: mesmo que duas variáveis se movam juntas, "
           "isso não prova que uma cause a outra.")

st.subheader("Previsão interativa")
valor_x_previsto = st.number_input(f"Digite um valor de {coluna_x}:", value=float(media(dados_x)))
valor_y_previsto = a + b * valor_x_previsto
st.metric(f"{coluna_y} previsto", f"{valor_y_previsto:.2f}")