"""Capa de presentación de reportes (SRP)."""

from src.portafolio import Portafolio


class ReportadorFinanciero:
    """Genera reportes a partir de un portafolio."""

    def imprimir_resumen(self, portafolio: Portafolio) -> str:
        """Genera un resumen textual del portafolio."""
        cantidad = portafolio.cantidad_posiciones()
        lineas = [
            "=" * 40,
            "   RESUMEN DEL PORTAFOLIO",
            "=" * 40,
            f"Total de posiciones: {cantidad}",
        ]

        for posicion in portafolio.posiciones:
            costo_total = posicion.cantidad * posicion.precio_entrada
            lineas.append(
                f"  - {posicion.instrumento.ticker}: "
                f"{posicion.cantidad} unidades @ "
                f"${posicion.precio_entrada:.2f} "
                f"| Costo total: ${costo_total:.2f}"
            )

        lineas.append("=" * 40)
        return "\n".join(lineas)
