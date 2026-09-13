import pandas as pd
import streamlit as st

from core.minhastats import (
    media, mediana, moda, amplitude, variancia, desvio_padrao,
    coeficiente_variacao, quartis, tabela_frequencias, percentil,
)
import plotly.express as px

st.set_page_config(page_title="Laboratório de Estatística — Varejo Brasileiro", layout="wide")

CSS_DASHBOARD = """
<style>
.stApp {
    background-color: #F4F5F7;
}
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