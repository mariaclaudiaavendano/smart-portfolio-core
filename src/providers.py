# src/providers.py
"""
Data Layer — Proveedores de datos de mercado.

SRP: Este módulo SOLO se encarga de obtener datos externos.
La lógica de predicción vive en Instrumento.
"""

import pandas as pd


class YahooFinanceClient:
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


class MockDataProvider:
    """
    Proveedor simulado para tests — no llama a internet.

    Inyectas datos predefinidos y el modelo se entrena sobre ellos.
    En tests → usas esto.
    En producción → usas YahooFinanceClient.
    """

    def __init__(self, precios: list[float] | None = None) -> None:
        if precios is None:
            # Datos sintéticos con tendencia alcista
            self.precios = [100 + i * 2.5 for i in range(252)]
        else:
            self.precios = precios

    def obtener_historia(self, ticker: str) -> pd.DataFrame:
        import numpy as np
        fechas = pd.date_range(end=pd.Timestamp.today(), periods=len(self.precios), freq="B")
        return pd.DataFrame({"Close": self.precios}, index=fechas)

    def obtener_precio_actual(self, ticker: str) -> float:
        return self.precios[-1]