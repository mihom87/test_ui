import ext_allure as allure
from .base import Base


class BasePage(Base):

    def __repr__(self):
        return 'BasePage'

    @allure.step('Navigate to page {url}')
    def goto(self, url, **kwargs):
        return self.instance.goto(url, **kwargs)

    @allure.step('Click on page')
    def click(self, selector, **kwargs):
        self.instance.click(selector, **kwargs)
