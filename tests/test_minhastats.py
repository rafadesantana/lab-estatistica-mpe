import numpy as np
import pytest
from scipy import stats

from core.minhastats import (
    media, mediana, moda, amplitude, variancia, desvio_padrao,
    quartis, percentil, coeficiente_variacao,
    covariancia, correlacao_pearson, regressao_linear_simples, r_quadrado,
    numero_classes_sturges, tabela_frequencias,
)

DADOS_A = [4, 8, 15, 16, 23, 42]
DADOS_B = [2.5, 3.1, 7.4, 8.8, 9.9, 12.0]


def test_media():
    assert media(DADOS_A) == pytest.approx(np.mean(DADOS_A))


def test_mediana():
    assert mediana(DADOS_A) == pytest.approx(np.median(DADOS_A))


def test_amplitude():
    assert amplitude(DADOS_A) == pytest.approx(np.ptp(DADOS_A))


def test_moda():
    assert moda([1, 2, 2, 3]) == [2]


def test_variancia():
    assert variancia(DADOS_A, amostral=True) == pytest.approx(np.var(DADOS_A, ddof=1))


def test_desvio_padrao():
    assert desvio_padrao(DADOS_A, amostral=True) == pytest.approx(np.std(DADOS_A, ddof=1))


def test_quartis():
    q1, q2, q3 = quartis(DADOS_A)
    assert q1 == pytest.approx(np.percentile(DADOS_A, 25))
    assert q2 == pytest.approx(np.percentile(DADOS_A, 50))
    assert q3 == pytest.approx(np.percentile(DADOS_A, 75))


def test_percentil():
    assert percentil(DADOS_A, 90) == pytest.approx(np.percentile(DADOS_A, 90))


def test_coeficiente_variacao():
    esperado = (np.std(DADOS_A, ddof=1) / np.mean(DADOS_A)) * 100
    assert coeficiente_variacao(DADOS_A, amostral=True) == pytest.approx(esperado)


def test_covariancia():
    esperado = np.cov(DADOS_A, DADOS_B, ddof=1)[0][1]
    assert covariancia(DADOS_A, DADOS_B, amostral=True) == pytest.approx(esperado)


def test_correlacao_pearson():
    esperado, _ = stats.pearsonr(DADOS_A, DADOS_B)
    assert correlacao_pearson(DADOS_A, DADOS_B) == pytest.approx(esperado)


def test_regressao_linear_simples():
    b_esperado, a_esperado, r, p, erro_padrao = stats.linregress(DADOS_A, DADOS_B)
    a, b = regressao_linear_simples(DADOS_A, DADOS_B)
    assert a == pytest.approx(a_esperado)
    assert b == pytest.approx(b_esperado)


def test_r_quadrado():
    _, _, r, _, _ = stats.linregress(DADOS_A, DADOS_B)
    assert r_quadrado(DADOS_A, DADOS_B) == pytest.approx(r ** 2)


def test_numero_classes_sturges():
    # k = 1 + 3.322*log10(6) = 3.58... -> arredonda pra 4
    assert numero_classes_sturges(6) == 4


def test_tabela_frequencias():
    tabela = tabela_frequencias(DADOS_B, num_classes=4)
    contagens_esperadas, bordas_esperadas = np.histogram(DADOS_B, bins=4)

    frequencias_obtidas = [classe["frequencia_absoluta"] for classe in tabela]
    assert frequencias_obtidas == list(contagens_esperadas)

    assert tabela[0]["limite_inferior"] == pytest.approx(bordas_esperadas[0])
    assert tabela[-1]["limite_superior"] == pytest.approx(bordas_esperadas[-1])

    assert sum(frequencias_obtidas) == len(DADOS_B)
    assert tabela[-1]["frequencia_acumulada"] == len(DADOS_B)
    assert tabela[-1]["frequencia_relativa_acumulada"] == pytest.approx(100.0)