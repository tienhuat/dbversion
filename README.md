# dbversion

## Purpose
This python script will access the database to generate the report for the following
 * database schema, eg table, view, stored procedures, index, unique constraints
 * master data, which affect the program logic. Customize the sql script inside dbversion.py

It will also generate a SHA1 hash of the dbversion report. 

Currently it only support MySQL database. 


## Installation
```python 
# install python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python
deactivate
```
Run the script by calling main.py

