class Dbversion:
    def __init__(self, host, user, database, schema, password):
        import psycopg2
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            database=database,
            password=password
        )
        self.schema = schema

    def get_dbversion_report(self):
        cursor = self.connection.cursor()
        query = f"""
        SELECT * FROM Products  
        """
        cursor.execute(query)
        report = cursor.fetchall()
        cursor.close()
        return str(report)

    def calculate_hash(self, report):
        import hashlib
        return hashlib.sha256(report.encode()).hexdigest()

    def close_connection(self):
        self.connection.close()