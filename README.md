# Workforce-Data-Pipeline

##Project Overview

This project builds a lightweight data pipeline to transform raw, inconsistent HR source files into clean, validated, and analytics ready datasets. The pipeline ingests multiple raw data sources, applies data cleaning and validation rules, generates a data quality report, and produces structured outputs for reporting and dashboarding.

##Business Problem

HR and business reporting teams often receive raw source files that are not standardized or analyticsr eady. These datasets frequently contain:

- Duplicate records
- Missing or inconsistent values
- Invalid date formats
- Mismatched reference data

This results in manual data cleanup, reporting delays, and increased risk of inaccurate insights. Leadership needs a repeatable process to ensure data is reliable and ready for reporting.

## Objectives
- Ingest multiple raw HR data sources
- Clean and standardize inconsistent data
- Identify and quantify data quality issues
- Apply validation rules and business logic
- Transform data into analytics-ready tables
- Generate a data quality report for transparency
- Export clean datasets for reporting and dashboarding

## Tools Used
- Python (Pandas, NumPy) 
- Jupyter Notebook 
- Python Script 
- CSV / Excel
  
## Dataset

Raw Input Files:
- raw_employees.csv
- raw_departments.csv
- raw_terminations.csv
  
Key Fields:
- employee_id – Unique identifier (with duplicates in raw data)
- department – Department name (inconsistent formatting)
- job_level – Role level (missing values present)
- hire_date – Mixed formats and invalid values
- termination_date – Includes invalid and missing values
- salary – Numeric field with variability

Data Characteristics:
- 500+ employee records
- Intentionally messy data to simulate real-world conditions
- Includes duplicates, missing values, inconsistent formatting, and invalid dates

## Methodology
1. Data Ingestion
  -  Loaded raw datasets from multiple source files
2. Data Cleaning
  - Standardized text fields (names, departments, job levels)
  - Trimmed whitespace and fixed casing
  - Replaced missing values with default categories
  - Converted date fields and flagged invalid records
  - Removed duplicate employee records
3. Data Validation
  - Identified duplicate employee IDs
  - Flagged missing departments and job levels
  - Detected invalid hire and termination dates
  - Checked for unmatched department values
4. Data Transformation
  - Joined employee, department, and termination data
  - Created an employee master table
  - Derived active and terminated employee flags
  - Structured data for reporting use cases
5. Data Quality Reporting
Generated a data quality report capturing:
  - Issue type
  - Issue count
  - Severity level
  - Recommended action
6. Output Generation
Exported clean, analytics-ready datasets for reporting

## Key Metrics
- Duplicate Employee Records Identified
- Missing Department Values
- Missing Job Level Values
- Invalid Hire Dates
- Invalid Termination Dates
- Unmatched Department Records

These metrics provide visibility into data quality and help prioritize remediation efforts.

## Results Summary
- Successfully transformed messy, inconsistent HR data into structured, analytics-ready datasets
- Identified and quantified key data quality issues across multiple source systems
- Standardized critical fields such as department, job level, and dates
- Created a reusable pipeline that reduces manual data preparation effort
- Enabled downstream reporting for headcount and turnover analysis

## Business Recommendation
To improve data reliability and reporting efficiency:
- Implement standardized data validation rules at the source system level to reduce downstream cleanup
- Automate data quality monitoring using a recurring pipeline process
- Address high-severity issues (e.g., invalid dates, duplicates) first to ensure reporting accuracy
- Maintain a centralized, clean employee master dataset for consistent reporting across teams

By operationalizing this pipeline, organizations can reduce manual effort, improve data accuracy, and enable faster, more reliable decision-making.

## Pipeline Flowchart
<img width="731" height="858" alt="Screenshot 2026-04-29 120915" src="https://github.com/user-attachments/assets/2fbbc0fb-248f-4beb-b9b8-daf27bd9113b" />

## Portfolio Link
View the full business case and dashboard summary in my [Notion portfolio](https://www.notion.so/Data-Science-Portfolio-6edb5c142bd5828688a901519a004abb?source=copy_link)
