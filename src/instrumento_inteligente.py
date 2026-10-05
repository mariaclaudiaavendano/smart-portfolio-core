# src/instrumento_inteligente.py
"""
Instrumento Inteligente con ML encapsulado.
Importa Instrumento y Posicion de modelos.py para evitar duplicación.
"""

import pandas as pd
from sklearn.linear_model import LinearRegression

from src.modelos import Instrumento, Posicion


class InstrumentoInteligente(Instrumento):
    """
    Extiende Instrumento con capacidades de ML.
    Recibe un data_provider por inyección de dependencias.
    """

    def __init__(self, ticker: str, tipo: str, sector: str, data_provider) -> None:
        super().__init__(ticker=ticker, tipo=tipo, sector=sector)
        self.provider = data_provider
        self._history: pd.DataFrame = pd.DataFrame()
        self._modelo = LinearRegression()
        self._entrenado = False

    def _cargar_historia(self) -> None:
        if self._history.empty:
            self._history = self.provider.obtener_historia(self.ticker)

    def entrenar_modelo(self) -> None:
        self._cargar_historia()
        df = self._history.reset_index()
        X = df.index.values.reshape(-1, 1)
        y = df["Close"].values
        self._modelo.fit(X, y)
        self._entrenado = True
        print(f" Modelo entrenado para {self.ticker}")

    def predecir_precio(self, dias_futuros: int = 1) -> float:
        if not self._entrenado:
            self.entrenar_modelo()
        ultimo_indice = len(self._history)
        pred = self._modelo.predict([[ultimo_indice + dias_futuros]])
        return float(pred[0])

    def predecir_tendencia(self, dias_futuros: int = 7) -> str:
        precio_actual = self.provider.obtener_precio_actual(self.ticker)
        precio_futuro = self.predecir_precio(dias_futuros)
        if precio_futuro > precio_actual:
            return "ALCISTA"
        return "BAJISTA"