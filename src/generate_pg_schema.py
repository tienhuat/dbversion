# Use this script to generate SQL SELECT statements for all tables in a given PostgreSQL schema.
# This script connects to a PostgreSQL database and generates SQL SELECT statements for all tables
# in a specified schema.



import psycopg2


def generate_select_statements(schema_name):
    # Connection parameters
    conn = psycopg2.connect(
        dbname="northwind",
        user="admin",
        password="admin123",
        host="localhost",
        port="5432"  # default PostgreSQL port
    )
 
    
    cursor = conn.cursor()

    # Step 1: Get all tables in the schema
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s            
        ORDER BY table_name;
    """, (schema_name,))
    
    tables = cursor.fetchall()
    
    sql_statements = []

    # Step 2: For each table, get its columns and generate SQL
    for (table_name,) in tables:
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s
              AND table_name = %s
            ORDER BY ordinal_position;
        """, (schema_name, table_name))
        
        columns = cursor.fetchall()
        column_list = [f"c.{col[0]}" for col in columns]

        # Assemble the SQL
        select_clause = ", ".join(column_list)
        order_by_clause = ", ".join(column_list)
        
        sql = f"""SELECT {select_clause}
FROM {schema_name}.{table_name} c
ORDER BY {order_by_clause};"""

        sql_statements.append(sql)

    cursor.close()
    conn.close()

    return sql_statements

# Example usage
if __name__ == "__main__":
    schema = 'pg_catalog'  # or your specific schema
    selects = generate_select_statements(schema)
    index = 0; 
    sqls = ""
    for stmt in selects:
        sqls += f"\"{index}\":"        
        print(f"\"{index}\":")

        sqls += "\"" * 3
        print("\"" * 3) 

        sqls += stmt
        print(stmt)

        sqls += "\"" * 3
        print("\"" * 3)

        sqls += ", \n\n"
        print(", \n\n") 

        index += 1

    # save the sqls to a file
    with open("sql_statements.txt", "w") as f:
        f.write(sqls)
    print("SQL statements saved to sql_statements.txt")


