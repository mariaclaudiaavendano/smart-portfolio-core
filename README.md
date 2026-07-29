# SmartPortfolio Core 🚀

Core bancario (backend) para la gestión de portafolios de inversión.
Reemplaza el control manual en Excel por un sistema **tipado, validado e inmutable**
que impide errores humanos de copiar/pegar.

---

## 👥 Equipo

| Nombre | Rol | Usuario GitHub | Responsabilidad |
|---|---|---|---|
| _Maria Claudia Avendaño_ | 🏗️ Arquitecto / Repository Owner | `@mariaclaudiaavendano` | Repo, protección de `main`, estructura, code review y merges |
| _(nombre 2)_ | 💻 Developer 1 | `@usuario2` | `src/modelos.py` — `Instrumento` y `Posicion` |
| _(nombre 3)_ | 💻 Developer 2 | `@usuario3` | `src/portafolio.py` y `src/reportes.py` |

> ⚠️ Reemplacen los nombres y usuarios reales antes de entregar el link.

---

## 📁 Estructura del proyecto

```
smart-portfolio/
├── src/
│   ├── __init__.py
│   ├── modelos.py       # Dominio: Instrumento (frozen) y Posicion (validada)
│   ├── portafolio.py    # Colección: gestión de posiciones
│   └── reportes.py      # Presentación: ReportadorFinanciero (SRP)
├── .gitignore
├── README.md
└── main.py              # Script de prueba de integración
```

## 🧱 Decisiones de arquitectura

- **`Instrumento` es `@dataclass(frozen=True)`**: un instrumento financiero (AAPL, US10Y) es un
  hecho del mercado, no un estado mutable. Congelarlo evita que alguien le cambie el ticker por accidente.
- **`Posicion` valida con `@property`**: la cantidad nunca puede ser negativa. La validación vive
  en el modelo, no en el código que lo usa.
- **`ReportadorFinanciero` no guarda estado (SRP)**: solo recibe un `Portafolio` y produce salidas.
  Si mañana queremos exportar a CSV o JSON, agregamos un método sin tocar el dominio (OCP).
- **Type hints obligatorios** en todas las funciones y métodos públicos.

## ▶️ Cómo ejecutar

Requiere Python 3.10 o superior.

```bash
git clone https://github.com/<usuario-arquitecto>/smart-portfolio-core.git
cd smart-portfolio-core
python main.py
```

## 🔁 Flujo de trabajo (Git Flow)

1. `main` está protegida: no se hace push directo, no se puede borrar.
2. Cada feature vive en su propia rama:
   - `feat/modelos` → Developer 1
   - `feat/logica` → Developer 2
3. Se abre un **Pull Request** hacia `main`.
4. Mínimo **1 comentario de code review** por PR antes de aprobar.
5. El Arquitecto hace el **merge**.

### Convención de commits

```
feat: agrega dataclass Instrumento
fix: corrige validacion de cantidad negativa
docs: actualiza README con integrantes
```
