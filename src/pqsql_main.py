
from pgsql_dbversion import Dbversion
import time

dbversion = Dbversion(
    host="localhost",          # Since you're running PostgreSQL locally via Docker
    user="admin",              # Matches POSTGRES_USER in the docker-compose.yml
    database="northwind",      # Matches POSTGRES_DB in the docker-compose.yml
    schema="public",           # Default schema in PostgreSQL
    password="admin123"        # Matches POSTGRES_PASSWORD in the docker-compose.yml
)

# benchmark the time taken to get the database version
start_time = time.time()

report = dbversion.get_dbversion_report()
hash = dbversion.calculate_hash(report)

with open("dbversion_report.txt", 'w', newline='') as file:
    file.write(report)

with open("dbversion_hash.txt", 'w', newline='') as file:
    file.write(hash)

end_time = time.time()
print(f"Time taken to get database version: {end_time - start_time} seconds")


pass