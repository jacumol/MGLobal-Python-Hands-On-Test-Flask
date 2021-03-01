from flask import Blueprint
from flask_restful import Api


employeeapi_bp = Blueprint(
    "employeeapi", __name__, template_folder="templates"
)
employeeapi_api = Api(employeeapi_bp)

from . import resources
