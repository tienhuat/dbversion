# dbversion

## Purpose

This Python script is designed to query the database and generate a database version report, including the following elements:

* Database schema elements such as tables, views, stored procedures, triggers, indexes, check constraints, unique constraints, etc.
* Configuration data that impacts the program's logic, e.g. code table, rules, workflow, etc. You can customize the SQL script inside the `xxx_dbversion.py` file.

Additionally, it will create a SHA1 hash of the dbversion report.

For sample reports, please refer to `dbversion_report.txt` and `dbversion_hash.txt`.

Currently, it only supports MySQL databases (using `mysql_dbversion.py` and `mysql_main.py`) as well as MS SQL databases (using `mssql_dbversion.py` and `mssql_main.py`).

## Use Cases

* Compare database versions without using commercial tools
* Detect unauthorized changes of database schema/configuration data
* By checking the dbversion report and its hash into source code repository, we can link the database version with source code and version control it
* Ensure that the database version is properly changed after the changes are applied. This step can be automated in CI/CD pipeline by checking the hash in the source code repository and the database version of the deployed database
 
## Instructions
```python 
# Install the Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python
# or pip install pymssql

# Define the parameters in `mysql_main.py` or `mssql_main.py` before use

# Generate the report
python3 mysql_main.py
# or python3 mssql_main.py

# `dbversion_report.txt` and `dbversion_hash.txt` will be generated in the current folder

# Deactivate the venv
deactivate
```
 

