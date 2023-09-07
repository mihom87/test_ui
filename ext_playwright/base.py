import ext_allure as allure
# from .base_locator import BaseLocator


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

class BaseLocator(Base):

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __init__(self, locator):
        self.instance = locator

    @allure.step(f'Click on locator')
    def click(self, **kwargs):
        self.instance.click(**kwargs)