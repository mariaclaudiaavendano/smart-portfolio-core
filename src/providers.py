# src/providers.py
"""Data Layer — Proveedores de datos de mercado."""

from abc import ABC, abstractmethod
import pandas as pd


class MarketDataProvider(ABC):
    """Clase abstracta que define el contrato para proveedores de datos."""

    @abstractmethod
    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        """Retorna el historial de precios del ticker."""
        pass

    @abstractmethod
    def obtener_precio_actual(self, ticker: str) -> float:
        """Retorna el precio actual del ticker."""
        pass


class YahooFinanceClient(MarketDataProvider):
    """Proveedor real — consulta Yahoo Finance."""

    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        import yfinance as yf
        t = yf.Ticker(ticker)
        return t.history(period="1y")

    def obtener_precio_actual(self, ticker: str) -> float:
        import yfinance as yf
        t = yf.Ticker(ticker)
        hist = t.history(period="1d")
        return float(hist["Close"].iloc[-1])


class MockDataProvider(MarketDataProvider):
    """Proveedor simulado para tests — no llama a internet."""

    def __init__(self, precios: list[float] | None = None) -> None:
        if precios is None:
            self.precios = [100 + i * 2.5 for i in range(252)]
        else:
            self.precios = precios

    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        fechas = pd.date_range(end=pd.Timestamp.today(), periods=len(self.precios), freq="B")
        return pd.DataFrame({"Close": self.precios}, index=fechas)

    def obtener_precio_actual(self, ticker: str) -> float:
        return self.precios[-1]
