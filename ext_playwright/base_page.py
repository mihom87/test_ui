from playwright.sync_api import Page, Locator
import ext_allure as allure
from enum import Enum
from typing import Optional


class Base:
    def __repr__(self):
        return 'Base'

    instance = None

    def __getattr__(self, name):
        return getattr(self.instance, name)

    @allure.step('Get locator by role {role}')
    def get_by_role(self, role, **kwargs):
        return BaseLocator(self.instance.get_by_role(role, **kwargs))

    @allure.step('Get locator by text "{text}"')
    def get_by_text(self, text, **kwargs):
        return BaseLocator(self.instance.get_by_text(text, **kwargs))

    @allure.step('Get locator by label "{text}"')
    def get_by_label(self, text, **kwargs):
        return BaseLocator(self.instance.get_by_label(text, **kwargs))

    @allure.step('Get locator by placeholder "{text}"')
    def get_by_placeholder(self, text, **kwargs):
        return BaseLocator(self.instance.get_by_placeholder(text, **kwargs))

    @allure.step('Get locator by alt text "{text}"')
    def get_by_alt_text(self, text, **kwargs):
        return BaseLocator(self.instance.get_by_alt_text(text, **kwargs))

    @allure.step('Get locator by title "{text}"')
    def get_by_title(self, text, **kwargs):
        return BaseLocator(self.instance.get_by_title(text, **kwargs))

    @allure.step('Get locator by test_id "{test_id}"')
    def get_by_test_id(self, test_id):
        return BaseLocator(self.instance.get_by_test_id(test_id))


class BasePage(# Page,
               Base):
    instance = None

    def __repr__(self):
        return 'BasePage'

    @allure.step('Navigate to page {url}')
    def goto(self, url, **kwargs):
        return self.instance.goto(url, **kwargs)

    @allure.step('Click on page')
    def click(self, selector, **kwargs):
        self.instance.click(selector, **kwargs)


class BaseLocator(# Locator,
                  Base):
    locator = None

    def __repr__(self):
        return 'BaseLocator'

    def __getattr__(self, name):
        return getattr(self.locator, name)

    def __init__(self, locator):
        self.instance = locator

    @allure.step(f'Click on locator')
    def click(self, **kwargs):
        self.instance.click(**kwargs)


elements = {'en': {'login_button': 'Login'





                   },
            'ru': {'login_button': 'Войти'}

            }


class DefaultElements(Enum):
    LOGIN_BUTTON = 'Login'
    PASSWORD_FIELD_HOVER = None


class LocaleClass(Enum, DefaultElements):
    pass


class Locale(Enum):
    EN = LocaleClass().as_dict()

    RU = LocaleClass(PASSWORD_FIELD_HOVER='пароль').as_dict()

class RegistrationPage(BasePage):
    # def __repr__(self):
    #     return 'RegistrationPage'


    def __init__(self, page, locale='En'):
        self.instance = page
        for attrib in Color()[locale].__dict__():
            self.__setattr__(attrib)


    LOGIN_BUTTON = 'логин'

    def _setup_locale(self, locale):




