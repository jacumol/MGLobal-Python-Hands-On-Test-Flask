import abc
from collections import namedtuple

from marshmallow import Schema, fields


class BaseEmployeeSchema(Schema):
    __metaclass__ = abc.ABCMeta

    id = fields.Int()
    name = fields.Str()
    contractTypeName = fields.Str()
    roleId = fields.Int()
    roleName = fields.Str(required=True)
    roleDescription = fields.Str(required=True)
    hourlySalary = fields.Int()
    monthlySalary = fields.Int()

    anualSalary = fields.Method("get_anualSalary")

    @abc.abstractmethod
    def get_anualSalary(self, instance) -> int:
        """This method computes the anualsalary of the employee."""
        pass


class HourlyContractEmployeeSchema(BaseEmployeeSchema):
    def get_anualSalary(self, instance) -> int:
        return 120 * instance.hourlySalary * 12


class MontlyContractEmployeeSchema(BaseEmployeeSchema):
    def get_anualSalary(self, instance) -> int:
        return instance.monthlySalary * 12


class EmployeeSchema(object):
    @classmethod
    def factory(cls, data):
        """This method implements the Simple Factory Pattern to create the 
        respective object
        """
        employee = namedtuple("Employee", data.keys())(*data.values())

        if data.get("contractTypeName") == "HourlySalaryEmployee":
            schema = HourlyContractEmployeeSchema()
            print(employee)
            print(schema.dump(employee))
            return schema.dump(employee)
        elif data.get("contractTypeName") == "MonthlySalaryEmployee":
            schema = MontlyContractEmployeeSchema()
            print(schema.dump(employee))
            return schema.dump(employee)
        assert 0, "Bad Employee creation: " + data.get("contractTypeName")
