from time import sleep
import pytest
from ext_playwright.base_locale import BaseLocale
from playwright.sync_api import Page, expect
from tests.yandex_passport.pages.registration_page import RegistrationPage


#  @pytest.mark.parametrize('locale', ('en', 'ru'))
def test_first(page: Page,
               # locale,
               ):

    tab = RegistrationPage(page, locale=BaseLocale.EN)
    tab.goto('https://passport.yandex.ru/')
    tab.get_by_role('button', name=tab.elements_texts.login_button).click()
    # print(page.title())
    # page.click()
    # page.get_by_role('button', name=obj.login_button).click()
    # page.get_by_role('button', name="Войти").get_by_role().get_by_label()
    # page.get_by_test_id().get_by_test_id()
    # # print(tab.title())
    sleep(3)
    # a = tab.get_by_role('button', name="Войти")
    # a.click()
    # print(tab.url)
    # sleep(3)
    pass
