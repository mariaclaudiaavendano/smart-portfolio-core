"""Capa de presentación de reportes (SRP)."""

from src.portafolio import Portafolio


class ReportadorFinanciero:
    """Genera reportes a partir de un portafolio."""

    def imprimir_resumen(self, portafolio: Portafolio) -> str:
        """Genera un resumen textual del portafolio."""
        cantidad = portafolio.cantidad_posiciones()

        return f"El portafolio contiene {cantidad} posiciones."