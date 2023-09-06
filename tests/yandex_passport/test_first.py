from time import sleep
import pytest
from ext_playwright.base_page import RegistrationPage, BasePage
from playwright.sync_api import Page, expect


@pytest.mark.parametrize('locale', ('en', 'ru'))
def test_first(page: Page, locale):

    tab = RegistrationPage(page, locale='en')
    Elements.LOGIN_BUTTON.get(locale)
    tab.goto('https://passport.yandex.ru/')
    tab.get_by_role('button', name=tab.login_button).click()
    # print(page.title())
    # page.click()
    # page.get_by_role('button', name=obj.login_button).click()
    # page.get_by_role('button', name="Войти").get_by_role().get_by_label()
    # page.get_by_test_id().get_by_test_id()
    # # print(tab.title())
    # sleep(3)
    # a = tab.get_by_role('button', name="Войти")
    # a.click()
    # print(tab.url)
    # sleep(3)
    pass
