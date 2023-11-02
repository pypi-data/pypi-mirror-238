import functools
import json
from time import time

from google.cloud import logging


def method_logger(f, private_output: bool = False, exclude_inputs: list = None, exclude_outputs: list = None):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not exclude_inputs or f.__name__ not in exclude_inputs:
            print(f"Calling {f.__name__} with args: {args, kwargs}")
        t1 = time()
        result = f(*args, **kwargs)
        t2 = time()
        if not exclude_outputs or f.__name__ not in exclude_outputs:
            print(
                f"Function {f.__name__!r} executed in {(t2 - t1):.4f}s. Received "
                f"{f.__name__} result: {json.dumps(str(result)) if not private_output else '***MASKED***'}"
            )
        return result

    return wrapper


class BaseService:

    def __init__(
        self,
        log_name,
        private_output: bool = False,
        exclude_inputs: list = None,
        exclude_outputs: list = None
    ) -> None:
        self.private_output = private_output
        self.exclude_inputs = exclude_inputs
        self.exclude_outputs = exclude_outputs
        logging_client = logging.Client()
        self.logger = logging_client.logger(log_name)

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if type(value) not in [bool, type, str, int] and callable(value):
            decorator = method_logger
            return decorator(
                value,
                private_output=self.private_output,
                exclude_inputs=self.exclude_inputs,
                exclude_outputs=self.exclude_outputs
            )

        return value
