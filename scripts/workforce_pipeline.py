# 1. Import Libraries
import pandas as pd
import numpy as np

# 2. Load Raw Data
employees_raw = pd.read_csv("raw_employees.csv")
departments_raw = pd.read_csv("raw_departments.csv")
terminations_raw = pd.read_csv("raw_terminations.csv")

# 3. Create Data Quality Report Framework
dq_checks = []

def add_dq_check(check_name, issue_count, severity, recommended_action):
    dq_checks.append({
        "check_name": check_name,
        "issue_count": int(issue_count),
        "severity": severity,
        "recommended_action": recommended_action
    })

# 4. Raw Data Quality Checks
add_dq_check(
    "Duplicate employee IDs in raw employee file",
    employees_raw["employee_id"].duplicated().sum(),
    "High",
    "Deduplicate employee records before creating employee master."
)

add_dq_check(
    "Missing department in raw employee file",
    employees_raw["department"].isnull().sum(),
    "Medium",
    "Replace missing departments with Unknown or resolve using source system."
)

add_dq_check(
    "Missing job level in raw employee file",
    employees_raw["job_level"].isnull().sum(),
    "Medium",
    "Replace missing job levels with Unknown or validate with HR source."
)

add_dq_check(
    "Missing termination reason",
    terminations_raw["reason"].isnull().sum(),
    "Low",
    "Replace missing termination reasons with Unknown."
)

# 5. Clean Employees
employees = employees_raw.copy()

employees["name"] = employees["name"].astype(str).str.strip().str.title()

employees["department"] = (
    employees["department"]
    .astype(str)
    .str.strip()
    .str.title()
    .replace(["None", "Nan", "NaN", ""], np.nan)
    .fillna("Unknown")
)

employees["job_level"] = (
    employees["job_level"]
    .astype(str)
    .str.strip()
    .str.title()
    .replace(["None", "Nan", "NaN", ""], np.nan)
    .fillna("Unknown")
)

employees["hire_date_clean"] = pd.to_datetime(
    employees["hire_date"],
    errors="coerce"
)

employees["invalid_hire_date_flag"] = employees["hire_date_clean"].isnull().astype(int)
employees["salary"] = pd.to_numeric(employees["salary"], errors="coerce")
employees = employees.drop_duplicates(subset=["employee_id"], keep="first")

# 6. Clean Departments
departments = departments_raw.copy()

departments["department"] = departments["department"].astype(str).str.strip().str.title()
departments["manager"] = departments["manager"].astype(str).str.strip().str.title()
departments = departments.drop_duplicates(subset=["department"], keep="first")

# 7. Clean Terminations
terminations = terminations_raw.copy()

terminations["termination_date_clean"] = pd.to_datetime(
    terminations["termination_date"],
    errors="coerce"
)

terminations["invalid_termination_date_flag"] = (
    terminations["termination_date_clean"].isnull().astype(int)
)

terminations["reason"] = (
    terminations["reason"]
    .astype(str)
    .str.strip()
    .str.title()
    .replace(["None", "Nan", "NaN", ""], np.nan)
    .fillna("Unknown")
)

terminations = terminations.drop_duplicates(subset=["employee_id"], keep="first")

# 8. Post-Cleaning Data Quality Checks
add_dq_check(
    "Invalid hire dates after cleaning",
    employees["invalid_hire_date_flag"].sum(),
    "High",
    "Review records with invalid hire dates before time-based reporting."
)

add_dq_check(
    "Invalid termination dates after cleaning",
    terminations["invalid_termination_date_flag"].sum(),
    "High",
    "Review records with invalid termination dates before turnover reporting."
)

add_dq_check(
    "Unknown departments after cleaning",
    (employees["department"] == "Unknown").sum(),
    "Medium",
    "Resolve Unknown departments with HR source system."
)

add_dq_check(
    "Unknown job levels after cleaning",
    (employees["job_level"] == "Unknown").sum(),
    "Medium",
    "Resolve Unknown job levels with HR source system."
)

# 9. Create Employee Master
employee_master = employees.merge(
    departments,
    on="department",
    how="left"
)

employee_master = employee_master.merge(
    terminations[
        [
            "employee_id",
            "termination_date_clean",
            "reason",
            "invalid_termination_date_flag"
        ]
    ],
    on="employee_id",
    how="left"
)

employee_master["active_flag"] = employee_master["termination_date_clean"].isnull().astype(int)
employee_master["terminated_flag"] = employee_master["termination_date_clean"].notnull().astype(int)

employee_master = employee_master.rename(columns={
    "hire_date_clean": "hire_date",
    "termination_date_clean": "termination_date",
    "reason": "termination_reason"
})

employee_master = employee_master[
    [
        "employee_id",
        "name",
        "department",
        "manager",
        "job_level",
        "hire_date",
        "termination_date",
        "termination_reason",
        "salary",
        "active_flag",
        "terminated_flag",
        "invalid_hire_date_flag",
        "invalid_termination_date_flag"
    ]
]

# 10. Department Match Check
add_dq_check(
    "Departments not matched to department lookup",
    employee_master["manager"].isnull().sum(),
    "Medium",
    "Add missing departments to lookup table or correct source values."
)

# 11. Headcount Summary
headcount_summary = employee_master.groupby(
    ["department", "job_level"]
).agg(
    total_employees=("employee_id", "count"),
    active_employees=("active_flag", "sum"),
    terminated_employees=("terminated_flag", "sum"),
    avg_salary=("salary", "mean")
).reset_index()

headcount_summary["avg_salary"] = headcount_summary["avg_salary"].round(2)

# 12. Turnover Summary
turnover_summary = employee_master.groupby("department").agg(
    total_employees=("employee_id", "count"),
    active_employees=("active_flag", "sum"),
    terminated_employees=("terminated_flag", "sum")
).reset_index()

turnover_summary["turnover_rate"] = (
    turnover_summary["terminated_employees"] / turnover_summary["total_employees"]
).round(4)

# 13. Data Quality Report
data_quality_report = pd.DataFrame(dq_checks)

# 14. Export Processed Files
employee_master.to_csv("clean_employee_master.csv", index=False)
headcount_summary.to_csv("clean_headcount_summary.csv", index=False)
turnover_summary.to_csv("clean_turnover_summary.csv", index=False)
data_quality_report.to_csv("data_quality_report.csv", index=False)

print("Processed files created successfully.")
