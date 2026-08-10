"""Gestor de colección de posiciones."""

from src.modelos import Posicion


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
        self._posiciones.remove(posicion)

    def cantidad_posiciones(self) -> int:
        """Devuelve el número de posiciones del portafolio."""
        return len(self._posiciones)