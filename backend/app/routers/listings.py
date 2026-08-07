from fastapi import APIRouter, Depends, HTTPException, status
from mysql.connector import Error as MySQLError
from typing import Dict
from app.database import get_db
from app.schemas import ListingBulkIn

router = APIRouter(prefix="/api/listings", tags=["listings"])

@router.post("/bulk", status_code=status.HTTP_201_CREATED)
def bulk_insert_listings(data: ListingBulkIn, db = Depends(get_db)) -> Dict[str, int]:
    """
    Bulk inserts a list of business listings into the MySQL database.
    """
    # 1. Validation: Return 422 if listings array is empty
    if not data.listings:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The listings list cannot be empty. At least one business listing must be provided."
        )

    # Convert Pydantic objects to tuple representation for executemany
    records = []
    for item in data.listings:
        # Normalize fields: Empty strings for optional fields phone/address should remain empty or None
        address = item.address.strip() if item.address else None
        phone = item.phone.strip() if item.phone else None
        
        records.append((
            item.business_name,
            item.category,
            item.city,
            address,
            phone,
            item.source
        ))

    # 2. Database transaction execution
    cursor = db.cursor()
    try:
        insert_query = """
        INSERT INTO listing_master (
            business_name, category, city, address, phone, source
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, records)
        db.commit()
        
        inserted_count = cursor.rowcount
        return {"inserted_rows": inserted_count}
        
    except MySQLError as err:
        # Rollback connection in case of database exception
        try:
            db.rollback()
        except Exception:
            pass
        # 3. Error Handling: return a generic 500 status (no raw DB secrets/errors)
        # Log locally (simulated print for this task)
        print(f"[ERROR] Database error during bulk insert: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while inserting data into the database. Please try again later."
        )
    finally:
        cursor.close()
