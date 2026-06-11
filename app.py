from flask import Flask, render_template, request, redirect, url_for, flash
from company import Company
from employee import FullTimeEmployee, PartTimeEmployee, Manager

app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages"  # Required for flash messages

# Initialize company
try:
    company = Company("employees.json")
except Exception as e:
    print(f"Error initializing company: {e}")
    company = Company("employees.json") # retry or handle gracefully. It throws exception if file is corrupted.

@app.route("/")
def index():
    search_query = request.args.get("search", "").strip().lower()
    employees = company.display_all_employees()
    
    if search_query:
        filtered_employees = []
        for emp in employees:
            emp_type = emp.__class__.__name__.lower()
            if (search_query in emp.employee_id.lower() or 
                search_query in emp.name.lower() or 
                search_query in emp.department.lower() or 
                search_query in emp_type):
                filtered_employees.append(emp)
        employees = filtered_employees

    summary = company.department_summary()
    total_payroll = company.calculate_total_payroll()
    
    return render_template("index.html", 
                           employees=employees, 
                           summary=summary, 
                           total_payroll=total_payroll,
                           search_query=request.args.get("search", "").strip())

@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        emp_type = request.form.get("type")
        emp_id = request.form.get("employee_id")
        name = request.form.get("name")
        department = request.form.get("department")

        try:
            if company.search_employee(emp_id):
                flash(f"Employee with ID {emp_id} already exists.", "danger")
                return redirect(url_for("add_employee"))

            if emp_type == "fulltime":
                salary = float(request.form.get("monthly_salary", 0))
                emp = FullTimeEmployee(emp_id, name, department, salary)
            elif emp_type == "parttime":
                rate = float(request.form.get("hourly_rate", 0))
                hours = float(request.form.get("hours_worked", 0))
                emp = PartTimeEmployee(emp_id, name, department, rate, hours)
            elif emp_type == "manager":
                salary = float(request.form.get("monthly_salary", 0))
                bonus = float(request.form.get("bonus", 0))
                emp = Manager(emp_id, name, department, salary, bonus)
            else:
                flash("Invalid employee type selected.", "danger")
                return redirect(url_for("add_employee"))

            company.add_employee(emp)
            flash(f"Employee '{name}' added successfully!", "success")
            return redirect(url_for("index"))

        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for("add_employee"))

    return render_template("add.html")

@app.route("/delete/<emp_id>", methods=["POST"])
def delete_employee(emp_id):
    if company.remove_employee(emp_id):
        flash(f"Employee with ID {emp_id} removed successfully.", "success")
    else:
        flash(f"Employee with ID {emp_id} not found.", "danger")
    return redirect(url_for("index"))

@app.route("/update/<emp_id>", methods=["GET", "POST"])
def update_employee(emp_id):
    emp = company.search_employee(emp_id)
    if not emp:
        flash(f"Employee with ID {emp_id} not found.", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        department = request.form.get("department")
        
        try:
            if name:
                company.update_employee(emp_id, name=name)
            if department:
                company.update_employee(emp_id, department=department)

            if isinstance(emp, FullTimeEmployee) and not isinstance(emp, Manager):
                salary_str = request.form.get("monthly_salary")
                if salary_str:
                    company.update_employee(emp_id, monthly_salary=float(salary_str))
                    
            elif isinstance(emp, PartTimeEmployee):
                rate_str = request.form.get("hourly_rate")
                if rate_str:
                    company.update_employee(emp_id, hourly_rate=float(rate_str))
                hours_str = request.form.get("hours_worked")
                if hours_str:
                    company.update_employee(emp_id, hours_worked_per_month=float(hours_str))
                    
            elif isinstance(emp, Manager):
                salary_str = request.form.get("monthly_salary")
                if salary_str:
                    company.update_employee(emp_id, monthly_salary=float(salary_str))
                bonus_str = request.form.get("bonus")
                if bonus_str:
                    company.update_employee(emp_id, bonus=float(bonus_str))

            flash("Employee updated successfully!", "success")
            return redirect(url_for("index"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("update.html", emp=emp)

if __name__ == "__main__":
    app.run(debug=True)
