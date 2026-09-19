import math

def media(dados):
    """Media aritmetica, soma de todos os valores dividida pela quantidade de valores."""
    if len(dados) == 0:
        raise ValueError("media de sequencia vazia e indefinida")
    return sum(dados) / len(dados)


def mediana(dados):
    """Mediana, valor do meio da lista ordenada, ou media dos dois valores do meio quando n e par."""
    ordenados = sorted(dados)
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 1:
        return ordenados[meio]
    else:
        return (ordenados[meio - 1] + ordenados[meio]) / 2


def moda(dados):
    """Moda, valor ou valores que aparecem com mais frequencia na lista."""
    contagem = {}
    for valor in dados:
        if valor in contagem:
            contagem[valor] = contagem[valor] + 1
        else:
            contagem[valor] = 1
    maior_contagem = max(contagem.values())
    modas = [valor for valor, vezes in contagem.items() if vezes == maior_contagem]
    return modas


def amplitude(dados):
    """Amplitude, diferenca entre o maior e o menor valor da lista."""
    return max(dados) - min(dados)


def variancia(dados, amostral=True):
    """Variancia, mede o quanto os dados se espalham em torno da media, amostral=True divide por n-1 (correcao de Bessel), False divide por n."""
    n = len(dados)
    if amostral and n < 2:
        raise ValueError("variancia amostral exige n >= 2")
    if not amostral and n < 1:
        raise ValueError("variancia populacional exige n >= 1")
    m = media(dados)
    soma_quadrados = sum((x - m) ** 2 for x in dados)
    if amostral:
        return soma_quadrados / (n - 1)
    else:
        return soma_quadrados / n


def desvio_padrao(dados, amostral=True):
    """Desvio padrao, raiz quadrada da variancia, na mesma unidade dos dados originais."""
    return variancia(dados, amostral) ** 0.5


def percentil(dados, p):
    """Percentil p, valor abaixo do qual fica p por cento dos dados, com interpolacao linear entre os vizinhos."""
    ordenados = sorted(dados)
    n = len(ordenados)
    indice = (p / 100) * (n - 1)
    indice_baixo = int(indice)
    indice_alto = min(indice_baixo + 1, n - 1)
    fracao = indice - indice_baixo
    return ordenados[indice_baixo] + fracao * (ordenados[indice_alto] - ordenados[indice_baixo])


def quartis(dados):
    """Quartis, retorna Q1, Q2 (mediana) e Q3, os percentis 25, 50 e 75."""
    q1 = percentil(dados, 25)
    q2 = percentil(dados, 50)
    q3 = percentil(dados, 75)
    return q1, q2, q3


def coeficiente_variacao(dados, amostral=True):
    """Coeficiente de variacao, desvio padrao dividido pela media, em porcentagem, mede a dispersao relativa."""
    m = media(dados)
    if m == 0:
        raise ValueError("coeficiente de variacao indefinido para media zero")
    return (desvio_padrao(dados, amostral) / m) * 100


def covariancia(x, y, amostral=True):
    """Covariancia, mede se duas variaveis crescem juntas ou em direcoes opostas."""
    if len(x) != len(y):
        raise ValueError("x e y precisam ter o mesmo tamanho")
    media_x = media(x)
    media_y = media(y)
    soma = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
    n = len(x)
    if amostral:
        return soma / (n - 1)
    else:
        return soma / n


def correlacao_pearson(x, y):
    """Correlacao de Pearson, mede a forca e a direcao da relacao linear entre x e y, varia entre -1 e 1."""
    desvio_x = desvio_padrao(x)
    desvio_y = desvio_padrao(y)
    if desvio_x == 0 or desvio_y == 0:
        raise ValueError("correlacao indefinida quando uma variavel e constante (desvio zero)")
    return covariancia(x, y) / (desvio_x * desvio_y)


def regressao_linear_simples(x, y):
    """Regressao linear simples, calcula a reta y = a + b*x que melhor se ajusta aos dados pelo metodo dos minimos quadrados."""
    variancia_x = variancia(x)
    if variancia_x == 0:
        raise ValueError("regressao indefinida quando x e constante (variancia zero)")
    b = covariancia(x, y) / variancia_x
    a = media(y) - b * media(x)
    return a, b


def r_quadrado(x, y):
    """R quadrado, proporcao da variacao de y que e explicada pela reta de regressao."""
    r = correlacao_pearson(x, y)
    return r ** 2


def numero_classes_sturges(n):
    """Numero de classes do histograma, pela regra de Sturges."""
    return round(1 + 3.322 * math.log10(n))


def tabela_frequencias(dados, num_classes=None):
    """Tabela de frequencias, divide os dados em classes e calcula frequencia absoluta, relativa e acumulada de cada uma."""
    if num_classes is None:
        num_classes = numero_classes_sturges(len(dados))

    minimo = min(dados)
    maximo = max(dados)
    largura = (maximo - minimo) / num_classes

    classes = []
    limite_inferior = minimo
    for i in range(num_classes):
        limite_superior = limite_inferior + largura
        if i == num_classes - 1:
            frequencia = sum(1 for x in dados if limite_inferior <= x <= limite_superior)
        else:
            frequencia = sum(1 for x in dados if limite_inferior <= x < limite_superior)
        classes.append({
            "limite_inferior": limite_inferior,
            "limite_superior": limite_superior,
            "frequencia_absoluta": frequencia,
        })
        limite_inferior = limite_superior

    n = len(dados)
    acumulada = 0
    for classe in classes:
        classe["frequencia_relativa"] = (classe["frequencia_absoluta"] / n) * 100
        acumulada += classe["frequencia_absoluta"]
        classe["frequencia_acumulada"] = acumulada
        classe["frequencia_relativa_acumulada"] = (acumulada / n) * 100

    return classes


def limites_outliers(dados):
    """Limites de outliers, calcula o limite inferior e superior pela regra do IQR (1,5 vezes a distancia interquartil)."""
    q1, q2, q3 = quartis(dados)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    return limite_inferior, limite_superior


def outliers(dados):
    """Outliers, lista os valores que ficam fora dos limites calculados pela regra do IQR."""
    limite_inferior, limite_superior = limites_outliers(dados)
    return [x for x in dados if x < limite_inferior or x > limite_superior]


def densidade_normal(x, m, s):
    """Densidade da distribuicao Normal no ponto x, dados a media m e o desvio padrao s."""
    expoente = -((x - m) ** 2) / (2 * s ** 2)
    return (1 / (s * math.sqrt(2 * math.pi))) * math.exp(expoente)


def densidade_exponencial(x, taxa):
    """Densidade da distribuicao Exponencial no ponto x, dada a taxa, retorna zero para x negativo."""
    if x < 0:
        return 0.0
    return taxa * math.exp(-taxa * x)
