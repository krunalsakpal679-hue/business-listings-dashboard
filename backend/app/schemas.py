from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ListingIn(BaseModel):
    business_name: str = Field(..., min_length=1, description="Name of the business")
    category: str = Field(..., min_length=1, description="Category of listing")
    city: str = Field(..., min_length=1, description="City location")
    address: Optional[str] = Field(default="", description="Postal address")
    phone: Optional[str] = Field(default="", description="Contact phone number")
    source: str = Field(..., min_length=1, description="Data source name")

    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "Taj Mahal Palace Restaurant",
                "category": "restaurants",
                "city": "Mumbai",
                "address": "Apollo Bandar, Colaba, Mumbai, Maharashtra 400001",
                "phone": "+91 22 6665 3366",
                "source": "Google"
            }
        }

class ListingBulkIn(BaseModel):
    listings: List[ListingIn] = Field(..., description="List of business listings to bulk insert")

    class Config:
        json_schema_extra = {
            "example": {
                "listings": [
                    {
                        "business_name": "Quick Spark Electricians",
                        "category": "electricians",
                        "city": "Bengaluru",
                        "address": "12 Main St, Indiranagar",
                        "phone": "+91 98765 43210",
                        "source": "Sulekha"
                    },
                    {
                        "business_name": "Daily Needs Store",
                        "category": "grocery stores",
                        "city": "Delhi",
                        "address": "Block C, Connaught Place",
                        "phone": "+91 91234 56789",
                        "source": "Justdial"
                    }
                ]
            }
        }

class ListingOut(BaseModel):
    id: int
    business_name: str
    category: str
    city: str
    address: Optional[str] = ""
    phone: Optional[str] = ""
    source: str
    created_at: datetime

    class Config:
        from_attributes = True

class CountResult(BaseModel):
    label: str = Field(..., description="The classification label (e.g. city, category, source name)")
    count: int = Field(..., description="The count of records matching this label")

    class Config:
        from_attributes = True
