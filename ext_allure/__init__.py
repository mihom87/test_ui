import pprint
from datetime import datetime
from functools import wraps

from allure import (
    attach,
    attachment_type,
    description,
    description_html,
    epic,
    feature,
    id,
    issue,
    link,
    parent_suite,
    severity,
    dynamic,
    story,
    sub_suite,
    suite,
    tag,
    testcase,
    title,
    label
)
from allure import step as origin_step
from allure_commons._allure import StepContext
from allure_commons.utils import func_parameters, represent


def step(title_):
    if callable(title_):
        return CustomStepContext(title_.__name__, {})(title_)
    else:
        return CustomStepContext(title_, {})


class CustomStepContext(StepContext):
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is AssertionError:
            exc_val.error_to_description = f'\n\nFail to perform step: {self.title}'
        super().__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, func):
        @wraps(func)
        def impl(*args, **kwargs):
            __tracebackhide__ = True
            f_args = list(map(lambda x: represent(x), args))
            f_params = func_parameters(func, *args, **kwargs)

            with CustomStepContext(self.title.format(*f_args, **f_params), f_params):
                result = func(*args, **kwargs)
                return result

        return impl


