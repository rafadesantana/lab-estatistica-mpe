import numpy as np
import pytest
from scipy import stats

from core.minhastats import (
    media, mediana, moda, amplitude, variancia, desvio_padrao,
    quartis, percentil, coeficiente_variacao,
    covariancia, correlacao_pearson, regressao_linear_simples, r_quadrado,
    numero_classes_sturges, tabela_frequencias,
    limites_outliers, outliers,
    densidade_normal, densidade_exponencial,
)

DADOS_A = [4, 8, 15, 16, 23, 42]
DADOS_B = [2.5, 3.1, 7.4, 8.8, 9.9, 12.0]
DADOS_C = np.random.default_rng(42).gamma(2, 9, 60).tolist()
DADOS_D = np.random.default_rng(7).gamma(2, 9, 60).tolist()

TOLERANCIA = 1e-9


def test_media():
    assert media(DADOS_A) == pytest.approx(np.mean(DADOS_A), rel=TOLERANCIA)


def test_media_dataset_maior():
    assert media(DADOS_C) == pytest.approx(np.mean(DADOS_C), rel=TOLERANCIA)


def test_media_vazia_levanta_erro():
    with pytest.raises(ValueError):
        media([])


def test_mediana():
    assert mediana(DADOS_A) == pytest.approx(np.median(DADOS_A), rel=TOLERANCIA)


def test_amplitude():
    assert amplitude(DADOS_A) == pytest.approx(np.ptp(DADOS_A), rel=TOLERANCIA)


def test_moda():
    assert moda([1, 2, 2, 3]) == [2]


def test_variancia_amostral():
    assert variancia(DADOS_A, amostral=True) == pytest.approx(np.var(DADOS_A, ddof=1), rel=TOLERANCIA)


def test_variancia_populacional():
    assert variancia(DADOS_A, amostral=False) == pytest.approx(np.var(DADOS_A, ddof=0), rel=TOLERANCIA)


def test_variancia_dataset_maior():
    assert variancia(DADOS_C, amostral=True) == pytest.approx(np.var(DADOS_C, ddof=1), rel=TOLERANCIA)
    assert variancia(DADOS_C, amostral=False) == pytest.approx(np.var(DADOS_C, ddof=0), rel=TOLERANCIA)


def test_variancia_amostral_n_menor_que_2_levanta_erro():
    with pytest.raises(ValueError):
        variancia([5], amostral=True)


def test_desvio_padrao():
    assert desvio_padrao(DADOS_A, amostral=True) == pytest.approx(np.std(DADOS_A, ddof=1), rel=TOLERANCIA)


def test_quartis():
    q1, q2, q3 = quartis(DADOS_A)
    assert q1 == pytest.approx(np.percentile(DADOS_A, 25), rel=TOLERANCIA)
    assert q2 == pytest.approx(np.percentile(DADOS_A, 50), rel=TOLERANCIA)
    assert q3 == pytest.approx(np.percentile(DADOS_A, 75), rel=TOLERANCIA)


def test_percentil():
    assert percentil(DADOS_A, 90) == pytest.approx(np.percentile(DADOS_A, 90), rel=TOLERANCIA)


def test_coeficiente_variacao():
    esperado = (np.std(DADOS_A, ddof=1) / np.mean(DADOS_A)) * 100
    assert coeficiente_variacao(DADOS_A, amostral=True) == pytest.approx(esperado, rel=TOLERANCIA)


def test_coeficiente_variacao_media_zero_levanta_erro():
    with pytest.raises(ValueError):
        coeficiente_variacao([-1, 1])


def test_covariancia_amostral():
    esperado = np.cov(DADOS_A, DADOS_B, ddof=1)[0][1]
    assert covariancia(DADOS_A, DADOS_B, amostral=True) == pytest.approx(esperado, rel=TOLERANCIA)


def test_covariancia_populacional():
    esperado = np.cov(DADOS_A, DADOS_B, ddof=0)[0][1]
    assert covariancia(DADOS_A, DADOS_B, amostral=False) == pytest.approx(esperado, rel=TOLERANCIA)


def test_covariancia_tamanhos_diferentes_levanta_erro():
    with pytest.raises(ValueError):
        covariancia([1, 2, 3], [1, 2])


def test_correlacao_pearson():
    esperado, _ = stats.pearsonr(DADOS_A, DADOS_B)
    assert correlacao_pearson(DADOS_A, DADOS_B) == pytest.approx(esperado, rel=TOLERANCIA)


def test_correlacao_pearson_dataset_maior():
    esperado, _ = stats.pearsonr(DADOS_C, DADOS_D)
    assert correlacao_pearson(DADOS_C, DADOS_D) == pytest.approx(esperado, rel=TOLERANCIA)


def test_correlacao_pearson_variavel_constante_levanta_erro():
    with pytest.raises(ValueError):
        correlacao_pearson([1, 1, 1], [1, 2, 3])


def test_regressao_linear_simples():
    b_esperado, a_esperado, r, p, erro_padrao = stats.linregress(DADOS_A, DADOS_B)
    a, b = regressao_linear_simples(DADOS_A, DADOS_B)
    assert a == pytest.approx(a_esperado, rel=TOLERANCIA)
    assert b == pytest.approx(b_esperado, rel=TOLERANCIA)


def test_regressao_linear_simples_dataset_maior():
    b_esperado, a_esperado, r, p, erro_padrao = stats.linregress(DADOS_C, DADOS_D)
    a, b = regressao_linear_simples(DADOS_C, DADOS_D)
    assert a == pytest.approx(a_esperado, rel=TOLERANCIA)
    assert b == pytest.approx(b_esperado, rel=TOLERANCIA)


def test_regressao_linear_simples_x_constante_levanta_erro():
    with pytest.raises(ValueError):
        regressao_linear_simples([5, 5, 5], [1, 2, 3])


def test_r_quadrado():
    _, _, r, _, _ = stats.linregress(DADOS_A, DADOS_B)
    assert r_quadrado(DADOS_A, DADOS_B) == pytest.approx(r ** 2, rel=TOLERANCIA)


def test_numero_classes_sturges():
    assert numero_classes_sturges(6) == 4


def test_tabela_frequencias():
    tabela = tabela_frequencias(DADOS_B, num_classes=4)
    contagens_esperadas, bordas_esperadas = np.histogram(DADOS_B, bins=4)

    frequencias_obtidas = [classe["frequencia_absoluta"] for classe in tabela]
    assert frequencias_obtidas == list(contagens_esperadas)

    assert tabela[0]["limite_inferior"] == pytest.approx(bordas_esperadas[0], rel=TOLERANCIA)
    assert tabela[-1]["limite_superior"] == pytest.approx(bordas_esperadas[-1], rel=TOLERANCIA)

    assert sum(frequencias_obtidas) == len(DADOS_B)
    assert tabela[-1]["frequencia_acumulada"] == len(DADOS_B)
    assert tabela[-1]["frequencia_relativa_acumulada"] == pytest.approx(100.0, rel=TOLERANCIA)


def test_limites_outliers():
    q1 = np.percentile(DADOS_A, 25)
    q3 = np.percentile(DADOS_A, 75)
    iqr = q3 - q1
    esperado_inferior = q1 - 1.5 * iqr
    esperado_superior = q3 + 1.5 * iqr

    limite_inferior, limite_superior = limites_outliers(DADOS_A)
    assert limite_inferior == pytest.approx(esperado_inferior, rel=TOLERANCIA)
    assert limite_superior == pytest.approx(esperado_superior, rel=TOLERANCIA)


def test_outliers():
    q1 = np.percentile(DADOS_A, 25)
    q3 = np.percentile(DADOS_A, 75)
    iqr = q3 - q1
    esperado = [x for x in DADOS_A if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr]

    assert outliers(DADOS_A) == esperado


def test_densidade_normal():
    m, s = 10, 2
    x = 11
    esperado = stats.norm.pdf(x, loc=m, scale=s)
    assert densidade_normal(x, m, s) == pytest.approx(esperado, rel=TOLERANCIA)


def test_densidade_exponencial():
    taxa = 0.5
    x = 3
    esperado = stats.expon.pdf(x, scale=1 / taxa)
    assert densidade_exponencial(x, taxa) == pytest.approx(esperado, rel=TOLERANCIA)
