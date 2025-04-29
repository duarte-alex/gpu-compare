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
        password=db_pass)
    
    cursor = conn.cursor()

    for gpu in gpu_data:
        cursor.execute("""
            INSERT INTO gpus (type, provider, region, price, carbon_intensity, efficiency)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            gpu["type"],
            gpu["provider"],
            gpu["region"],
            gpu["price"],
            gpu["carbonIntensity"],
            gpu["efficiency"]
        ))

    # Commit the transaction.
    conn.commit()

    # Query the table to verify the inserted rows.
    #cursor.execute("SELECT * FROM gpus;")
    #rows = cursor.fetchall()
    #print("Rows in gpus table:", rows)

    #cursor.close()
    #conn.close()

if __name__ == "__main__":

    # keys: type, provider, region, price, carbonIntensity, efficiency
    gpus: list[dict] = [
  {"type": 'NVIDIA A100', "provider": 'AWS', "region": 'us-east-1', "price": 1, "carbonIntensity": 400, "efficiency": 'high' },
  {"type": 'NVIDIA P100', "provider": 'Google Cloud', "region": 'europe-west4', "price": 2, "carbonIntensity": 200, "efficiency": 'medium' },
  {"type": 'AMD MI250', "provider": 'Azure', "region": 'asia-southeast1', "price": 4, "carbonIntensity": 100, "efficiency": 'low' },
  {"type": 'NVIDIA A100', "provider": 'AWS', "region": 'us-east-1', "price": 6, "carbonIntensity": 150, "efficiency": 'high' },
  {"type": 'NVIDIA P100', "provider": 'Google Cloud', "region": 'europe-west4', "price": 8, "carbonIntensity": 220, "efficiency": 'medium' },
  {"type": 'AMD MI250', "provider": 'Azure', "region": 'asia-southeast1', "price": 3, "carbonIntensity": 300, "efficiency": 'low' },
  ]
    
store_gpus(gpus)