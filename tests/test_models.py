import pytest
from dataclasses import FrozenInstanceError

from src.modelos import Instrumento, Posicion

from src.portafolio import Portafolio

from src.reportes import ReportadorFinanciero


def test_crear_instrumento():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    assert instrumento.ticker == "TSLA"
    assert instrumento.tipo == "Acción"
    assert instrumento.sector == "Tecnología"


def test_instrumento_no_se_puede_modificar():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    with pytest.raises(FrozenInstanceError):
        instrumento.ticker = "AAPL"


def test_crear_posicion():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    assert posicion.instrumento == instrumento
    assert posicion.cantidad == 10
    assert posicion.precio_entrada == 200


def test_posicion_no_permite_cantidad_negativa():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    with pytest.raises(ValueError, match="La cantidad NO puede ser negativa."):
        Posicion(
            instrumento=instrumento,
            cantidad=-1,
            precio_entrada=200,
        )


def test_modificar_cantidad():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    posicion.cantidad = 15

    assert posicion.cantidad == 15

def test_modificar_cantidad_no_permite_negativos():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    with pytest.raises(ValueError, match="La cantidad NO puede ser negativa."):
        posicion.cantidad = -1


def test_calcular_valor_actual():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    resultado = posicion.calcular_valor_actual(250)

    assert resultado == 2500

def test_calcular_valor_actual_con_precio_cero():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    resultado = posicion.calcular_valor_actual(0)

    assert resultado == 0

def test_posicion_permite_cantidad_cero(instrumento_test):
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=0,
        precio_entrada=100.0,
    )

    assert posicion.cantidad == 0

def test_portafolio_vacio():
    portafolio = Portafolio()

    assert portafolio.cantidad_posiciones() == 0


def test_agregar_posicion():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    portafolio = Portafolio()
    portafolio.agregar_posicion(posicion)

    assert portafolio.cantidad_posiciones() == 1
    assert posicion in portafolio.posiciones


def test_eliminar_posicion():
    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    portafolio = Portafolio()
    portafolio.agregar_posicion(posicion)
    portafolio.eliminar_posicion(posicion)

    assert portafolio.cantidad_posiciones() == 0

def test_eliminar_posicion_inexistente():
    portafolio = Portafolio()

    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    with pytest.raises(ValueError):
        portafolio.eliminar_posicion(posicion)

def test_reportador_financiero_portafolio_vacio():
    portafolio = Portafolio()
    reportador = ReportadorFinanciero()

    resultado = reportador.imprimir_resumen(portafolio)

    assert resultado == "El portafolio contiene 0 posiciones."

def test_agregar_varias_posiciones():
    instrumento1 = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    instrumento2 = Instrumento(
        ticker="AAPL",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion1 = Posicion(
        instrumento=instrumento1,
        cantidad=10,
        precio_entrada=200,
    )

    posicion2 = Posicion(
        instrumento=instrumento2,
        cantidad=5,
        precio_entrada=150,
    )

    portafolio = Portafolio()

    portafolio.agregar_posicion(posicion1)
    portafolio.agregar_posicion(posicion2)

    assert portafolio.cantidad_posiciones() == 2
    assert posicion1 in portafolio.posiciones
    assert posicion2 in portafolio.posiciones

def test_posiciones_devuelve_una_copia():
    portafolio = Portafolio()

    instrumento = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    posicion = Posicion(
        instrumento=instrumento,
        cantidad=10,
        precio_entrada=200,
    )

    portafolio.agregar_posicion(posicion)

    posiciones = portafolio.posiciones
    posiciones.clear()

    assert portafolio.cantidad_posiciones() == 1

def test_reportador_financiero_con_una_posicion(instrumento_test):


    portafolio = Portafolio()
    posicion = Posicion(
        instrumento_test,
        cantidad=10,
        precio_entrada=100
    )

    portafolio.agregar_posicion(posicion)

    reportador = ReportadorFinanciero()
    resultado = reportador.imprimir_resumen(portafolio)

    assert resultado == "El portafolio contiene 1 posiciones."

def test_reportador_financiero_con_varias_posiciones():
    instrumento_1 = Instrumento(
        ticker="TSLA",
        tipo="Acción",
        sector="Tecnología",
    )

    instrumento_2 = Instrumento(
        ticker="AAPL",
        tipo="Acción",
        sector="Tecnología",
    )

    portafolio = Portafolio()

    portafolio.agregar_posicion(
        Posicion(instrumento_1, cantidad=10, precio_entrada=200)
    )

    portafolio.agregar_posicion(
        Posicion(instrumento_2, cantidad=5, precio_entrada=150)
    )

    reportador = ReportadorFinanciero()

    resultado = reportador.imprimir_resumen(portafolio)

    assert resultado == "El portafolio contiene 2 posiciones."
