"""
Helpful fixtures for testing
"""

from flask import Flask
from flask_restful import Api

from pytest import fixture

from config import TestingConfig

# from routes import setup_routes


@fixture(scope="module")
def demo_app():
    """
    Setup the flask app context I hope
    """
    app = Flask(__name__)

    app.config.from_object(TestingConfig)
    app.testing = True


    api = Api(app)

    # setup_routes(api)

    return app
