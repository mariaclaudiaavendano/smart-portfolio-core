"""Capa de presentación de reportes (SRP)."""

import csv
import json
from pathlib import Path

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

    def exportar_json(self, portafolio: Portafolio, ruta: str = "portafolio.json") -> None:
        """Exporta el portafolio a un archivo JSON."""
        datos = []
        for posicion in portafolio.posiciones:
            datos.append({
                "ticker": posicion.instrumento.ticker,
                "tipo": posicion.instrumento.tipo,
                "sector": posicion.instrumento.sector,
                "cantidad": posicion.cantidad,
                "precio_entrada": posicion.precio_entrada,
                "costo_total": posicion.cantidad * posicion.precio_entrada,
            })
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print(f"✅ Portafolio exportado a {ruta}")

    def exportar_csv(self, portafolio: Portafolio, ruta: str = "portafolio.csv") -> None:
        """Exporta el portafolio a un archivo CSV."""
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "ticker", "tipo", "sector", "cantidad", "precio_entrada", "costo_total"
            ])
            writer.writeheader()
            for posicion in portafolio.posiciones:
                writer.writerow({
                    "ticker": posicion.instrumento.ticker,
                    "tipo": posicion.instrumento.tipo,
                    "sector": posicion.instrumento.sector,
                    "cantidad": posicion.cantidad,
                    "precio_entrada": posicion.precio_entrada,
                    "costo_total": posicion.cantidad * posicion.precio_entrada,
                })
        print(f"✅ Portafolio exportado a {ruta}")
