import os

from flask import Flask

from public import public_bp
from employeeapi import employeeapi_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["ENV"] = "development"

    # Blueprints registers
    app.register_blueprint(public_bp)
    app.register_blueprint(employeeapi_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
