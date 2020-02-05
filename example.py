import logging
from flask_wrap import FlaskWrap


logging.basicConfig(level=logging.INFO)


class HelloWorldService(FlaskWrap):
    def endpoint_hello_world(self, name=None):
        logging.info("called endpoint_hello_world")
        return {"response": f"hello, {name}!"}


hello_world_service = HelloWorldService()
flask_app = hello_world_service.flask_app
if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8000)
