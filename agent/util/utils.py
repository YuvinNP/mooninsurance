import pyodbc


def create_db_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=rds-mssql-db.cxoameg6ycbo.us-east-1.rds.amazonaws.com;PORT=1433;"
        "DATABASE=meditrack_db;"
        "UID=admin;PWD=admin123"
    )
    return conn


def get_patient_ids():
    conn = create_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT count(*) from patient.patient_details")
    patient_count = cur.fetchone()[0]
    conn.close()
    return patient_count
