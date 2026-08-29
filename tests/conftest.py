import pytest

from src.modelos import Instrumento
from src.portafolio import Portafolio


@pytest.fixture
def instrumento_test():
    return Instrumento(ticker="TSLA", tipo="Acción", sector="Tecnología")


@pytest.fixture
def portafolio_vacio():
    return Portafolio()