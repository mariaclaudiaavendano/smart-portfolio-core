# src/instrumento_inteligente.py
"""
Domain Layer — Instrumento Inteligente con ML encapsulado.

El objeto Instrumento ya no solo almacena precios:
ahora entrena modelos y predice tendencias.
Esto es Domain-Driven Data Science.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class Instrumento:
    """
    Instrumento financiero inteligente.

    Recibe un data_provider por inyección de dependencias:
    - En producción → YahooFinanceClient
    - En tests      → MockDataProvider

    Esto desacopla los datos de la lógica de predicción.
    """

    def __init__(self, ticker: str, data_provider) -> None:
        self.ticker = ticker.upper()
        self.provider = data_provider
        self._history: pd.DataFrame = pd.DataFrame()
        self._modelo = LinearRegression()
        self._entrenado = False

    def _cargar_historia(self) -> None:
        """Carga datos del proveedor si aún no están en memoria."""
        if self._history.empty:
            self._history = self.provider.obtener_historia(self.ticker)

    def entrenar_modelo(self) -> None:
        """Entrena una regresión lineal sobre precios de cierre históricos."""
        self._cargar_historia()
        df = self._history.reset_index()
        X = df.index.values.reshape(-1, 1)
        y = df["Close"].values
        self._modelo.fit(X, y)
        self._entrenado = True
        print(f"🤖 Modelo entrenado para {self.ticker}")

    def predecir_precio(self, dias_futuros: int = 1) -> float:
        """
        Predice el precio para N días en el futuro.

        Args:
            dias_futuros: Días desde hoy a predecir. Default: 1.

        Returns:
            Precio estimado como float.
        """
        if not self._entrenado:
            self.entrenar_modelo()
        ultimo_indice = len(self._history)
        dia_objetivo = ultimo_indice + dias_futuros
        pred = self._modelo.predict([[dia_objetivo]])
        return float(pred[0])

    def predecir_tendencia(self, dias_futuros: int = 7) -> str:
        """
        Retorna 'ALCISTA' o 'BAJISTA' comparando precio actual vs predicción.

        Args:
            dias_futuros: Horizonte de predicción. Default: 7 días.
        """
        precio_actual = self.provider.obtener_precio_actual(self.ticker)
        precio_futuro = self.predecir_precio(dias_futuros)
        if precio_futuro > precio_actual:
            return "ALCISTA 📈"
        return "BAJISTA 📉"


class Posicion:
    """
    Posición financiera con alerta de riesgo automática.

    alerta_riesgo se activa si la pérdida supera el 10%.
    """

    def __init__(self, instrumento: Instrumento, cantidad: float, precio_entrada: float) -> None:
        self.instrumento = instrumento
        self.cantidad = cantidad
        self.precio_entrada = precio_entrada

    @property
    def alerta_riesgo(self) -> bool:
        """
        True si la pérdida no realizada supera el 10% del costo.
        Requiere que el provider pueda dar precio actual.
        """
        precio_actual = self.instrumento.provider.obtener_precio_actual(
            self.instrumento.ticker
        )
        perdida_pct = (precio_actual - self.precio_entrada) / self.precio_entrada * 100
        return perdida_pct < -10

    def calcular_ganancia_no_realizada(self, precio_actual: float) -> float:
        return (precio_actual - self.precio_entrada) * self.cantidad