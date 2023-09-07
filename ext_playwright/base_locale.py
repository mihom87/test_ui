from utils.ext_enum import ExtendedEnum as Enum

class Translate:
    def __init__(self, default: None | str = None, **kwargs):
        self._lang_set = kwargs
        self.default = default or list(kwargs.keys())[0]

    def __getitem__(self, item):
        return self._lang_set.get(item, self._lang_set.get(self.default))


class BaseLocale(str, Enum):
    EN = 'en'
    RU = 'ru'