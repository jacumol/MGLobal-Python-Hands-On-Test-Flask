from flask_restful import Resource

from employeeapi.utils import EmployeeDataGetter
from employeeapi import employeeapi_api
from employeeapi.schemas import EmployeeSchema


class EmployeeList(Resource):
    @classmethod
    def get(cls):
        response = EmployeeDataGetter.get_api_data()
        if type(response) is dict:
            return response, 503
        employees = [EmployeeSchema.factory(t) for t in response]
        return employees, 200


class EmployeeDetail(Resource):
    @classmethod
    def get(cls, pk: int):
        response = EmployeeDataGetter.get_api_data()
        if type(response) is dict:
            return response, 503
        employees = [
            EmployeeSchema.factory(t) for t in response if t.get("id") == pk
        ]

        if len(employees) == 1:
            employee = employees[0]
        elif len(employees) == 0:
            return {"message": "Resource not found"}, 404
        else:
            return {"message": "Multiple objects Returned"}, 418
        return employee, 200


employeeapi_api.add_resource(EmployeeList, "/employees/")
employeeapi_api.add_resource(EmployeeDetail, "/employees/<int:pk>/")
