import pyodbc

import hashlib
import json


class Dbversion:
   
    # Constructor to initialize instance variables
    def __init__(self, host, database, schema, user, password):
        self.host = host      
        self.database = database
        self.schema = schema
        self.user = user
        self.password = password

    
    def get_dbversion_report(self):
        
        report = ""

        try:
          
            print("connection starting")
            connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + \
                self.host+';DATABASE='+self.database+';UID='+self.user+';PWD=' + self.password
            
            connection =  pyodbc.connect(connectionString)

            print("connection successful")

            cursor = connection.cursor()

         

            for queryName, queryStatement in self.sqls.items():   

                queryStatement = queryStatement.replace("%schema_name", "'" + self.schema + "' ")

                cursor.execute(queryStatement)
              
                rows = cursor.fetchall()

                print("fetching " + queryName )
                
                report = report + "--------------------------------------------" + "\r\n"
                report = report + queryName +  "\r\n"
                report = report + "--------------------------------------------" + "\r\n"
    
                report = report + self.to_json(cursor, rows) + "\r\n" 
                report = report + "\r\n\r\n"
            
            report = report.strip()          
        except Exception as e:
            print("Error while connecting to MS SQL", e)
            pass
        

        return report

    
    def calculate_hash(self, text):
        # Create a new hash object using the specified algorithm
        algorithm='sha1'
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
sc.DEFAULT_CHARACTER_SET_CATALOG,
sc.DEFAULT_CHARACTER_SET_SCHEMA,
sc.DEFAULT_CHARACTER_SET_NAME

from information_schema.schemata sc
where sc.schema_name = %schema_name

order by 
sc.CATALOG_NAME,
sc.SCHEMA_NAME,
sc.DEFAULT_CHARACTER_SET_CATALOG,
sc.DEFAULT_CHARACTER_SET_SCHEMA,
sc.DEFAULT_CHARACTER_SET_NAME

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
  t.TABLE_TYPE
FROM 
    INFORMATION_SCHEMA.tables  t
where t.table_schema = %schema_name
and t.table_name  not like '[_][_]%'
order by 
  t.TABLE_CATALOG, 
  t.TABLE_SCHEMA, 
  t.TABLE_NAME, 
  t.TABLE_TYPE
""", 
    
    # --------------------------------
    # column
    # --------------------------------
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
    c.CHARACTER_SET_SCHEMA,
    c.CHARACTER_SET_NAME,
    c.COLLATION_CATALOG, 
    c.COLLATION_SCHEMA,
    c.COLLATION_NAME  

FROM INFORMATION_SCHEMA.COLUMNS c 
WHERE 
    c.TABLE_SCHEMA = %schema_name
    and c.table_name not like '[_][_]%'
    and c.column_name not like '[_][_]%'

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
    c.CHARACTER_SET_SCHEMA,
    c.CHARACTER_SET_NAME,
    c.COLLATION_CATALOG, 
    c.COLLATION_SCHEMA,
    c.COLLATION_NAME
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
  tc.CONSTRAINT_TYPE
FROM  
  INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc   
where tc.table_schema = %schema_name
and tc.table_name not like '[_][_]%'
order by 
tc.CONSTRAINT_CATALOG, 
  tc.table_schema, 
  tc.table_name, 
  tc.CONSTRAINT_NAME, 
  tc.CONSTRAINT_TYPE
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
  cu.CONSTRAINT_SCHEMA, 
  cu.constraint_name, 

  cu.TABLE_CATALOG, 
  cu.TABLE_SCHEMA, 
  cu.TABLE_NAME,   
  cu.COLUMN_NAME

from INFORMATION_SCHEMA.KEY_COLUMN_USAGE cu
where cu.CONSTRAINT_SCHEMA = %schema_name
and cu.TABLE_NAME not like '[_][_]%'
and cu.COLUMN_NAME not like '[_][_]%'
order by 
  cu.CONSTRAINT_CATALOG, 
  cu.CONSTRAINT_SCHEMA, 
  cu.constraint_name, 

  cu.TABLE_CATALOG, 
  cu.TABLE_SCHEMA, 
  cu.TABLE_NAME,   
  cu.COLUMN_NAME
""", 
    
    # --------------------------------
    # stored proc and function
    # --------------------------------
    "routine": 
"""select 
distinct
r.SPECIFIC_CATALOG,
r.SPECIFIC_SCHEMA,
r.SPECIFIC_NAME,
r.ROUTINE_CATALOG,
r.ROUTINE_SCHEMA,
r.ROUTINE_NAME,
r.ROUTINE_TYPE,
r.DATA_TYPE,
r.CHARACTER_MAXIMUM_LENGTH,
r.CHARACTER_OCTET_LENGTH,
r.COLLATION_NAME,
r.CHARACTER_SET_NAME,
r.NUMERIC_PRECISION,
r.NUMERIC_PRECISION_RADIX,
r.NUMERIC_SCALE,
r.DATETIME_PRECISION,
r.ROUTINE_BODY,
r.ROUTINE_DEFINITION,
r.IS_DETERMINISTIC,
r.SQL_DATA_ACCESS

from information_schema.routines r
where r.ROUTINE_SCHEMA = %schema_name

order by 
r.SPECIFIC_CATALOG,
r.SPECIFIC_SCHEMA,
r.SPECIFIC_NAME,
r.ROUTINE_CATALOG,
r.ROUTINE_SCHEMA,
r.ROUTINE_NAME,
r.ROUTINE_TYPE,
r.DATA_TYPE,
r.CHARACTER_MAXIMUM_LENGTH,
r.CHARACTER_OCTET_LENGTH,
r.COLLATION_NAME,
r.CHARACTER_SET_NAME,
r.NUMERIC_PRECISION,
r.NUMERIC_PRECISION_RADIX,
r.NUMERIC_SCALE,
r.DATETIME_PRECISION,
r.ROUTINE_BODY,
r.ROUTINE_DEFINITION,
r.IS_DETERMINISTIC,
r.SQL_DATA_ACCESS

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
and v.table_name not like '[_][_]%'
 
order by 
v.TABLE_CATALOG,
v.TABLE_SCHEMA,
v.TABLE_NAME,
v.VIEW_DEFINITION,
v.CHECK_OPTION,
v.IS_UPDATABLE
""", 

    # --------------------------------
    # routine columns
    # --------------------------------
    "routine columns":
    """
select 
rc.TABLE_CATALOG,
rc.TABLE_SCHEMA,
rc.TABLE_NAME,
rc.COLUMN_NAME,
rc.COLUMN_DEFAULT,
rc.IS_NULLABLE,
rc.DATA_TYPE,
rc.CHARACTER_MAXIMUM_LENGTH,
rc.CHARACTER_OCTET_LENGTH,
rc.NUMERIC_PRECISION,
rc.NUMERIC_PRECISION_RADIX,
rc.NUMERIC_SCALE,
rc.DATETIME_PRECISION,
rc.CHARACTER_SET_CATALOG,
rc.CHARACTER_SET_NAME,
rc.COLLATION_NAME,
rc.DOMAIN_CATALOG,
rc.DOMAIN_SCHEMA,
rc.DOMAIN_NAME
from information_schema.ROUTINE_COLUMNS rc
where rc.TABLE_SCHEMA = %schema_name
and rc.table_name  not like '[_][_]%'
and rc.column_name  not like '[_][_]%'

order by 
rc.TABLE_CATALOG,
rc.TABLE_SCHEMA,
rc.TABLE_NAME,
rc.COLUMN_NAME,
rc.COLUMN_DEFAULT,
rc.IS_NULLABLE,
rc.DATA_TYPE,
rc.CHARACTER_MAXIMUM_LENGTH,
rc.CHARACTER_OCTET_LENGTH,
rc.NUMERIC_PRECISION,
rc.NUMERIC_PRECISION_RADIX,
rc.NUMERIC_SCALE,
rc.DATETIME_PRECISION,
rc.CHARACTER_SET_CATALOG,
rc.CHARACTER_SET_NAME,
rc.COLLATION_NAME,
rc.DOMAIN_CATALOG,
rc.DOMAIN_SCHEMA,
rc.DOMAIN_NAME
""", 

    # --------------------------------
    # Contraint column usage
    # --------------------------------
    "constraint column usage":
    """select 
distinct
ccu.TABLE_CATALOG,
ccu.TABLE_SCHEMA,
ccu.TABLE_NAME,
ccu.COLUMN_NAME,
ccu.CONSTRAINT_CATALOG,
ccu.CONSTRAINT_SCHEMA,
ccu.CONSTRAINT_NAME
from information_schema.CONSTRAINT_COLUMN_USAGE ccu
where ccu.TABLE_SCHEMA = %schema_name
and ccu.table_name  not like '[_][_]%'
and ccu.column_name  not like '[_][_]%'

order by 
ccu.TABLE_CATALOG,
ccu.TABLE_SCHEMA,
ccu.TABLE_NAME,
ccu.COLUMN_NAME,
ccu.CONSTRAINT_CATALOG,
ccu.CONSTRAINT_SCHEMA,
ccu.CONSTRAINT_NAME
""",

    # --------------------------------
    # Contraint table usage
    # --------------------------------
    "constraint table usage":
    """select
distinct
ctu.TABLE_CATALOG,
ctu.TABLE_SCHEMA,
ctu.TABLE_NAME,
ctu.CONSTRAINT_CATALOG,
ctu.CONSTRAINT_SCHEMA,
ctu.CONSTRAINT_NAME
from INFORMATION_SCHEMA.CONSTRAINT_TABLE_USAGE ctu
where ctu.TABLE_NAME = %schema_name
and ctu.table_name  not like '[_][_]%'

order by
ctu.TABLE_CATALOG,
ctu.TABLE_SCHEMA,
ctu.TABLE_NAME,
ctu.CONSTRAINT_CATALOG,
ctu.CONSTRAINT_SCHEMA,
ctu.CONSTRAINT_NAME
""",

    # --------------------------------
    # View column usage
    # --------------------------------
    "view column usage":
    """select
distinct
vcu.VIEW_CATALOG,
vcu.VIEW_SCHEMA,
vcu.VIEW_NAME,
vcu.TABLE_CATALOG,
vcu.TABLE_SCHEMA,
vcu.TABLE_NAME,
vcu.COLUMN_NAME
from INFORMATION_SCHEMA.VIEW_COLUMN_USAGE vcu
where vcu.TABLE_SCHEMA = %schema_name
and vcu.table_name  not like '[_][_]%'
and vcu.column_name  not like '[_][_]%'

order by 
vcu.VIEW_CATALOG,
vcu.VIEW_SCHEMA,
vcu.VIEW_NAME,
vcu.TABLE_CATALOG,
vcu.TABLE_SCHEMA,
vcu.TABLE_NAME,
vcu.COLUMN_NAME

""",


    # --------------------------------
    # Domains
    # --------------------------------
    "domains":
    """select
distinct
d.DOMAIN_CATALOG,
d.DOMAIN_SCHEMA,
d.DOMAIN_NAME,
d.DATA_TYPE,
d.CHARACTER_MAXIMUM_LENGTH,
d.CHARACTER_OCTET_LENGTH,
d.COLLATION_NAME,
d.CHARACTER_SET_CATALOG,
d.CHARACTER_SET_NAME,
d.NUMERIC_PRECISION,
d.NUMERIC_PRECISION_RADIX,
d.NUMERIC_SCALE,
d.DATETIME_PRECISION,
d.DOMAIN_DEFAULT

from INFORMATION_SCHEMA.DOMAINS d
where d.DOMAIN_SCHEMA = %schema_name

order by 
d.DOMAIN_CATALOG,
d.DOMAIN_SCHEMA,
d.DOMAIN_NAME,
d.DATA_TYPE,
d.CHARACTER_MAXIMUM_LENGTH,
d.CHARACTER_OCTET_LENGTH,
d.COLLATION_NAME,
d.CHARACTER_SET_CATALOG,
d.CHARACTER_SET_NAME,
d.NUMERIC_PRECISION,
d.NUMERIC_PRECISION_RADIX,
d.NUMERIC_SCALE,
d.DATETIME_PRECISION,
d.DOMAIN_DEFAULT
""",


    # --------------------------------
    # Domains constraint
    # --------------------------------
    "domains constraint":
    """select 
distinct
dc.CONSTRAINT_CATALOG,
dc.CONSTRAINT_SCHEMA,
dc.CONSTRAINT_NAME,
dc.DOMAIN_CATALOG,
dc.DOMAIN_SCHEMA,
dc.DOMAIN_NAME

from INFORMATION_SCHEMA.DOMAIN_CONSTRAINTS dc
where dc.CONSTRAINT_SCHEMA = %schema_name

order by
dc.CONSTRAINT_CATALOG,
dc.CONSTRAINT_SCHEMA,
dc.CONSTRAINT_NAME,
dc.DOMAIN_CATALOG,
dc.DOMAIN_SCHEMA,
dc.DOMAIN_NAME
""",

    # --------------------------------
    # Column domain usage
    # --------------------------------
    "column domain usage":
    """select 
distinct
cdu.DOMAIN_CATALOG,
cdu.DOMAIN_SCHEMA,
cdu.DOMAIN_NAME,
cdu.TABLE_CATALOG,
cdu.TABLE_SCHEMA,
cdu.TABLE_NAME,
cdu.COLUMN_NAME

from INFORMATION_SCHEMA.COLUMN_DOMAIN_USAGE cdu
where cdu.TABLE_SCHEMA = %schema_name
and cdu.table_name  not like '[_][_]%'
and cdu.column_name  not like '[_][_]%'

order by 
cdu.DOMAIN_CATALOG,
cdu.DOMAIN_SCHEMA,
cdu.DOMAIN_NAME,
cdu.TABLE_CATALOG,
cdu.TABLE_SCHEMA,
cdu.TABLE_NAME,
cdu.COLUMN_NAME

""",

    # --------------------------------
    # view table usage
    # --------------------------------
    "view table usage":
    """select
distinct
vtu.VIEW_CATALOG,
vtu.VIEW_SCHEMA,
vtu.VIEW_NAME,
vtu.TABLE_CATALOG,
vtu.TABLE_SCHEMA,
vtu.TABLE_NAME

from INFORMATION_SCHEMA.VIEW_TABLE_USAGE vtu
where vtu.TABLE_SCHEMA = %schema_name
and vtu.table_name  not like '[_][_]%'

order by 
vtu.VIEW_CATALOG,
vtu.VIEW_SCHEMA,
vtu.VIEW_NAME,
vtu.TABLE_CATALOG,
vtu.TABLE_SCHEMA,
vtu.TABLE_NAME

""",

    # --------------------------------
    # sample table, which affect the application logic
    # --------------------------------
    "customers":
    """select 
c.CategoryID, 
c.CategoryName
from Categories c
order by 
c.CategoryID, 
c.CategoryName
"""
}
    
 
# --------------------------------------
# readme
# --------------------------------------

# Install mysql
# docker run --name mac-mysql2 --network my-network -e MYSQL_ROOT_PASSWORD=1234 -d mysql:latest
 
# install adminer 
# docker run --network my-network -d  --name mac-adminer --link mac-mysql:db -p 8080:8080 adminer
# browser http://localhosta:8080
# enter database=mac-mysql2, user=root, password=1234


# install python virtual environment
# python3 -m venv venv
# source venv/bin/activate
# pip install pip install pymssql
# deactivate



 

