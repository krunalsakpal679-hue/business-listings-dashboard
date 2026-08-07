import csv
import json
import os
import random
from faker import Faker

def generate_listings(count=550):
    # Initialize Faker with Indian locale
    fake = Faker('en_IN')
    
    # Define our constraints
    categories = [
        "restaurants", "salons", "electricians", "gyms", 
        "clinics", "grocery stores", "tutors", "plumbers"
    ]
    cities = [
        "Mumbai", "Delhi", "Bengaluru", "Pune", 
        "Hyderabad", "Chennai", "Kolkata", "Ahmedabad"
    ]
    sources = ["Google", "Justdial", "Sulekha"]
    
    # Naming patterns for realism
    name_templates = {
        "restaurants": [
            lambda: f"{fake.last_name()} Kitchen",
            lambda: f"{random.choice(cities)} Spice",
            lambda: "The Golden Curry",
            lambda: f"{fake.first_name()}'s Bistro",
            lambda: "Tandoori Nights",
            lambda: "Royal Darbar",
            lambda: "Flavors of India"
        ],
        "salons": [
            lambda: f"{fake.first_name()}'s Unisex Salon",
            lambda: "Glow & Style",
            lambda: "Shine Beauty Parlour",
            lambda: f"{fake.last_name()} Hair Studio",
            lambda: "Scissors & Comb"
        ],
        "electricians": [
            lambda: f"{fake.last_name()} Electricals",
            lambda: "Sparky Electric Services",
            lambda: f"{fake.first_name()} Electric",
            lambda: "Volt Power Solutions",
            lambda: "Bright Light Electricals"
        ],
        "gyms": [
            lambda: f"{random.choice(cities)} Fitness Club",
            lambda: "Iron & Sweat Gym",
            lambda: "FitLife Studio",
            lambda: f"{fake.last_name()} Gym & Fitness",
            lambda: "Gold's Fitness Hub"
        ],
        "clinics": [
            lambda: f"{fake.last_name()} Clinic",
            lambda: f"Dr. {fake.first_name()}'s Clinic",
            lambda: f"{random.choice(cities)} Health Center",
            lambda: "Care & Cure Clinic",
            lambda: "Arogya Medical Centre"
        ],
        "grocery stores": [
            lambda: f"{fake.last_name()} Kirana Store",
            lambda: f"{random.choice(cities)} Supermarket",
            lambda: "Daily Needs Grocery",
            lambda: f"{fake.first_name()} Mart",
            lambda: "Apna Bazar"
        ],
        "tutors": [
            lambda: f"{fake.last_name()} Coaching Classes",
            lambda: "Alpha Tutorials",
            lambda: "Bright Future Academy",
            lambda: f"{fake.first_name()}'s Academy",
            lambda: "Elite Tutorials"
        ],
        "plumbers": [
            lambda: f"{fake.last_name()} Plumbers",
            lambda: "QuickFix Plumbing",
            lambda: "FlowRight Plumber Services",
            lambda: f"{fake.first_name()} Plumbing",
            lambda: "Tap & Pipe Solutions"
        ]
    }
    
    listings = []
    
    # We want a fairly even split across categories and cities
    for i in range(count):
        category = categories[i % len(categories)]
        city = cities[i % len(cities)]
        
        # Generate realistic business name based on category
        business_name = random.choice(name_templates[category])()
        
        # 5% chance of empty address
        if random.random() < 0.05:
            address = ""
        else:
            address = fake.address().replace("\n", ", ")
            
        # 5% chance of empty phone number
        if random.random() < 0.05:
            phone = ""
        else:
            # Generate realistic Indian phone numbers (e.g. +91 98765 43210 or 022-24325432)
            if random.random() < 0.8:
                phone = f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"
            else:
                phone = f"0{random.randint(22, 80)}-{random.randint(20000000, 29999999)}"
                
        # Random source distribution (uniform)
        source = random.choice(sources)
        
        listings.append({
            "business_name": business_name,
            "category": category,
            "city": city,
            "address": address,
            "phone": phone,
            "source": source
        })
        
    # Shuffle list to mix cities/categories/sources naturally
    random.shuffle(listings)
    return listings

def save_to_csv(listings, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["business_name", "category", "city", "address", "phone", "source"])
        writer.writeheader()
        writer.writerows(listings)
    print(f"Saved {len(listings)} listings to CSV: {filepath}")

def save_to_json(listings, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode='w', encoding='utf-8') as f:
        json.dump(listings, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(listings)} listings to JSON: {filepath}")

if __name__ == "__main__":
    data = generate_listings(550)
    
    # Save in the database directory
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../database/listings_seed.csv"))
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../database/listings_seed.json"))
    
    save_to_csv(data, csv_path)
    save_to_json(data, json_path)
