# Resumo Executivo — Laboratório Estatístico Interativo

**Rafael Leandro Pereira de Santana** — matrícula 72650038

## Dataset

Brazilian E-Commerce Public Dataset by Olist (Kaggle, dados reais de e-commerce no Brasil, outubro de 2016 a agosto de 2018). A partir das 9 tabelas originais, construí uma base analítica única com 94.472 pedidos entregues, 13 variáveis numéricas e 3 categóricas.

## Módulos

A aplicação (Streamlit) tem um núcleo estatístico próprio de 19 funções em Python puro, validado por 31 testes automatizados contra NumPy e SciPy, com diferenças na ordem de 1e-9 ou menores. Sobre esse núcleo, foram construídos: estatística descritiva interativa (com interpretação automática de assimetria), simulação de Monte Carlo (Lei dos Grandes Números e Teorema Central do Limite sobre dados reais), ajuste de distribuições teóricas (Normal e Exponencial), e correlação e regressão linear com previsão interativa limitada ao intervalo observado.

## As 3 descobertas

1. **Frete pesa mais para quem mora longe.** Em São Paulo, o frete representa 25,1% do valor do produto comprado, em média. No Maranhão, chega a 53,7%, quase o dobro, refletindo a distância até os centros de distribuição, concentrados no Sudeste.
2. **Frete tem parte fixa e parte por peso.** A correlação entre peso do produto e valor do frete é moderada (r = 0,50). A regressão estima uma parte fixa de R$ 16,75, mais aproximadamente R$ 2,88 por quilo, explicando 25,2% da variação do frete.
3. **Atraso na entrega está associado a nota mais baixa.** Pedidos no prazo recebem nota média 4,29, contra 2,28 para pedidos atrasados, uma queda de 2,01 pontos numa escala de 1 a 5. Apenas 6,7% dos pedidos atrasam, mas o impacto na satisfação é forte.

Todas as descobertas são leituras associativas da amostra (2016–2018), não relações de causa e efeito comprovadas.
