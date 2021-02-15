import pytest
import Alexa as ax

print("hellow")

@pytest.fixture
def alexa():
    alexa = ax.Alexa()
    return alexa


def test_startup(alexa):
    assert alexa.startUp() == "I'm listening say something"
