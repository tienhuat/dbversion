from mssql_dbversion import Dbversion

dbversion = Dbversion(host = "localhost",    
    user = "sa",
    database="northwind", 
    schema="dbo", 
    password = "134Gblsdklsiekkl")
report = dbversion.get_dbversion_report()
hash =  dbversion.calculate_hash(report)

with open("dbversion_report.txt", 'w', newline='') as file:
    file.write(report)

with open("dbversion_hash.txt", 'w', newline='') as file:
    file.write(hash)

pass

