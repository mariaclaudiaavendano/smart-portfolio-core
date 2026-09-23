# SmartPortfolio Core 🚀

Este proyecto fue desarrollado como parte del Seminario de Programación de la Maestría. La idea principal es reemplazar el típico Excel donde uno anota sus inversiones por un sistema en Python que valida los datos automáticamente y hasta predice precios usando Machine Learning.

---

## 👥 Quiénes somos

| Nombre | Rol | GitHub | Qué hice |
|---|---|---|---|
| Maria Claudia Avendaño | 🏗️ Arquitecta | `@mariaclaudiaavendano` | Organicé el repo, revisé el código de mis compañeras y aprobé los cambios |
| Karen Sofia Galindo | 💻 Developer 1 | `@karengalindob12` | Programó los modelos base: `Instrumento` y `Posicion` |
| Beatriz Elena Pertuz | 💻 Developer 2 | `@Beatriz-23-dev` | Programó el portafolio, los reportes y los tests |

---

## 📁 Cómo está organizado el proyecto

```
smart-portfolio-core/
├── src/
│   ├── modelos.py                  # Las clases base: Instrumento y Posicion
│   ├── portafolio.py               # Maneja la colección de posiciones
│   ├── reportes.py                 # Genera resúmenes del portafolio
│   ├── providers.py                # Se conecta a Yahoo Finance para traer precios reales
│   └── instrumento_inteligente.py  # El instrumento que predice precios con ML
├── tests/
│   ├── conftest.py                 # Datos de prueba reutilizables (fixtures)
│   └── test_models.py              # Todas las pruebas automatizadas
├── main.py                         # Prueba básica de integración
└── main_oraculo.py                 # La aplicación principal: el Oráculo Financiero
```

---

## 🧱 Por qué tomamos estas decisiones técnicas

Cuando empezamos a diseñar el sistema, nos preguntamos: ¿cómo evitamos que alguien cometa errores al usar nuestro código? Estas fueron nuestras soluciones:

**`Instrumento` es inmutable (`frozen=True`)**
Un instrumento financiero como AAPL o TSLA es un hecho del mercado — no debería cambiar. Por eso lo hicimos inmutable: si alguien intenta cambiar el ticker por error, Python lanza una excepción automáticamente.

**`Posicion` valida con `@property`**
Una posición no puede tener cantidad negativa (¿cómo tendrías -5 acciones?). La validación vive dentro del objeto, no en el código que lo usa. Así no importa desde dónde se use, siempre va a validar.

**`ReportadorFinanciero` tiene una sola responsabilidad**
Solo sabe generar reportes. No guarda datos, no hace cálculos de inversión. Esto es el principio SRP (Single Responsibility Principle) que aprendimos en clase.

**`Instrumento` recibe el proveedor de datos por fuera (inyección de dependencias)**
En producción le pasamos `YahooFinanceClient` que trae datos reales de internet. En los tests le pasamos `MockDataProvider` con datos inventados para no depender de internet. Esto hace el código más fácil de probar.

---

## 🔮 El Oráculo Financiero — nuestra aplicación con Machine Learning

Esta fue la parte más interesante del proyecto. Construimos una aplicación de consola que predice si una acción va a subir o bajar.

### Cómo correrlo

```bash
export PYTHONPATH=$PWD
poetry run python main_oraculo.py
```

### Cómo se ve cuando corre

```
--- 🔮 SMART PORTFOLIO ORACLE ---

Ingrese Ticker: AAPL

Obteniendo datos... OK
Entrenando modelo... 🤖 Modelo entrenado para AAPL
OK

📊 AAPL
Precio actual: $338.98
Predicción 7 días: $319.27 (BAJISTA 📉)

¿Comprar? (s/n): s
Cantidad: 3

Guardado en portafolio.json ✅
```

### ¿Qué pasa cuando dice "Entrenando modelo"?

Esto fue lo que más nos costó entender al principio, así que lo explicamos paso a paso:

**Paso 1 — Baja el historial de precios**
El sistema se conecta a Yahoo Finance y descarga los precios de cierre de los últimos 12 meses para la acción que ingresamos. Para AAPL son aproximadamente 252 días de precios reales.

**Paso 2 — Aprende la tendencia**
Con esos 252 precios, entrena una **regresión lineal**. Básicamente dibuja la línea recta que mejor describe hacia dónde han ido los precios:

```
Precio
  │                 *  *
  │           *           ← esta es la línea de tendencia
  │      *
  │
  └────────────────────→ Tiempo (días)
```

**Paso 3 — Predice el futuro**
Una vez que tiene esa línea, la extiende 7 días hacia adelante y calcula el precio estimado. Si ese precio es mayor al actual → **ALCISTA 📈**. Si es menor → **BAJISTA 📉**.

**Paso 4 — Guarda la decisión**
Si decides comprar, guarda todo en un archivo `portafolio.json` con el ticker, precio, cantidad y predicción.

> ⚠️ **Ojo:** Esta predicción es un ejercicio académico. Una línea recta no captura toda la complejidad de los mercados reales. El objetivo del taller no era hacer predicciones perfectas, sino aprender a integrar Machine Learning dentro de objetos de dominio — lo que el profesor llama **Domain-Driven Data Science**.

---

## 🧪 Las pruebas que hicimos

Corremos los tests con este comando:

```bash
export PYTHONPATH=$PWD
poetry run pytest tests/ -v --cov=src.modelos --cov-report=term-missing
```

Logramos **95% de cobertura** en el módulo de modelos ✅

Para cumplir con lo que pedía el taller usamos:

- **`pytest.fixture`** — para no repetir la creación de objetos en cada test
- **`@pytest.mark.parametrize`** — para probar ganancia/pérdida con varios escenarios en un solo test
- **`pytest.approx`** — para comparar números decimales sin errores de punto flotante
- **`pytest.raises`** — para verificar que el sistema lanza errores cuando debe

---

## ⚙️ Cómo instalar el proyecto

Necesitas Python 3.10 o superior.

```bash
git clone https://github.com/mariaclaudiaavendano/smart-portfolio-core.git
cd smart-portfolio-core
poetry install
poetry add scikit-learn yfinance
poetry add pytest pytest-cov --group dev
```

---

## 🔁 Cómo trabajamos en equipo (Git Flow)

Desde el principio acordamos unas reglas para no pisarnos entre nosotras:

1. **Nadie hace push directo a `main`** — está protegida en GitHub
2. Cada una trabaja en su propia rama:
   - `feat/modelos` → Karen
   - `feat/logica` → Beatriz
   - `feat/test-suite` → Tests y cobertura
   - `feat/ml-providers` → Providers y CLI del oráculo
   - `feat/instrumento-inteligente` → ML encapsulado
3. Cuando termina, abre un **Pull Request**
4. Otra compañera revisa y deja al menos un comentario
5. La Arquitecta aprueba y hace el **merge**

### Cómo escribimos los commits

```
feat: añadir clase Instrumento con dataclass frozen
fix: corregir validación de cantidad negativa
test: añadir tests parametrizados de PnL
docs: complementar README con explicación del oráculo
chore: elevar cobertura de modelos al 95%
```