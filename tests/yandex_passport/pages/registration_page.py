from ext_playwright.base_page import BasePage
from utils.base_data_factory import DataClass
from ext_playwright.base_locale import BaseLocale, Translate
from typing import Optional
from pydantic import Field


class ElementsTexts:
    login_button = Translate(ru='Войти', en='Log in')
    login_button_hint = Translate(en='Press button to login', ru='Vhodite')

    def __init__(self, lang: str):
        self._lang = lang
        a = ElementsTexts.__dict__.items()
        print(a)
        self._translations = {
            key: value[self._lang] for key, value in ElementsTexts.__dict__.items() if isinstance(value, Translate)
        }
        for key, value in self._translations.items():
            setattr(self, key, value)
        print(lang)


    # def __getattribute__(self, item):
    #     if item in self._translations.keys():
    #         return self._translations[item]
    #     return self.item



class RegistrationPage(BasePage):

    def __init__(self, page, locale: str):
        self.instance = page
        self.elements_texts = ElementsTexts(lang=locale)






