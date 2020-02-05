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
    '''
    Main class for creating API endpoints.

    Inherit from this class and create one or more methods whose
    names start with ``endpoint_``. It will create an endpoint
    with the same name as the method, with the ``endpoint_``
    prefix removed.

    For example, suppose the following class were in ``my_endpoint.py``:

    ```
        class MyEndpoint(FlaskWrap):
            def endpoint_foobar(self, thing=None):
                ...do something...
                return {'some': 'dictionary'}

        my_endpoint = MyEndpoint()
        flask_app = my_endpoint.flask_app
    ```

    Then we would have an endpoint called ``foobar`` which accepts
    the ``GET`` parameter ``thing`` (because ``thing`` is a kwarg in
    the signature of ``endpoint_foobar``).

    The API can be started by running ``gunicorn`` like so:

    ```
        gunicorn my_endpoint:flask_app -b 0.0.0.0
    ```

    When this is done, you could call the endpoint by using ``curl``:

    ```
        curl http://localhost:8000/my_endpoint?thing=whatever
    ```

    The ``gunicorn`` command is in the script ``start_service.sh``.

    The class uses introspection to find the names of all
    methods which start with ``endpoint_``. For each such
    method, we invoke ``functools.partial`` on the
    ``_endpoint_partial`` to create a new method at runtime
    which is assigned a route by Flask.
    '''

    def __init__(self):
        self.service_class_name = self.__class__.__name__
        self.flask_app = app.Flask(self.service_class_name)


        for attr in dir(self):
            obj = getattr(self, attr)
            if attr.startswith(ENDPOINT_PREFIX) and isinstance(
                obj, (types.MethodType,)
            ):
                logging.info(f"Found endpoint method: {attr}")
                endpoint_name = attr.replace("endpoint_", "")
                logging.info(f"Creating endpoint: {endpoint_name}")
                partial_endpoint_function = functools.partial(
                    self._endpoint_partial, endpoint_function=obj
                )
                self.flask_app.add_url_rule(
                    f"/{endpoint_name}",
                    endpoint_name,
                    partial_endpoint_function,
                )

    def _endpoint_partial(self, endpoint_function=None):
        '''
        This is the partial function that is a template for
        any methods that are assigned routes by Flask at
        runtime.
        '''
        assert endpoint_function is not None, "_endpoint_partial was called without an endpoint_function."
        logging.info("Called endpoint_partial")
        logging.info(f"Request arguments: {str(request.args)}")
        return endpoint_function(**request.args)
