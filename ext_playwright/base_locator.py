import ext_allure as allure
from .base import Base


class BaseLocator(Base):

    def __repr__(self):
        return 'BaseLocator'

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __init__(self, locator):
        self.instance = locator

    @allure.step(f'Click on locator')
    def click(self, **kwargs):
        self.instance.click(**kwargs)