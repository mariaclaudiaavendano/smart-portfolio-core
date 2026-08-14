"""Script de prueba de integración de SmartPortfolio.

TODO(Arquitecto): completar tras el merge de feat/modelos y feat/logica.
"""

from src.modelos import Instrumento, Posicion
from src.portafolio import Portafolio
from src.reportes import ReportadorFinanciero


def main() -> None:
    print("SmartPortfolio Core - Iniciando sistema...")

    # 1. Definir Activos
    apple = Instrumento(ticker="AAPL", tipo="Acción", sector="Tecnología")
    tesoro = Instrumento(ticker="US10Y", tipo="Bono", sector="Gobierno")

    # 2. Crear Operaciones (Con validación automática de cantidad >= 0)
    pos1 = Posicion(instrumento=apple, cantidad=10, precio_entrada=150)
    pos2 = Posicion(instrumento=tesoro, cantidad=5, precio_entrada=100)

    # 3. Gestionar Portafolio
    fondo = Portafolio()
    fondo.agregar_posicion(pos1)
    fondo.agregar_posicion(pos2)

    # 4. Reportar (SOLID en acción)
    reportador = ReportadorFinanciero()
    
    # Usamos imprimir_resumen tal como lo pide la rúbrica
    reportador.imprimir_resumen(fondo)


if __name__ == "__main__":
    main()