import json
import os
from typing import List, Optional, Dict
from employee import Employee

class Company:
    """
    Manages a collection of Employee objects.
    Demonstrates file handling, collections, and polymorphism.
    """
    def __init__(self, data_file: str = "employees.json"):
        self.__employees: List[Employee] = []
        self.__data_file = data_file
        self._load_data()

    def _load_data(self):
        """Loads employee data from a JSON file into objects."""
        if not os.path.exists(self.__data_file):
            return
        
        try:
            with open(self.__data_file, 'r', encoding='utf-8') as file:
                data_list = json.load(file)
                for item in data_list:
                    emp = Employee.from_dict(item)
                    self.__employees.append(emp)
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from file {self.__data_file}. File may be corrupted.")
        except Exception as e:
            raise Exception(f"Failed to load data: {e}")

    def _save_data(self):
        """Saves current employee objects back to the JSON file."""
        try:
            data_list = [emp.to_dict() for emp in self.__employees]
            with open(self.__data_file, 'w', encoding='utf-8') as file:
                json.dump(data_list, file, indent=4)
        except Exception as e:
            raise Exception(f"Failed to save data: {e}")

    def add_employee(self, employee: Employee):
        """Adds a new employee and auto-saves."""
        if self.search_employee(employee.employee_id):
            raise ValueError(f"Employee with ID {employee.employee_id} already exists.")
        
        self.__employees.append(employee)
        self._save_data()

    def remove_employee(self, employee_id: str) -> bool:
        """Removes an employee by ID and auto-saves."""
        emp = self.search_employee(employee_id)
        if emp:
            self.__employees.remove(emp)
            self._save_data()
            return True
        return False

    def update_employee(self, employee_id: str, **kwargs):
        """Updates attributes of an existing employee and auto-saves."""
        emp = self.search_employee(employee_id)
        if not emp:
            raise ValueError(f"Employee with ID {employee_id} not found.")

        for key, value in kwargs.items():
            if hasattr(emp, key):
                setattr(emp, key, value)
            else:
                raise ValueError(f"Invalid attribute '{key}' for employee type.")
        self._save_data()

    def search_employee(self, employee_id: str) -> Optional[Employee]:
        """Searches for an employee by ID."""
        for emp in self.__employees:
            if emp.employee_id == employee_id:
                return emp
        return None

    def search_by_name(self, name: str) -> List[Employee]:
        """Searches for employees matching the given name partially or fully."""
        return [emp for emp in self.__employees if name.lower() in emp.name.lower()]

    def search_by_department(self, department: str) -> List[Employee]:
        """Searches for employees in a specific department."""
        return [emp for emp in self.__employees if department.lower() == emp.department.lower()]

    def search_by_type(self, emp_type: str) -> List[Employee]:
        """Searches for employees by their role/type."""
        return [emp for emp in self.__employees if emp_type.lower().replace(" ", "").replace("-", "") in emp.__class__.__name__.lower()]

    def display_all_employees(self) -> List[Employee]:
        """Returns the list of all employees."""
        return self.__employees

    def calculate_total_payroll(self) -> float:
        """Calculates total payroll for all employees."""
        return sum(emp.calculate_salary() for emp in self.__employees)

    def sort_by_name(self):
        """Sorts the employee list by name."""
        self.__employees.sort(key=lambda emp: emp.name.lower())

    def sort_by_salary(self):
        """Sorts the employee list by salary in descending order."""
        self.__employees.sort(key=lambda emp: emp.calculate_salary(), reverse=True)

    def department_summary(self) -> Dict[str, Dict[str, float]]:
        """Returns count and average salary per department."""
        summary = {}
        for emp in self.__employees:
            dept = emp.department
            sal = emp.calculate_salary()
            if dept not in summary:
                summary[dept] = {"count": 0, "total_salary": 0.0}
            summary[dept]["count"] += 1
            summary[dept]["total_salary"] += sal
        
        for dept, stats in summary.items():
            stats["avg_salary"] = stats["total_salary"] / stats["count"]
            
        return summary

    def generate_payroll_report(self) -> str:
        """Generates a formatted payroll report string."""
        if not self.__employees:
            return "No employees found to generate a report."

        lines = []
        lines.append("-" * 75)
        lines.append(f"{'PAYROLL REPORT':^75}")
        lines.append("-" * 75)
        lines.append(f"{'ID':<10} | {'Name':<15} | {'Type':<15} | {'Department':<12} | {'Salary':>10}")
        lines.append("-" * 75)

        highest_salary = float('-inf')
        lowest_salary = float('inf')

        for emp in self.__employees:
            sal = emp.calculate_salary()
            emp_type = emp.__class__.__name__.replace("Employee", "")
            lines.append(f"{emp.employee_id:<10} | {emp.name[:15]:<15} | {emp_type[:15]:<15} | {emp.department[:12]:<12} | ${sal:,.2f}")
            
            if sal > highest_salary:
                highest_salary = sal
            if sal < lowest_salary:
                lowest_salary = sal

        total_payroll = self.calculate_total_payroll()
        count = len(self.__employees)
        avg_salary = total_payroll / count if count > 0 else 0

        lines.append("-" * 75)
        lines.append(f"Total Payroll:  ${total_payroll:,.2f}")
        lines.append(f"Highest Salary: ${highest_salary:,.2f}" if count > 0 else "Highest Salary: N/A")
        lines.append(f"Lowest Salary:  ${lowest_salary:,.2f}" if count > 0 else "Lowest Salary: N/A")
        lines.append(f"Average Salary: ${avg_salary:,.2f}")
        lines.append(f"Employee Count: {count}")
        lines.append("-" * 75)

        return "\n".join(lines)
