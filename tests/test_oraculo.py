# tests/test_oraculo.py
import pytest
from src.providers import MockDataProvider
from src.instrumento_inteligente import Instrumento, Posicion


@pytest.fixture
def provider_mock():
    precios = [100 + i * 2.5 for i in range(100)]
    return MockDataProvider(precios=precios)


@pytest.fixture
def instrumento_mock(provider_mock):
    return Instrumento(ticker="TSLA", data_provider=provider_mock)


@pytest.mark.parametrize("dias", [1, 7, 30])
def test_predecir_precio_retorna_float(instrumento_mock, dias):
    precio = instrumento_mock.predecir_precio(dias_futuros=dias)
    assert isinstance(precio, float)


def test_tendencia_alcista_con_datos_crecientes(instrumento_mock):
    tendencia = instrumento_mock.predecir_tendencia(dias_futuros=7)
    assert "ALCISTA" in tendencia


def test_tendencia_bajista_con_datos_decrecientes():
    precios = [300 - i * 2 for i in range(100)]
    provider = MockDataProvider(precios=precios)
    instrumento = Instrumento(ticker="TEST", data_provider=provider)
    tendencia = instrumento.predecir_tendencia(dias_futuros=7)
    assert "BAJISTA" in tendencia


def test_alerta_riesgo_true_con_perdida_mayor_10():
    precios = [100.0] * 100
    provider = MockDataProvider(precios=precios)
    instrumento = Instrumento(ticker="TSLA", data_provider=provider)
    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=120.0,
    )
    assert posicion.alerta_riesgo is True
