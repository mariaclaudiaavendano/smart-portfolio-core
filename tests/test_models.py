# tests/test_models.py
import pytest

from src.modelos import Instrumento, Posicion
from src.portafolio import Portafolio, PosicionNoExisteError


# B) Tests parametrizados
@pytest.mark.parametrize(
    "precio_entrada, precio_actual, cantidad, esperado",
    [
        (100, 150, 10,  500),
        (200, 180,  5, -100),
        ( 50,  50,  7,    0),
    ],
)
def test_calculo_pnl(
    precio_entrada,
    precio_actual,
    cantidad,
    esperado,
    instrumento_test,
):
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=cantidad,
        precio_entrada=precio_entrada,
    )
    pnl = posicion.calcular_ganancia_no_realizada(
        precio_actual=precio_actual
    )
    assert pnl == pytest.approx(esperado)


# C) Unhappy path
def test_remover_activo_inexistente_lanza_error(portafolio_vacio):
    with pytest.raises(PosicionNoExisteError):
        portafolio_vacio.remover_posicion(ticker="NFLX")


# D) Tests adicionales para subir coverage
def test_calcular_valor_actual(instrumento_test):
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=10,
        precio_entrada=100,
    )
    assert posicion.calcular_valor_actual(200) == pytest.approx(2000)


def test_cantidad_cero_es_valida(instrumento_test):
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=0,
        precio_entrada=100,
    )
    assert posicion.cantidad == pytest.approx(0)


# E) Tests de reportes
def test_reportador_portafolio_vacio(portafolio_vacio):
    from src.reportes import ReportadorFinanciero
    reportador = ReportadorFinanciero()
    resultado = reportador.imprimir_resumen(portafolio_vacio)
    assert "Total de posiciones: 0" in resultado


def test_reportador_con_una_posicion(instrumento_test):
    from src.reportes import ReportadorFinanciero
    from src.portafolio import Portafolio
    from src.modelos import Posicion
    portafolio = Portafolio()
    posicion = Posicion(instrumento=instrumento_test, cantidad=10, precio_entrada=100)
    portafolio.agregar_posicion(posicion)
    reportador = ReportadorFinanciero()
    resultado = reportador.imprimir_resumen(portafolio)
    assert "Total de posiciones: 1" in resultado
    assert "TSLA" in resultado

def test_eliminar_posicion_existente(instrumento_test):
    from src.portafolio import Portafolio
    from src.modelos import Posicion
    portafolio = Portafolio()
    posicion = Posicion(instrumento=instrumento_test, cantidad=10, precio_entrada=100)
    portafolio.agregar_posicion(posicion)
    portafolio.eliminar_posicion(posicion)
    assert portafolio.cantidad_posiciones() == 0


def test_eliminar_posicion_inexistente_lanza_error(instrumento_test):
    from src.portafolio import Portafolio, PosicionNoExisteError
    from src.modelos import Posicion
    portafolio = Portafolio()
    posicion = Posicion(instrumento=instrumento_test, cantidad=10, precio_entrada=100)
    with pytest.raises(PosicionNoExisteError):
        portafolio.eliminar_posicion(posicion)
