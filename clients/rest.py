from json import JSONDecodeError
from pprint import pformat

import curlify2
from requests import Session

import ext_allure as allure


class ClientRest:
    def __init__(self, base_url, default_headers=None, default_cookies=None, verify=False, default_cert=None):
        self.base_url = base_url
        self._session = Session()
        self._session.headers.update(default_headers or {})
        self._session.cookies.update(default_cookies or {})
        self._session.verify = verify
        self._session.cert = default_cert

    def request(
            self,
            method,
            url,
            params=None,
            headers=None,
            cookies=None,
            files=None,
            json=None,
            data=None,
            response_code=None,
            allow_redirects=True,
            cert=None,
            verify=None,
            timeout=None,
    ):
        try:
            response = self._session.request(
                method=method,
                url=f'{self.base_url}{url}',
                headers=headers,
                params=params,
                cookies=cookies,
                json=json,
                data=data,
                files=files,
                allow_redirects=allow_redirects,
                cert=cert,
                verify=verify,
                timeout=timeout,
            )
        except Exception as e:
            allure.attach(body=f'Request details: \n\n'
                               f'Method: {method} \n\n'
                               f'url: {self.base_url}{url} \n\n'
                               f'allow redirects: {allow_redirects}\n\n'
                               f'Headers: \n {headers} \n\n'
                               f'Params: \n {params} \n\n'
                               f'Cookies: \n {cookies} \n\n'
                               f'json: \n {json} \n\n'
                               f'data: \n {data} \n\n'
                               f'files: \n {files}  \n\n'
                               f'cert: \n {cert} \n\n'
                               f'verify: {verify} \n\n'
                               f'timeout: {timeout} \n\n',
                          name=f'Failed request: {method} {self.base_url}{url}',
                          attachment_type=allure.attachment_type.TEXT,
                          )
            raise e

        self.enrich_allure(response)

        if response_code:
            self.validate_response_code(response_code, response)
        return response

    @staticmethod
    def validate_response_code(expected_code, response):
        if expected_code != response.status_code:
            allure.attach(
                body=f'Expected Response Code: {expected_code}\n\n' f'Actual Response Code: {response.status_code}\n\n',
                name=f'Failed: unexpected response code ({response.status_code}!={expected_code})',
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.status_code == expected_code, f'Unexpected Response Code: {response.status_code}'

    @staticmethod
    def enrich_allure(response):
        indent = 4

        if response.history:
            list_of_responses = [response for response in response.history]
            list_of_responses.append(response)
            for response in list_of_responses:
                request_body = pformat(response.request.body)
                try:
                    response_body = pformat(response.json(), indent=indent)
                except (JSONDecodeError, TypeError):
                    response_body = pformat(response.text, indent=indent)
                with allure.step(f'{response}'):
                    allure.attach(
                        body=f'Request:\n{response.request.method} {response.request.url}\n\n'
                             f'Request Headers:\n{pformat(dict(response.request.headers), indent=indent)}\n\n'
                             f'Request Cookies:\n{pformat(response.request._cookies.get_dict(), indent=indent)}\n\n'
                             f'Request Body:\n{request_body}\n\n'
                             f'{curlify2.to_curl(response.request)}',
                        name=f'{response.request.method} {response.request.url}',
                        attachment_type=allure.attachment_type.TEXT,
                    )
                    allure.attach(
                        body=f'Response Code:\n {response.status_code} {response.reason}\n\n'
                             f'Response Headers:\n{pformat(dict(response.headers), indent=indent)}\n\n'
                             f'Response Cookies:\n{pformat(response.cookies.get_dict(), indent=indent)}\n\n'
                             f'Response Body:\n{response_body}\n\n',
                        name=f'Response {response.status_code} {response.reason}',
                        attachment_type=allure.attachment_type.TEXT,
                    )
        else:
            request_body = pformat(response.request.body, indent=indent)

            try:
                response_body = pformat(response.json(), indent=indent)
            except (JSONDecodeError, TypeError, UnicodeDecodeError):
                response_body = pformat(response.text, indent=indent)

            try:
                to_curl = curlify2.to_curl(response.request)
            except UnicodeDecodeError:
                to_curl = ''

            allure.attach(
                body=f'Request:\n{response.request.method} {response.request.url}\n\n'
                     f'Request Headers:\n{pformat(dict(response.request.headers), indent=indent)}\n\n'
                     f'Request Cookies:\n{pformat(response.request._cookies.get_dict(), indent=indent)}\n\n'
                     f'Request Body:\n{request_body}\n\n'
                     f'{to_curl}',
                name=f'{response.request.method} {response.request.url}',
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                body=f'Response Code:\n {response.status_code} {response.reason}\n\n'
                     f'Response Headers:\n{pformat(dict(response.headers), indent=indent)}\n\n'
                     f'Response Cookies:\n{pformat(response.cookies.get_dict(), indent=indent)}\n\n'
                     f'Response Body:\n{response_body}\n\n',
                name=f'Response {response.status_code} {response.reason}',
                attachment_type=allure.attachment_type.TEXT,
            )
