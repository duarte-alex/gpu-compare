from dotenv import load_dotenv
import os
import psycopg2

def store_gpus(gpu_data: list[dict]):
    """
    Connects to the PostgreSQL database using environment variables,
    inserts GPU data into the 'gpus' table, and prints the table contents.
    """
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")

    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_pass
    )
    cursor = conn.cursor()

    # Insert each GPU record into the table.
    for gpu in gpu_data:
        cursor.execute("""
            INSERT INTO gpus (zone, gpu_name, description, max_cards_per_instance)
            VALUES (%s, %s, %s, %s)
        """, (
            gpu["Zone"],
            gpu["GPU_Name"],
            gpu["Description"],
            gpu["Max_Cards_Per_Instance"]
        ))
    
    # Commit the transaction.
    conn.commit()

    # Query the table to verify the inserted rows.
    cursor.execute("SELECT * FROM gpus;")
    rows = cursor.fetchall()
    print("Rows in gpus table:", rows)

    cursor.close()
    conn.close()