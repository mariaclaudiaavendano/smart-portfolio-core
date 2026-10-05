# main_oraculo.py
"""
Aplicación CLI — Smart Portfolio Oracle.

Flujo exacto del taller:
1. Pedir ticker
2. Consultar precio actual
3. Predecir tendencia
4. Preguntar compra
5. Guardar JSON
"""

import json
from src.providers import YahooFinanceClient
from src.instrumento_inteligente import Instrumento, Posicion


def main() -> None:
    print("\n--- SMART PORTFOLIO ORACLE ---\n")

    # 1. Pedir ticker
    ticker = input("Ingrese Ticker: ").strip().upper()

    # 2. Obtener datos reales
    print("\nObteniendo datos... ", end="")
    provider = YahooFinanceClient()
    instrumento = Instrumento(ticker, provider)
    precio_actual = provider.obtener_precio_actual(ticker)
    print("OK")

    # 3. Entrenar modelo y predecir
    print("Entrenando modelo... ", end="")
    instrumento.entrenar_modelo()
    print("OK")

    precio_7d = instrumento.predecir_precio(dias_futuros=7)
    tendencia = instrumento.predecir_tendencia(dias_futuros=7)

    print(f"\n {ticker}")
    print(f"Precio actual: ${precio_actual:.2f}")
    print(f"Predicción 7 días: ${precio_7d:.2f} ({tendencia})")

    # 4. Preguntar compra
    comprar = input("\n¿Comprar? (s/n): ").strip().lower()

    if comprar == "s":
        cantidad = float(input("Cantidad: "))
        posicion = Posicion(
            instrumento=instrumento,
            cantidad=cantidad,
            precio_entrada=precio_actual,
        )

        # 5. Guardar JSON
        datos = {
            "ticker": ticker,
            "precio_entrada": precio_actual,
            "cantidad": cantidad,
            "prediccion_7d": round(precio_7d, 2),
            "tendencia": tendencia,
            "alerta_riesgo": posicion.alerta_riesgo,
        }

        with open("portafolio.json", "w") as f:
            json.dump(datos, f, indent=2)

        print("\nGuardado en portafolio.json")
    else:
        print("\nOperación cancelada.")

    print()


if __name__ == "__main__":
    main()