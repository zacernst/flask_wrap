# flask_wrap
This is a wrapper for Flask.

The purpose of this is to standardize how we build and deploy APIs that use Flask.

To use this class, do the following:

1. Write a class that inherits from ``FlaskWrap``.
2. Inside that class, create a method whose name starts with ``endpoint_``.
3. Instantiate your class, e.g. ``my_service = MyService()``
4. Add a line of code: ``flask_app = my_service.flask_app`` at the end.
5. Run ``gunicorn`` to start the server: ``gunicorn my_service:flask_app``
6. Send a request to your new service: ``curl http://127.0.0.1/my_service``

There is an example in the ``example.py`` file. You can start it by:

```
gunicorn example:flask_app
```

It takes a parameter called ``name`` and says "hello":

```
curl http://127.0.0.1:8000/hello_world?name=bob
```

It will respond with:

```
{"response":"hello, bob!"}
```

The rationale for this class is that we can put any logging, monitoring, testing, into the
``FlaskWrap`` class (specifically, in the ``endpoint_partial`` function) and it will
automatically be inherited by any services we create. This also allows people to create
useful APIs without having to understand Flask or anything else relating to the mechanics
of APIs. They only need to write a class that inherits fro ``FlaskWrap`` and then they can
create as many endpoints as they like, simply by writing methods whose names start with
the string ``endpoint_``. ``FlaskWrap`` will take care of the rest.
