"""Modelos del dominio financiero.

TODO(Dev 1 - rama feat/modelos): implementar Instrumento y Posicion.
"""

"""Modelos de dominio financiero."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrumento:
    """Representa un instrumento financiero que no cambia."""
    ticker: str
    tipo: str  # Ej: "Acción", "Bono"
    sector: str


class Posicion:
    """Representa una posición financiera dentro del portafolio."""

    def __init__(self, instrumento: Instrumento, cantidad: float, precio_entrada: float) -> None:
        self.instrumento = instrumento
        # Usamos un atributo protegido y llamamos al setter para validar de una vez
        self.cantidad = cantidad  
        self.precio_entrada = precio_entrada

    @property
    def cantidad(self) -> float:
        """Devuelve la cantidad."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: float) -> None:
        """Valida automáticamente que la cantidad no sea negativa."""
        if valor < 0:
            raise ValueError("La cantidad NO puede ser negativa.")
        self._cantidad = valor

    def calcular_valor_actual(self, precio_mercado: float) -> float:
        """Calcula el valor actual multiplicando cantidad por precio de mercado."""
        return self.cantidad * precio_mercado