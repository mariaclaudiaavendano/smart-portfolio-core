"""Gestor de colección de posiciones."""

from src.modelos import Posicion


class PosicionNoExisteError(Exception):
    """Se lanza cuando se opera sobre una posición que no existe."""
    pass


class Portafolio:
    """Gestiona una colección de posiciones financieras."""

    def __init__(self) -> None:
        """Inicializa un portafolio vacío."""
        self._posiciones: list[Posicion] = []

    @property
    def posiciones(self) -> list[Posicion]:
        """Devuelve las posiciones del portafolio."""
        return self._posiciones.copy()

    def agregar_posicion(self, posicion: Posicion) -> None:
        """Agrega una posición al portafolio."""
        self._posiciones.append(posicion)

    def eliminar_posicion(self, posicion: Posicion) -> None:
        """Elimina una posición del portafolio."""
        if posicion not in self._posiciones:
            raise PosicionNoExisteError(
                f"La posición no existe en el portafolio."
            )
        self._posiciones.remove(posicion)

    def remover_posicion(self, ticker: str) -> None:
        """Elimina una posición por ticker."""
        for posicion in self._posiciones:
            if posicion.instrumento.ticker == ticker:
                self._posiciones.remove(posicion)
                return
        raise PosicionNoExisteError(
            f"No existe posición para el ticker '{ticker}'."
        )

    def cantidad_posiciones(self) -> int:
        """Devuelve el número de posiciones del portafolio."""
        return len(self._posiciones)