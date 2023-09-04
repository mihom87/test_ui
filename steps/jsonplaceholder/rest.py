from clients import ClientRest
from dynaconf import settings
import ext_allure as allure

_client_api = ClientRest(base_url=settings.YANDEX_PASSPORT)


@allure.step('[JSON_PLACEHOLDER]Get users')
def get_users(response_code: int):
    return _client_api.request(method='POST', url='/users', response_code=response_code).json()
