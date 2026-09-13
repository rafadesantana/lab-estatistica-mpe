import math

def media(dados):
    return sum(dados) / len(dados)


def mediana(dados):
    ordenados = sorted(dados)
    n = len(ordenados)
    meio = n // 2
    if n % 2 == 1:
        return ordenados[meio]
    else:
        return (ordenados[meio - 1] + ordenados[meio]) / 2


def moda(dados):
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
    return max(dados) - min(dados)


def variancia(dados, amostral=True):
    m = media(dados)
    soma_quadrados = sum((x - m) ** 2 for x in dados)
    n = len(dados)
    if amostral:
        return soma_quadrados / (n - 1)
    else:
        return soma_quadrados / n


def desvio_padrao(dados, amostral=True):
    return variancia(dados, amostral) ** 0.5


def percentil(dados, p):
    ordenados = sorted(dados)
    n = len(ordenados)
    indice = (p / 100) * (n - 1)
    indice_baixo = int(indice)
    indice_alto = min(indice_baixo + 1, n - 1)
    fracao = indice - indice_baixo
    return ordenados[indice_baixo] + fracao * (ordenados[indice_alto] - ordenados[indice_baixo])


def quartis(dados):
    q1 = percentil(dados, 25)
    q2 = percentil(dados, 50)
    q3 = percentil(dados, 75)
    return q1, q2, q3


def coeficiente_variacao(dados, amostral=True):
    return (desvio_padrao(dados, amostral) / media(dados)) * 100


def covariancia(x, y, amostral=True):
    media_x = media(x)
    media_y = media(y)
    soma = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
    n = len(x)
    if amostral:
        return soma / (n - 1)
    else:
        return soma / n


def correlacao_pearson(x, y):
    return covariancia(x, y) / (desvio_padrao(x) * desvio_padrao(y))


def regressao_linear_simples(x, y):
    b = covariancia(x, y) / variancia(x)
    a = media(y) - b * media(x)
    return a, b


def r_quadrado(x, y):
    r = correlacao_pearson(x, y)
    return r ** 2


def numero_classes_sturges(n):
    return round(1 + 3.322 * math.log10(n))


def tabela_frequencias(dados, num_classes=None):
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
    q1, q2, q3 = quartis(dados)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    return limite_inferior, limite_superior


def outliers(dados):
    limite_inferior, limite_superior = limites_outliers(dados)
    return [x for x in dados if x < limite_inferior or x > limite_superior]