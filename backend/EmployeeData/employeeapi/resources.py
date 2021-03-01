from flask import request
from flask_restful import Resource
import requests

from employeeapi.utils import EmployeeDataGetter
from employeeapi import employeeapi_api
from employeeapi.schemas import EmployeeSchema


class EmployeeList(Resource):
    @classmethod
    def get(cls):
        response = EmployeeDataGetter.get_api_data()
        response = EmployeeDataGetter.get_api_data()
        if type(response) is dict:
            return response, 503
        employees = [EmployeeSchema.factory(t) for t in response]
        return employees, 200


class EmployeeDetail(Resource):
    pass


employeeapi_api.add_resource(EmployeeList, "/employees/")
