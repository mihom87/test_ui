
import pytest

import ext_allure as allure


def common_assert(description: str, expression, assert_message: str, soft: bool = True):
    if soft:
        with pytest.assume, allure.step(description):
            assert expression, assert_message
    else:
        with allure.step(description):
            assert expression, assert_message


