"""Modelos de dominio financiero."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrumento:
    """Representa un instrumento financiero que no cambia."""
    ticker: str
    tipo: str
    sector: str


class Posicion:
    """Representa una posición financiera dentro del portafolio."""

    def __init__(self, instrumento: Instrumento, cantidad: float, precio_entrada: float) -> None:
        self.instrumento = instrumento
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

    def calcular_ganancia_no_realizada(self, precio_actual: float) -> float:
        """Calcula la ganancia o pérdida no realizada.

        Fórmula: (precio_actual - precio_entrada) × cantidad
        """
        return (precio_actual - self.precio_entrada) * self.cantidad

    @property
    def alerta_riesgo(self) -> bool:
        """True si la pérdida supera el 10% del costo de entrada."""
        if not hasattr(self.instrumento, 'provider'):
            return False
        precio_actual = self.instrumento.provider.obtener_precio_actual(
            self.instrumento.ticker
        )
        perdida_pct = (precio_actual - self.precio_entrada) / self.precio_entrada * 100
        return perdida_pct < -10