import mysql.connector
from mysql.connector import Error 

import hashlib
import json


class Dbversion:
   
    # Constructor to initialize instance variables
    def __init__(self, host, databasse, user, password):
        self.host = host      
        self.database = databasse
        self.user = user        
        self.password = password

    
    def get_dbversion_report(self):
        
        report = ""

        try:
            # Connect to the MySQL database
            connection = mysql.connector.connect(
                host=self.host, 
                database=self.database,                             
                user=self.user,
                password=self.password
            )

            if connection.is_connected():
                db_info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
              
                
                for queryName, queryStatement in self.sqls.items():         

                    queryStatement = queryStatement.replace("%schema_name", "'" + self.database + "' ")

                    cursor.execute(queryStatement)
                    rows = cursor.fetchall()
                    
                    report = report + "--------------------------------------------" + "\r\n"
                    report = report + queryName + ":" + str(cursor.rowcount) +  "\r\n"
                    report = report + "--------------------------------------------" + "\r\n"
     

                    report = report + self.to_json(cursor, rows) + "\r\n" 
                    report = report + "\r\n\r\n"
                
                report = report.strip()          
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            # Closing the connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        return report

    
    def calculate_hash(self, text):
        # Create a new hash object using the specified algorithm
        algorithm='sha256'
        hash_object = hashlib.new(algorithm)
        
        # Update the hash object with the bytes of the text
        hash_object.update(text.encode())

        # Return the hexadecimal digest of the hash
        return hash_object.hexdigest()
    
    def to_json(self, cursor, rows):
        # Assuming you know the column names
        column_names = [description[0] for description in cursor.description]

        # Convert each row to JSON
        json_data = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            json_row = json.dumps(row_dict)
            json_data.append(json_row)

        return "\r\n".join(json_data)

    sqls = {
    # --------------------------------
    # schema
    # --------------------------------
    "schema":
"""select 
distinct 
sc.CATALOG_NAME,
sc.SCHEMA_NAME,
sc.DEFAULT_CHARACTER_SET_NAME,
sc.DEFAULT_COLLATION_NAME,
sc.DEFAULT_ENCRYPTION

from information_schema.schemata sc
where sc.schema_name = %schema_name

order by 
sc.CATALOG_NAME,
sc.SCHEMA_NAME,
sc.DEFAULT_CHARACTER_SET_NAME,
sc.DEFAULT_COLLATION_NAME,
sc.DEFAULT_ENCRYPTION
""", 

    # --------------------------------
    # tables
    # --------------------------------
    "table":
"""SELECT 
  distinct 
  t.TABLE_CATALOG, 
  t.TABLE_SCHEMA, 
  t.TABLE_NAME, 
  t.TABLE_TYPE, 
  t.ENGINE, 
  t.ROW_FORMAT
FROM 
    INFORMATION_SCHEMA.tables  t
where t.table_schema = %schema_name
and t.table_name  not like '\_\_%'
order by 
  t.TABLE_CATALOG, 
  t.TABLE_SCHEMA, 
  t.TABLE_NAME, 
  t.TABLE_TYPE, 
  t.ENGINE, 
  t.ROW_FORMAT
""", 
    # --------------------------------
    # table extension
    # --------------------------------
    "table_extension":
"""Select 
te.TABLE_CATALOG,
te.TABLE_SCHEMA,
te.TABLE_NAME,
te.ENGINE_ATTRIBUTE,
te.SECONDARY_ENGINE_ATTRIBUTE

from information_schema.TABLES_EXTENSIONS te
where te.TABLE_SCHEMA = %schema_name
and te.TABLE_NAME not like '\_\_%'

order by
te.TABLE_CATALOG,
te.TABLE_SCHEMA,
te.TABLE_NAME,
te.ENGINE_ATTRIBUTE,
te.SECONDARY_ENGINE_ATTRIBUTE
""", 

    # column info
    "column": 
    """SELECT 
    distinct
    c.TABLE_CATALOG, 
    c.TABLE_SCHEMA,    
    c.TABLE_NAME,    
    c.COLUMN_NAME,
    c.COLUMN_DEFAULT,
    c.IS_NULLABLE,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH, 
    c.CHARACTER_OCTET_LENGTH, 
    c.NUMERIC_PRECISION, 
    c.NUMERIC_SCALE,
    c.DATETIME_PRECISION,
    c.CHARACTER_SET_NAME,
    c.COLLATION_NAME, 
    c.COLUMN_TYPE, 
    c.COLUMN_KEY,
    c.SRS_ID, 
    c.GENERATION_EXPRESSION

FROM INFORMATION_SCHEMA.COLUMNS c 

WHERE 
    c.TABLE_SCHEMA = %schema_name
    and c.table_name not like '\_\_%'
    and c.column_name not like '\_\_%'

order by 
   c.TABLE_CATALOG, 
    c.TABLE_SCHEMA,    
    c.TABLE_NAME,    
    c.COLUMN_NAME,
    c.COLUMN_DEFAULT,
    c.IS_NULLABLE,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH, 
    c.CHARACTER_OCTET_LENGTH, 
    c.NUMERIC_PRECISION, 
    c.NUMERIC_SCALE,
    c.DATETIME_PRECISION,
    c.CHARACTER_SET_NAME,
    c.COLLATION_NAME, 
    c.COLUMN_TYPE, 
    c.COLUMN_KEY,    
    c.SRS_ID
""", 

    # --------------------------------
    # column extension
    # --------------------------------
    "column_extension":
"""select 
distinct
ce.TABLE_CATALOG, 
ce.TABLE_SCHEMA, 
ce.TABLE_NAME, 
ce.COLUMN_NAME, 
ce.ENGINE_ATTRIBUTE, 
ce.SECONDARY_ENGINE_ATTRIBUTE

from information_schema.COLUMNS_EXTENSIONS ce
where ce.table_schema = %schema_name
    and ce.table_name not like '\_\_%'
    and ce.column_name not like '\_\_%'
    
order by 
ce.TABLE_CATALOG, 
ce.TABLE_SCHEMA, 
ce.TABLE_NAME, 
ce.COLUMN_NAME, 
ce.ENGINE_ATTRIBUTE, 
ce.SECONDARY_ENGINE_ATTRIBUTE
""", 
    # --------------------------------
    # constraint info
    # --------------------------------
    "constraint": 
"""select 
  distinct 
  tc.CONSTRAINT_CATALOG, 
  tc.table_schema, 
  tc.table_name, 
  tc.CONSTRAINT_NAME, 
  tc.CONSTRAINT_TYPE, 
  tc.ENFORCED

FROM  
  INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc   
where tc.table_schema = %schema_name
and tc.table_name not like '\_\_%'
order by 
tc.CONSTRAINT_CATALOG, 
  tc.table_schema, 
  tc.table_name, 
  tc.CONSTRAINT_NAME, 
  tc.CONSTRAINT_TYPE, 
  tc.ENFORCED
""", 

    # --------------------------------
    # check constraint info
    # --------------------------------
    "check_constraint":
"""select 

cc.CONSTRAINT_CATALOG, 
cc.CONSTRAINT_SCHEMA,
cc.CONSTRAINT_NAME, 
cc.CHECK_CLAUSE

from information_schema.check_constraints cc
where cc.CONSTRAINT_SCHEMA = %schema_name
order by 
cc.CONSTRAINT_CATALOG, 
cc.CONSTRAINT_SCHEMA,
cc.CONSTRAINT_NAME
""", 
    # --------------------------------
    # referential constraints
    # --------------------------------
    "referential_constraint":
"""select 
distinct 
rc.CONSTRAINT_CATALOG,
rc.CONSTRAINT_SCHEMA,
rc.CONSTRAINT_NAME,
rc.UNIQUE_CONSTRAINT_CATALOG,
rc.UNIQUE_CONSTRAINT_SCHEMA,
rc.UNIQUE_CONSTRAINT_NAME,	
rc.TABLE_NAME,
rc.REFERENCED_TABLE_NAME,
rc.MATCH_OPTION,
rc.UPDATE_RULE,
rc.DELETE_RULE
from information_schema.REFERENTIAL_CONSTRAINTS rc
where rc.CONSTRAINT_SCHEMA = %schema_name
ORDER BY
rc.CONSTRAINT_CATALOG,
rc.CONSTRAINT_SCHEMA,
rc.CONSTRAINT_NAME,
rc.UNIQUE_CONSTRAINT_CATALOG,
rc.UNIQUE_CONSTRAINT_SCHEMA,
rc.UNIQUE_CONSTRAINT_NAME,	
rc.TABLE_NAME,
rc.REFERENCED_TABLE_NAME,
rc.MATCH_OPTION,
rc.UPDATE_RULE,
rc.DELETE_RULE
""", 
    # --------------------------------
    # key usage
    # --------------------------------
    "key_usage":
"""select 
  distinct
  cu.CONSTRAINT_CATALOG, 
  cu.TABLE_SCHEMA, 
  cu.TABLE_NAME, 
  cu.COLUMN_NAME, 
  cu.constraint_name, 
  cu.POSITION_IN_UNIQUE_CONSTRAINT, 
  cu.REFERENCED_TABLE_SCHEMA, 
  cu.REFERENCED_TABLE_NAME, 
  cu.REFERENCED_COLUMN_NAME
from INFORMATION_SCHEMA.KEY_COLUMN_USAGE cu
where cu.CONSTRAINT_SCHEMA = %schema_name
and cu.TABLE_NAME not like '\_\_%'
and cu.COLUMN_NAME not like '\_\_%'
order by 
   cu.CONSTRAINT_CATALOG, 
  cu.TABLE_SCHEMA,  
  cu.TABLE_NAME, 
  cu.COLUMN_NAME, 
  cu.constraint_name, 
  cu.POSITION_IN_UNIQUE_CONSTRAINT, 
  cu.REFERENCED_TABLE_SCHEMA, 
  cu.REFERENCED_TABLE_NAME, 
  cu.REFERENCED_COLUMN_NAME
""", 
    # --------------------------------
    # index information
    # --------------------------------
    "index":
"""select 
  
st.TABLE_CATALOG, 
st.TABLE_SCHEMA, 
st.TABLE_NAME, 
st.COLUMN_NAME, 
st.SEQ_IN_INDEX, 
st.INDEX_NAME, 
st.NON_UNIQUE, 
st.COLLATION, 
st.PACKED, 
st.NULLABLE, 
st.INDEX_TYPE,
st.IS_VISIBLE, 

st.EXPRESSION

from INFORMATION_SCHEMA.STATISTICS st
where st.TABLE_SCHEMA = %schema_name
and st.TABLE_NAME not like '\_\_%'
and st.COLUMN_NAME not like '\_\_%'

order by 
st.TABLE_CATALOG, 
st.TABLE_SCHEMA, 
st.TABLE_NAME, 
st.COLUMN_NAME, 
st.SEQ_IN_INDEX, 
st.INDEX_NAME, 
st.NON_UNIQUE, 
st.COLLATION, 
st.PACKED, 
st.NULLABLE, 
st.INDEX_TYPE,
st.IS_VISIBLE
""", 
    # --------------------------------
    # stored proc and function
    # --------------------------------
    "routine": 
"""select 
 
r.SPECIFIC_NAME,
r.ROUTINE_CATALOG,
r.ROUTINE_SCHEMA,
r.ROUTINE_NAME,
r.ROUTINE_TYPE,
r.DATA_TYPE,
r.CHARACTER_MAXIMUM_LENGTH,
r.CHARACTER_OCTET_LENGTH,
r.NUMERIC_PRECISION,
r.NUMERIC_SCALE,
r.DATETIME_PRECISION,
r.CHARACTER_SET_NAME,
r.COLLATION_NAME,
r.DTD_IDENTIFIER,
r.ROUTINE_BODY, 
r.EXTERNAL_NAME,
r.EXTERNAL_LANGUAGE,
r.PARAMETER_STYLE,
r.IS_DETERMINISTIC, 

r.ROUTINE_DEFINITION

from information_schema.routines r
where r.ROUTINE_SCHEMA = %schema_name

order by 

r.SPECIFIC_NAME,
r.ROUTINE_CATALOG,
r.ROUTINE_SCHEMA,
r.ROUTINE_NAME,
r.ROUTINE_TYPE,
r.DATA_TYPE,
r.CHARACTER_MAXIMUM_LENGTH,
r.CHARACTER_OCTET_LENGTH,
r.NUMERIC_PRECISION,
r.NUMERIC_SCALE,
r.DATETIME_PRECISION,
r.CHARACTER_SET_NAME,
r.COLLATION_NAME,
r.DTD_IDENTIFIER,
r.ROUTINE_BODY,
r.ROUTINE_DEFINITION,
r.EXTERNAL_NAME,
r.EXTERNAL_LANGUAGE,
r.PARAMETER_STYLE,
r.IS_DETERMINISTIC

""", 
    # --------------------------------
    # trigger
    # --------------------------------
    "trigger": 
"""select 
 

t.TRIGGER_CATALOG,
t.TRIGGER_SCHEMA,
t.TRIGGER_NAME,
t.EVENT_MANIPULATION,
t.EVENT_OBJECT_CATALOG,
t.EVENT_OBJECT_SCHEMA,
t.EVENT_OBJECT_TABLE,
t.ACTION_ORDER,
t.ACTION_CONDITION,
t.ACTION_ORIENTATION,
t.ACTION_TIMING,
t.ACTION_REFERENCE_OLD_TABLE,
t.ACTION_REFERENCE_NEW_TABLE,
t.ACTION_REFERENCE_OLD_ROW,
t.ACTION_REFERENCE_NEW_ROW, 

t.ACTION_STATEMENT

from information_schema.triggers t

where t.trigger_schema = %schema_name

order by 
t.TRIGGER_CATALOG,
t.TRIGGER_SCHEMA,
t.TRIGGER_NAME,
t.EVENT_MANIPULATION,
t.EVENT_OBJECT_CATALOG,
t.EVENT_OBJECT_SCHEMA,
t.EVENT_OBJECT_TABLE,
t.ACTION_ORDER,
t.ACTION_CONDITION,
t.ACTION_ORIENTATION,
t.ACTION_TIMING,
t.ACTION_REFERENCE_OLD_TABLE,
t.ACTION_REFERENCE_NEW_TABLE,
t.ACTION_REFERENCE_OLD_ROW,
t.ACTION_REFERENCE_NEW_ROW
""", 
    # --------------------------------
    # view
    # --------------------------------
    "view": 
"""select 
 
v.TABLE_CATALOG,
v.TABLE_SCHEMA,
v.TABLE_NAME,
v.VIEW_DEFINITION,
v.CHECK_OPTION,
v.IS_UPDATABLE
from information_schema.views v
where v.table_schema = %schema_name
and v.table_name not like '\_\_%'
 
order by 
v.TABLE_CATALOG,
v.TABLE_SCHEMA,
v.TABLE_NAME,
v.VIEW_DEFINITION,
v.CHECK_OPTION,
v.IS_UPDATABLE
""", 
    # --------------------------------
    # sample table, which affect the application logic
    # --------------------------------
    "customers":
    """select 
customerNumber, 
customerName 
from customers
order by 
customerNumber, 
customerName
"""
}
    
 
# --------------------------------------
# readme
# --------------------------------------

# Install mysql
# docker run --name mac-mysql2 --network my-network -e MYSQL_ROOT_PASSWORD=1234 -d  -p 3306:3306 mysql:latest 
 
# install adminer 
# docker run --network my-network -d  --name mac-adminer --link mac-mysql2:db -p 8080:8080 adminer
# browser http://localhosta:8080
# enter database=mac-mysql2, user=root, password=1234


# install python virtual environment
# python3 -m venv venv
# source venv/bin/activate
# pip install mysql-connector-python
# deactivate



 

