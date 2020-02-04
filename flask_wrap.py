"""
This is a class that helps us standardize our Flask APIs.
"""

import logging
import types
from flask import app, request
import functools

logging.basicConfig(level=logging.INFO)

ENDPOINT_PREFIX = "endpoint_"


class FlaskWrap:
    def __init__(self):
        self.service_class_name = self.__class__.__name__
        self.flask_app = app.Flask(self.service_class_name)

        # Find methods for endpoints
        for attr in dir(self):
            obj = getattr(self, attr)
            if attr.startswith(ENDPOINT_PREFIX) and isinstance(
                obj, (types.MethodType,)
            ):
                logging.info(f"Found endpoint method: {attr}")
                endpoint_name = attr.replace("endpoint_", "")
                logging.info(f"Creating endpoint: {endpoint_name}")
                partial_endpoint_function = functools.partial(
                    self.endpoint_partial, endpoint_function=obj
                )
                self.flask_app.add_url_rule(
                    f"/{endpoint_name}",
                    endpoint_name,
                    partial_endpoint_function,
                )

    def endpoint_partial(self, endpoint_function=None):
        logging.info("Called endpoint_partial")
        logging.info(f"Request arguments: {str(request.args)}")
        return endpoint_function(**request.args)
