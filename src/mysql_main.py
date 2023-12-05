from mysql_dbversion import Dbversion

dbversion = Dbversion(host = "localhost",    
    databasse="classicmodels",
    user = "root",
    password = "1234")
report = dbversion.get_dbversion_report()
hash =  dbversion.calculate_hash(report)

with open("dbversion_report.txt", 'w', newline="") as file:
    file.write(report)

with open("dbversion_hash.txt", 'w',  newline="") as file:
    file.write(hash)

pass
