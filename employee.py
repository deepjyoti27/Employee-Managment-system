from abc import ABC, abstractmethod
from typing import Dict, Any

class Employee(ABC):
    """
    Abstract Base Class representing a generic Employee.
    Demonstrates Abstraction and Encapsulation.
    """
    def __init__(self, employee_id: str, name: str, department: str):
        self.employee_id = employee_id  # Uses property setter for validation
        self.name = name
        self.department = department

    @property
    def employee_id(self) -> str:
        return self.__employee_id

    @employee_id.setter
    def employee_id(self, value: str):
        if not value.strip():
            raise ValueError("Employee ID cannot be empty.")
        self.__employee_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Employee Name cannot be empty.")
        self.__name = value

    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value: str):
        if not value.strip():
            raise ValueError("Department cannot be empty.")
        self.__department = value

    @abstractmethod
    def calculate_salary(self) -> float:
        """Abstract method to calculate monthly salary."""
        pass

    def display_details(self) -> str:
        """Returns string representation of employee details."""
        return f"ID: {self.employee_id:<5} | Name: {self.name:<15} | Dept: {self.department:<10}"

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert employee object to dictionary for JSON serialization."""
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """
        Factory method to reconstruct correct subclass from dictionary.
        Demonstrates polymorphism and factory pattern.
        """
        emp_type = data.get("type", "").lower()
        if emp_type == "fulltimeemployee":
            return FullTimeEmployee(
                employee_id=data["id"],
                name=data["name"],
                department=data["department"],
                monthly_salary=data["monthly_salary"]
            )
        elif emp_type == "parttimeemployee":
            return PartTimeEmployee(
                employee_id=data["id"],
                name=data["name"],
                department=data["department"],
                hourly_rate=data["hourly_rate"],
                hours_worked_per_month=data["hours_worked_per_month"]
            )
        elif emp_type == "manager":
            return Manager(
                employee_id=data["id"],
                name=data["name"],
                department=data["department"],
                monthly_salary=data["monthly_salary"],
                bonus=data["bonus"]
            )
        else:
            raise ValueError(f"Unknown employee type: {emp_type}")


class FullTimeEmployee(Employee):
    """
    Inherits from Employee. Represents an employee with a fixed monthly salary.
    """
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float):
        super().__init__(employee_id, name, department)
        self.monthly_salary = monthly_salary  # Uses property setter

    @property
    def monthly_salary(self) -> float:
        return self.__monthly_salary

    @monthly_salary.setter
    def monthly_salary(self, value: float):
        if value < 0:
            raise ValueError("Salary cannot be negative.")
        self.__monthly_salary = value

    def calculate_salary(self) -> float:
        """Overrides abstract method."""
        return self.monthly_salary

    def display_details(self) -> str:
        base_details = super().display_details()
        return f"{base_details} | Type: Full-Time | Salary: ${self.calculate_salary():,.2f}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "fulltimeemployee",
            "id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "monthly_salary": self.monthly_salary
        }


class PartTimeEmployee(Employee):
    """
    Inherits from Employee. Represents an employee paid by the hour.
    """
    def __init__(self, employee_id: str, name: str, department: str, hourly_rate: float, hours_worked_per_month: float):
        super().__init__(employee_id, name, department)
        self.hourly_rate = hourly_rate
        self.hours_worked_per_month = hours_worked_per_month

    @property
    def hourly_rate(self) -> float:
        return self.__hourly_rate

    @hourly_rate.setter
    def hourly_rate(self, value: float):
        if value < 0:
            raise ValueError("Hourly rate cannot be negative.")
        self.__hourly_rate = value

    @property
    def hours_worked_per_month(self) -> float:
        return self.__hours_worked_per_month

    @hours_worked_per_month.setter
    def hours_worked_per_month(self, value: float):
        if value < 0:
            raise ValueError("Hours worked cannot be negative.")
        self.__hours_worked_per_month = value

    def calculate_salary(self) -> float:
        """Overrides abstract method."""
        return self.hourly_rate * self.hours_worked_per_month

    def display_details(self) -> str:
        base_details = super().display_details()
        return f"{base_details} | Type: Part-Time | Salary: ${self.calculate_salary():,.2f}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "parttimeemployee",
            "id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "hourly_rate": self.hourly_rate,
            "hours_worked_per_month": self.hours_worked_per_month
        }


class Manager(FullTimeEmployee):
    """
    Inherits from FullTimeEmployee. Represents a manager who also gets a bonus.
    """
    def __init__(self, employee_id: str, name: str, department: str, monthly_salary: float, bonus: float):
        super().__init__(employee_id, name, department, monthly_salary)
        self.bonus = bonus

    @property
    def bonus(self) -> float:
        return self.__bonus

    @bonus.setter
    def bonus(self, value: float):
        if value < 0:
            raise ValueError("Bonus cannot be negative.")
        self.__bonus = value

    def calculate_salary(self) -> float:
        """Overrides FullTimeEmployee's calculate_salary."""
        return self.monthly_salary + self.bonus

    def display_details(self) -> str:
        base_details = Employee.display_details(self)
        return f"{base_details} | Type: Manager   | Salary: ${self.calculate_salary():,.2f} (Base: ${self.monthly_salary:,.2f}, Bonus: ${self.bonus:,.2f})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "manager",
            "id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "monthly_salary": self.monthly_salary,
            "bonus": self.bonus
        }
