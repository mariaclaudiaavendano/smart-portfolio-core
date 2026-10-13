from fastapi import FastAPI

from src.modelos import Instrumento, Posicion
from src.portafolio import Portafolio

app = FastAPI(
    title="SmartPortfolio Core API",
    description="API para consultar posiciones de un portafolio financiero.",
    version="1.0.0",
)

# Portafolio de ejemplo para demostrar la API.
portafolio = Portafolio()
portafolio.agregar_posicion(
    Posicion(
        instrumento=Instrumento(ticker="AAPL", tipo="Acción", sector="Tecnología"),
        cantidad=10,
        precio_entrada=150,
    )
)
portafolio.agregar_posicion(
    Posicion(
        instrumento=Instrumento(ticker="US10Y", tipo="Bono", sector="Gobierno"),
        cantidad=5,
        precio_entrada=100,
    )
)


@app.get("/")
def inicio() -> dict[str, str]:
    return {"mensaje": "SmartPortfolio Core API funcionando"}


@app.get("/posiciones")
def consultar_posiciones() -> dict[str, object]:
    posiciones = [
        {
            "ticker": posicion.instrumento.ticker,
            "tipo": posicion.instrumento.tipo,
            "sector": posicion.instrumento.sector,
            "cantidad": posicion.cantidad,
            "precio_entrada": posicion.precio_entrada,
        }
        for posicion in portafolio.posiciones
    ]
    return {
        "cantidad_posiciones": portafolio.cantidad_posiciones(),
        "posiciones": posiciones,
    }
