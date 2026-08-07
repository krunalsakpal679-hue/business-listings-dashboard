import os
import csv
import mysql.connector
from dotenv import load_dotenv

def load_seed_data():
    # Load environment variables
    # Go up one level to look for .env in the backend folder
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))
    load_dotenv(dotenv_path=env_path)
    
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "business_listings_db")
    db_port = os.getenv("DB_PORT", "3306")
    
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../database/listings_seed.csv"))
    
    print("Database Connection Details:")
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"User: {db_user}")
    print(f"Database: {db_name}")
    print(f"CSV Path: {csv_path}\n")
    
    if not os.path.exists(csv_path):
        print(f"Error: Seed file not found at {csv_path}")
        return
        
    # Read listings from CSV
    listings = []
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Map blank values to None (which translates to SQL NULL)
            address = row["address"] if row["address"].strip() != "" else None
            phone = row["phone"] if row["phone"].strip() != "" else None
            
            listings.append((
                row["business_name"],
                row["category"],
                row["city"],
                address,
                phone,
                row["source"]
            ))
            
    print(f"Parsed {len(listings)} listings from CSV. Connecting to database...")
    
    try:
        # Establish connection to MySQL
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=int(db_port)
        )
        cursor = conn.cursor()
        
        # Prepare bulk insert statement
        insert_query = """
        INSERT INTO listing_master (
            business_name, category, city, address, phone, source
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        print("Executing bulk insertion (executemany)...")
        # Run batch insertion for maximum performance
        cursor.executemany(insert_query, listings)
        conn.commit()
        
        print(f"Success! Inserted {cursor.rowcount} rows into table 'listing_master'.")
        
        # Verify total count
        cursor.execute("SELECT COUNT(*) FROM listing_master")
        total_rows = cursor.fetchone()[0]
        print(f"Current total rows in 'listing_master': {total_rows}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"General Error: {e}")

if __name__ == "__main__":
    load_seed_data()
