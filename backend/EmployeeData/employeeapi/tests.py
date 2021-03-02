import unittest
from unittest.mock import patch, MagicMock

import requests

from employeeapi.schemas import (
    EmployeeSchema,
    HourlyContractEmployeeSchema,
    MontlyContractEmployeeSchema,
)
from app import create_app


class TestEmployeeSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.hourly_employee_dict = {
            "id": 1,
            "name": "Sub1",
            "contractTypeName": "HourlySalaryEmployee",
            "roleId": 1,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }
        self.monthly_employee_dict = {
            "id": 1,
            "name": "Sub2",
            "contractTypeName": "MonthlySalaryEmployee",
            "roleId": 1,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }

    def test_check_class_factory(self):
        employee_obj = EmployeeSchema.factory(self.hourly_employee_dict)
        self.assertIsInstance(employee_obj, dict)

        employee_obj = EmployeeSchema.factory(self.monthly_employee_dict)
        self.assertIsInstance(employee_obj, dict)

    def test_anual_salary_computation(self):
        employee_obj = EmployeeSchema.factory(self.hourly_employee_dict)
        salary = self.hourly_employee_dict["hourlySalary"] * 120 * 12
        self.assertEqual(employee_obj["anualSalary"], salary)

        employee_obj = EmployeeSchema.factory(self.monthly_employee_dict)
        salary = self.hourly_employee_dict["monthlySalary"] * 12
        self.assertEqual(employee_obj["anualSalary"], salary)


class TestEmployeeList(unittest.TestCase):
    def setUp(self) -> None:
        self.hourly_employee_dict = {
            "id": 1,
            "name": "Sub1",
            "contractTypeName": "HourlySalaryEmployee",
            "roleId": 1,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }
        self.monthly_employee_dict = {
            "id": 2,
            "name": "Sub2",
            "contractTypeName": "MonthlySalaryEmployee",
            "roleId": 2,
            "roleName": "Administrator",
            "roleDescription": None,
            "hourlySalary": 10000.0,
            "monthlySalary": 10000.0,
        }

        self.app = create_app()
        self.client = self.app.test_client()
    
    @patch("employeeapi.utils.EmployeeDataGetter.get_api_data")
    def test_employee_list(self, get_api_data):
        data = [self.hourly_employee_dict, self.monthly_employee_dict]
        get_api_data.return_value = data
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 2)
    
    @patch("employeeapi.utils.EmployeeDataGetter.get_api_data")
    def test_employee_detail(self, get_api_data):
        data = [self.hourly_employee_dict, self.monthly_employee_dict]
        get_api_data.return_value = data
        response = self.client.get('/api/employees/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertEqual(self.hourly_employee_dict["name"], response.json["name"])

    @patch("employeeapi.utils.EmployeeDataGetter.get_api_data")
    def test_unknown_employee_detail(self, get_api_data):
        data = [self.hourly_employee_dict, self.monthly_employee_dict]
        get_api_data.return_value = data
        response = self.client.get('/api/employees/3/')
        self.assertEqual(response.status_code, 404)

    @patch("requests.get")
    def test_bad_timeout_response_employee_list(self, get):
        get.side_effect = requests.exceptions.Timeout
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json["message"], "Timeout error")

    @patch("requests.get")
    def test_bad_too_many_redirect_response_employee_list(self, get):
        get.side_effect = requests.exceptions.TooManyRedirects
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json["message"], "Too many redirects error")

    @patch("requests.get")
    def test_bad_unknown_response_employee_list(self, get):
        get.side_effect = ZeroDivisionError
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json["message"], "Unknown error")
    



if __name__ == "__main__":
    unittest.main()
