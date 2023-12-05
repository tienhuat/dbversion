# dbversion

## Purpose
This python script will access the database to generate the report for the following
 * database schema, eg table, view, stored procedures, index, unique constraints
 * master data, which affect the program logic. Customize the sql script inside dbversion.py

It will also generate a SHA1 hash of the dbversion report. 

Currently it only support MySQL database (mysql_dbversion.py and mysql_main.py) and MS SQL (mssql_dbversion.py and mssql_main.py). 


## Instruction
```python 
# install python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python

# define the parameter in mysql_main.py or mssql_main.py before use
python3 mssql_main.py
# or python3 mysql_main.py
deactivate
```
Run the script by calling main.py

