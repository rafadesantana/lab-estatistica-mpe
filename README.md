# Laboratório Estatístico Interativo

**Rafael Leandro Pereira de Santana** — matrícula 72650038
Disciplina: Matemática e Estatística para Computação
Professor: Romes Heriberto

Aplicação em Streamlit com um núcleo estatístico próprio (sem `numpy`/`pandas` nas contas exibidas), aplicado a um dataset real de e-commerce brasileiro.

## Sobre o projeto

O núcleo estatístico (`core/minhastats.py`) implementa do zero, em Python puro, as funções usadas em todo o app: média, mediana, moda, amplitude, variância (amostral e populacional), desvio padrão, percentil, quartis, coeficiente de variação, covariância, correlação de Pearson, regressão linear simples, R², regra de Sturges, tabela de frequências, regra do IQR para outliers, e densidade Normal e Exponencial. Cada função tem um teste comparando o resultado com NumPy ou SciPy (`tests/test_minhastats.py`).

Em cima desse núcleo, a aplicação (`app.py`) tem 6 módulos: estatística descritiva interativa, probabilidade e simulação (Lei dos Grandes Números e Teorema Central do Limite), distribuições teóricas, correlação e regressão, e 3 descobertas sobre o dataset.

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), dados reais de pedidos de e-commerce no Brasil entre outubro de 2016 e agosto de 2018.

O arquivo usado pela aplicação (`data/varejo_brasileiro.csv`) é uma tabela analítica montada a partir de 6 das 9 tabelas originais (pedidos entregues, itens, produtos, pagamentos, avaliações e clientes), com 94.472 linhas, 13 colunas numéricas e 3 categóricas.

## Estrutura do repositório

```
lab-estatistica-mpe/
|-- app.py                    # interface (Streamlit)
|-- core/
|   +-- minhastats.py         # nucleo: so as funcoes proprias, sem numpy/pandas nas contas
|-- tests/
|   +-- test_minhastats.py    # testes pytest comparando com NumPy/SciPy
|-- data/
|   +-- varejo_brasileiro.csv
|-- .streamlit/
|   +-- config.toml           # tema claro forcado
|-- requirements.txt
|-- pytest.ini
|-- RELATORIO.md              # relatorio completo de entrega
|-- RESUMO_EXECUTIVO.md       # resumo de 1 pagina
+-- README.md
```

## Como rodar

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py     # roda a aplicação
pytest -v                # roda os testes (31 testes)
```

## Módulos da aplicação

1. **Estatística descritiva** — média, mediana, moda, desvio padrão, variância, amplitude, coeficiente de variação, quartis, histograma (regra de Sturges), boxplot com outliers (regra do IQR), interpretação automática de assimetria, e distribuição de variáveis categóricas.
2. **Probabilidade e simulação** — Lei dos Grandes Números (simulação de moeda) e Teorema Central do Limite (amostragem repetida sobre uma variável real do dataset).
3. **Distribuições teóricas** — ajuste de Normal e Exponencial aos dados reais, com discussão de quando o ajuste falha.
4. **Correlação e regressão** — dispersão, reta de mínimos quadrados, R², previsão interativa limitada ao intervalo observado.
5. **Descobertas** — 3 achados sobre o dataset, descritos abaixo.

## As 3 descobertas

1. **Frete pesa mais pra quem mora longe**: em São Paulo, o frete representa em média 25,1% do valor do produto, no Maranhão chega a 53,7%, quase o dobro.
2. **Frete tem parte fixa e parte por peso**: correlação moderada (r = 0,50) entre peso do produto e valor do frete, regressão estima parte fixa de R$ 16,75 mais aproximadamente R$ 2,88 por quilo.
3. **Atraso na entrega está associado a nota mais baixa**: nota média 4,29 para pedidos no prazo, contra 2,28 para pedidos atrasados.

Detalhes completos, fórmulas, tabela de validação e as 3 descobertas com todos os números estão no [RELATORIO.md](RELATORIO.md). Uma versão resumida está no [RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md).
