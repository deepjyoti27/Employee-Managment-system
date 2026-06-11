import sys
import time
from colorama import init, Fore, Style
from employee import FullTimeEmployee, PartTimeEmployee, Manager
from company import Company

# Initialize colorama
init(autoreset=True)

ASCII_BANNER = r"""
  ______                 _                         __  __                                              _   
 |  ____|               | |                       |  \/  |                                            | |  
 | |__   _ __ ___  _ __ | | ___  _   _  ___  ___  | \  / | __ _ _ __   __ _  __ _  ___ _ __ ___   ___| |_ 
 |  __| | '_ ` _ \| '_ \| |/ _ \| | | |/ _ \/ _ \ | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ __|
 | |____| | | | | | |_) | | (_) | |_| |  __/  __/ | |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ |_ 
 |______|_| |_| |_| .__/|_|\___/ \__, |\___|\___| |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|\__|
                  | |             __/ |                                      __/ |                        
                  |_|            |___/                                      |___/                         
"""

def print_banner():
    print(Fore.CYAN + Style.BRIGHT + ASCII_BANNER)
    print(Fore.YELLOW + "==================================================================")
    print(Fore.YELLOW + f"{'WELCOME TO THE NEXT-GEN EMPLOYEE MANAGEMENT SYSTEM':^66}")
    print(Fore.YELLOW + "==================================================================\n")

def show_loading_animation(message="Loading", duration=1.5):
    """Shows a simple loading animation on the console."""
    sys.stdout.write(Fore.CYAN + message)
    sys.stdout.flush()
    steps = 3
    for _ in range(steps):
        time.sleep(duration / steps)
        sys.stdout.write(Fore.CYAN + ".")
        sys.stdout.flush()
    print("\n")

def print_success(message):
    print(Fore.GREEN + Style.BRIGHT + f"✅ SUCCESS: {message}")

def print_error(message):
    print(Fore.RED + Style.BRIGHT + f"❌ ERROR: {message}")

def print_info(message):
    print(Fore.BLUE + Style.BRIGHT + f"ℹ️ INFO: {message}")

def get_valid_float(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print_error("Value cannot be negative. Please try again.")
                continue
            return val
        except ValueError:
            print_error("Invalid input. Please enter a valid number.")

def get_valid_string(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if not val:
            print_error("Value cannot be empty. Please try again.")
            continue
        return val

def add_employee_menu(company: Company):
    print(Fore.MAGENTA + Style.BRIGHT + "\n--- Add New Employee ---")
    emp_type = input("Select Type (1: Full-Time, 2: Part-Time, 3: Manager): ").strip()
    
    try:
        emp_id = get_valid_string("Enter Employee ID: ")
        if company.search_employee(emp_id):
            print_error(f"Employee with ID {emp_id} already exists.")
            return

        name = get_valid_string("Enter Name: ")
        dept = get_valid_string("Enter Department: ")

        if emp_type == "1":
            salary = get_valid_float("Enter Monthly Salary: ")
            emp = FullTimeEmployee(emp_id, name, dept, salary)
        elif emp_type == "2":
            rate = get_valid_float("Enter Hourly Rate: ")
            hours = get_valid_float("Enter Hours Worked Per Month: ")
            emp = PartTimeEmployee(emp_id, name, dept, rate, hours)
        elif emp_type == "3":
            salary = get_valid_float("Enter Base Monthly Salary: ")
            bonus = get_valid_float("Enter Bonus: ")
            emp = Manager(emp_id, name, dept, salary, bonus)
        else:
            print_error("Invalid employee type selected.")
            return

        company.add_employee(emp)
        print_success(f"Employee '{name}' added successfully!")
    except ValueError as e:
        print_error(str(e))

def update_employee_menu(company: Company):
    print(Fore.MAGENTA + Style.BRIGHT + "\n--- Update Employee ---")
    emp_id = input("Enter Employee ID to update: ").strip()
    emp = company.search_employee(emp_id)
    
    if not emp:
        print_error(f"Employee with ID {emp_id} not found.")
        return

    print_info(f"Updating Employee: {emp.name} ({emp.__class__.__name__})")
    
    try:
        name = input("Enter new Name (leave blank to keep current): ").strip()
        if name:
            company.update_employee(emp_id, name=name)
            
        dept = input("Enter new Department (leave blank to keep current): ").strip()
        if dept:
            company.update_employee(emp_id, department=dept)
            
        if isinstance(emp, FullTimeEmployee) and not isinstance(emp, Manager):
            salary_str = input("Enter new Monthly Salary (leave blank to keep current): ").strip()
            if salary_str:
                company.update_employee(emp_id, monthly_salary=float(salary_str))
                
        elif isinstance(emp, PartTimeEmployee):
            rate_str = input("Enter new Hourly Rate (leave blank to keep current): ").strip()
            if rate_str:
                company.update_employee(emp_id, hourly_rate=float(rate_str))
            hours_str = input("Enter new Hours Worked (leave blank to keep current): ").strip()
            if hours_str:
                company.update_employee(emp_id, hours_worked_per_month=float(hours_str))
                
        elif isinstance(emp, Manager):
            salary_str = input("Enter new Base Monthly Salary (leave blank to keep current): ").strip()
            if salary_str:
                company.update_employee(emp_id, monthly_salary=float(salary_str))
            bonus_str = input("Enter new Bonus (leave blank to keep current): ").strip()
            if bonus_str:
                company.update_employee(emp_id, bonus=float(bonus_str))
        
        print_success("Employee updated successfully!")
    except ValueError as e:
        print_error(str(e))

def display_menu():
    print(Fore.YELLOW + "\n==================================")
    print(Fore.YELLOW + Style.BRIGHT + "   EMPLOYEE MANAGEMENT SYSTEM   ")
    print(Fore.YELLOW + "==================================")
    print("1  ➕ Add Employee")
    print("2  👥 View Employees")
    print("3  🔍 Search Employee")
    print("4  🗑️  Remove Employee")
    print("5  ✏️  Update Employee")
    print("6  💰 Calculate Payroll")
    print("7  📊 Department Summary")
    print("8  💲 Sort by Salary")
    print("9  🔠 Sort by Name")
    print("10 📄 Export Payroll Report")
    print("11 ❌ Exit")
    print(Fore.YELLOW + "==================================")

def main():
    print_banner()
    show_loading_animation("Initializing System", duration=1.0)
    
    try:
        company = Company()
    except Exception as e:
        print_error(f"Failed to initialize company: {e}")
        return

    while True:
        display_menu()
        choice = input(Fore.CYAN + Style.BRIGHT + "Enter your choice (1-11): " + Style.RESET_ALL).strip()

        try:
            if choice == "1":
                add_employee_menu(company)
            
            elif choice == "2":
                employees = company.display_all_employees()
                if not employees:
                    print_info("No employees found.")
                else:
                    print(Fore.MAGENTA + Style.BRIGHT + "\n--- Employee List ---")
                    for emp in employees:
                        print(emp.display_details())
            
            elif choice == "3":
                sub_choice = input("Search by (1: ID, 2: Name, 3: Department, 4: Role/Type): ").strip()
                if sub_choice == "1":
                    emp_id = input("Enter ID: ").strip()
                    emp = company.search_employee(emp_id)
                    if emp:
                        print(Fore.GREEN + Style.BRIGHT + "\nEmployee Found:")
                        print(emp.display_details())
                    else:
                        print_error("Employee not found.")
                elif sub_choice == "2":
                    name = input("Enter Name: ").strip()
                    results = company.search_by_name(name)
                    if results:
                        print(Fore.GREEN + Style.BRIGHT + f"\nFound {len(results)} matches:")
                        for emp in results:
                            print(emp.display_details())
                    else:
                        print_error("No matches found.")
                elif sub_choice == "3":
                    dept = input("Enter Department: ").strip()
                    results = company.search_by_department(dept)
                    if results:
                        print(Fore.GREEN + Style.BRIGHT + f"\nFound {len(results)} employees in {dept}:")
                        for emp in results:
                            print(emp.display_details())
                    else:
                        print_error("No matches found.")
                elif sub_choice == "4":
                    emp_type = input("Enter Role/Type (e.g., Full-Time, Part-Time, Manager): ").strip()
                    results = company.search_by_type(emp_type)
                    if results:
                        print(Fore.GREEN + Style.BRIGHT + f"\nFound {len(results)} employees matching '{emp_type}':")
                        for emp in results:
                            print(emp.display_details())
                    else:
                        print_error("No matches found.")
                else:
                    print_error("Invalid choice.")
            
            elif choice == "4":
                emp_id = input("Enter Employee ID to remove: ").strip()
                if company.remove_employee(emp_id):
                    print_success(f"Employee with ID {emp_id} removed successfully.")
                else:
                    print_error("Employee not found.")
            
            elif choice == "5":
                update_employee_menu(company)
            
            elif choice == "6":
                total = company.calculate_total_payroll()
                print_info(f"Total Payroll for the company: ${total:,.2f}")
            
            elif choice == "7":
                summary = company.department_summary()
                if not summary:
                    print_info("No data available.")
                else:
                    print(Fore.MAGENTA + Style.BRIGHT + "\n--- Department Summary ---")
                    for dept, stats in summary.items():
                        print(f"Department: {dept:15} | Employees: {stats['count']:<3} | Avg Salary: ${stats['avg_salary']:,.2f}")
            
            elif choice == "8":
                company.sort_by_salary()
                print_success("Employees sorted by salary (Descending).")
                for emp in company.display_all_employees():
                    print(emp.display_details())
            
            elif choice == "9":
                company.sort_by_name()
                print_success("Employees sorted by name (A-Z).")
                for emp in company.display_all_employees():
                    print(emp.display_details())
            
            elif choice == "10":
                report = company.generate_payroll_report()
                with open("payroll_report.txt", "w", encoding='utf-8') as f:
                    f.write(report)
                print(Fore.WHITE + report)
                print_success("Report exported to 'payroll_report.txt'.")
            
            elif choice == "11":
                show_loading_animation("Saving data and shutting down", duration=1.0)
                print(Fore.GREEN + Style.BRIGHT + "Thank you for using Employee Management System. Goodbye!")
                break
            
            else:
                print_error("Invalid choice. Please select from 1-11.")
                
        except KeyboardInterrupt:
            print("\n" + Fore.RED + "Operation cancelled by user. Returning to menu...")
        except Exception as e:
            print_error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
