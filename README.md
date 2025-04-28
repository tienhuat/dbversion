# dbversion

## Purpose

This Python script has been created to perform database queries and generate a comprehensive database version report, which encompasses the following components:

1. Database schema elements, including tables, views, stored procedures, triggers, indexes, check constraints, unique constraints, and more.

1. Configuration data that directly influences the program's logic, such as code tables, rules, workflows, and so forth. You have the flexibility to customize the SQL script within the `xxx_dbversion.py` file as needed.

Additionally, it will create a SHA1 hash of the database version report.

For sample reports, please refer to `dbversion_report.txt` and `dbversion_hash.txt`.

Currently, it only supports MySQL databases (using `mysql_dbversion.py` and `mysql_main.py`) as well as MS SQL databases (using `mssql_dbversion.py` and `mssql_main.py`).

## Use Cases

1. Compare database versions without depending on commercial tools.
1. Detect unauthorized changes in the database version by regularly running a batch job that compares the expected hash with the calculated hash of the live database.
1. By including the database version report and its hash in the source code repository, we can establish a connection between the database version and the source code, facilitating version control of the database.
1. Ensure that the database version is accurately updated to the desired state after making any changes. This process can be automated within a CI/CD pipeline by comparing the hash in the source code repository with the computed hash of the live database following modifications.
 
 
## Instructions
```python 
# Install the Python virtual environment, optional
python3 -m venv venv

# Activate the venv in the terminal session
source venv/bin/activate
# venv/Scripts/activate.bat (for Windows cmd)
# venv/Script/activate.ps1 (for Windows PowerShell)

# Install database driver in venv, or global environment, if venv is not activated
pip install mysql-connector-python
# or pip install pyodbc (to access MS SQL database)
# pip install psycopg2-binary


# Define the parameters in `mysql_main.py` or `mssql_main.py` before use

# Generate the report and hash.
python3 mysql_main.py
# or python3 mssql_main.py

# `dbversion_report.txt` and `dbversion_hash.txt` will be generated in the working directory

# Deactivate the venv in the terminal session, optional 
deactivate
```
 
 ## License
 See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
