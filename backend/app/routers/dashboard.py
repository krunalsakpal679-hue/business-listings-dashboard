from fastapi import APIRouter, Depends, HTTPException, status
from mysql.connector import Error as MySQLError
from typing import List
from app.database import get_db
from app.schemas import CountResult

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

def execute_aggregation_query(db, column_name: str) -> List[CountResult]:
    """
    Helper function to safely execute classification count queries and map them to CountResult.
    """
    cursor = db.cursor()
    # Safely insert the column name (not user input, so safe from SQL injection)
    query = f"""
    SELECT {column_name} AS label, COUNT(*) AS count 
    FROM listing_master 
    GROUP BY {column_name} 
    ORDER BY count DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            # Map row: row[0] is label (str), row[1] is count (int)
            label_val = str(row[0]) if row[0] is not None else "Unknown"
            results.append(CountResult(label=label_val, count=row[1]))
            
        return results
        
    except MySQLError as err:
        print(f"[ERROR] Database error during aggregation on {column_name}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while compiling dashboard metrics. Please try again later."
        )
    finally:
        cursor.close()

@router.get("/city-wise", response_model=List[CountResult])
def get_city_wise_counts(db = Depends(get_db)):
    """
    Returns counts of listings grouped by city, ordered by count descending.
    """
    return execute_aggregation_query(db, "city")

@router.get("/category-wise", response_model=List[CountResult])
def get_category_wise_counts(db = Depends(get_db)):
    """
    Returns counts of listings grouped by category, ordered by count descending.
    """
    return execute_aggregation_query(db, "category")

@router.get("/source-wise", response_model=List[CountResult])
def get_source_wise_counts(db = Depends(get_db)):
    """
    Returns counts of listings grouped by data source, ordered by count descending.
    """
    return execute_aggregation_query(db, "source")
