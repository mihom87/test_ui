from pylenium.driver import Pylenium


def test_first(py: Pylenium):
    py.visit('https://passport.yandex.ru/')
    pass
