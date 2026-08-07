# Business Listings Dashboard

The **Business Listings Dashboard** is a full-stack, data-driven web application designed to collect, store, aggregate, and visualize local business listings. It provides real-time marketplace insights by analyzing business counts classified by cities, domains/categories, and source directories. The system features a robust FastAPI backend with connection pooling, a local MySQL database storage layer containing 550+ seeded records, and a high-performance React dashboard styled with premium glassmorphism and modern Recharts representations.

---

## Tech Stack
*   **Frontend**: React.js (Vite, JavaScript), Axios (API requests), Recharts (data visualization).
*   **Backend**: FastAPI (Python), Uvicorn (ASGI server), Pydantic (data contracts), `python-dotenv` (config).
*   **Database**: MySQL, `mysql-connector-python` (database connection & pool driver).
*   **Data Collection & Tooling**: Faker (mock seed generator), BeautifulSoup4 (scraping proof-of-concept), Git (version control).

---

## Folder Structure
```text
/backend
  /app
    /routers
      dashboard.py          # GET dashboard aggregation endpoints
      listings.py           # POST bulk listing endpoint
    /models
      __init__.py           # Package marker for models
    main.py                 # FastAPI application and CORS wireframe
    database.py             # Connection pooling configurations and dependencies
    schemas.py              # Pydantic models for request/response validation
  /scripts
    generate_mock_data.py   # Seeding generator (Faker)
    scrape_sample.py        # Compliance scraper POC (BeautifulSoup)
    load_seed_data.py       # SQL bulk loader (executemany)
  requirements.txt          # Python dependencies
  .env.example              # Shell configuration variables layout
/database
  schema.sql                # DDL database schema build
  listing_master_dump.sql   # Complete database dump (schema + data)
  listings_seed.csv         # Generated seed records (CSV)
  listings_seed.json        # Generated seed records (JSON)
/frontend
  /public
  /src
    /api
      api.js                # Axios client configurations
    /components
      CityChart.jsx         # BarChart component (cities)
      CategoryChart.jsx     # Donut Chart component (categories)
      SourceChart.jsx       # Horizontal BarChart component (sources)
    App.jsx                 # Dashboard shell and overall metrics
    App.css                 # Premium CSS UI styles
    main.jsx                # Entrypoint file
/docs
  scraping_approach.md      # Data collection approach documentation
  demo_video_script.md      # Demo video timeline outline script
README.md
.gitignore
```

---

## Setup Instructions

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/krunalsakpal679-hue/business-listings-dashboard.git
cd business-listings-dashboard
```

### 2. Configure the Database
Execute the database schema setup to create the database, tables, and optimized indexes:
```bash
mysql -u root -p < database/schema.sql
```

### 3. Setup the Backend Environment
Navigate to the backend directory, initialize a Python virtual environment, and install dependencies:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Backend Environment Variables
Create your local `.env` configuration:
```bash
copy .env.example .env
```
Open `.env` and fill in your local MySQL credentials:
```ini
PORT=8000
HOST=0.0.0.0
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=business_listings_db
```

### 5. Load Seed Data
Seed all 550 generated business listings into MySQL:
```bash
python scripts/load_seed_data.py
```

### 6. Start the Backend API Server
Start the Uvicorn development server:
```bash
uvicorn app.main:app --reload
```
*The API is now running at `http://localhost:8000` (Swagger docs available at `http://localhost:8000/docs`).*

### 7. Setup & Run the Frontend
In a new terminal window, navigate to the frontend directory, install npm packages, and start the Vite server:
```bash
cd frontend
npm install
npm run dev
```
*The dashboard interface is now running at `http://localhost:5173/`.*

---

## API Reference

### 1. Bulk Insert Listings
*   **Endpoint**: `POST /api/listings/bulk`
*   **Description**: Bulk inserts listings into the database. Returns a `422` if empty.
*   **Example Request Body**:
    ```json
    {
      "listings": [
        {
          "business_name": "Deepmind Kitchen",
          "category": "restaurants",
          "city": "Bengaluru",
          "address": "500 AI Lane",
          "phone": "+91 88888 77777",
          "source": "Justdial"
        }
      ]
    }
    ```
*   **Example Response (Status 201 Created)**:
    ```json
    {
      "inserted_rows": 1
    }
    ```

### 2. City-wise Aggregation
*   **Endpoint**: `GET /api/dashboard/city-wise`
*   **Description**: Returns business listing volumes grouped by city, sorted descending.
*   **Example Response (Status 200 OK)**:
    ```json
    [
      {
        "label": "Bengaluru",
        "count": 70
      },
      {
        "label": "Mumbai",
        "count": 70
      }
    ]
    ```

### 3. Category-wise Aggregation
*   **Endpoint**: `GET /api/dashboard/category-wise`
*   **Description**: Returns business listing volumes grouped by category, sorted descending.
*   **Example Response (Status 200 OK)**:
    ```json
    [
      {
        "label": "restaurants",
        "count": 70
      },
      {
        "label": "clinics",
        "count": 69
      }
    ]
    ```

### 4. Source-wise Aggregation
*   **Endpoint**: `GET /api/dashboard/source-wise`
*   **Description**: Returns listing volumes grouped by directory source, sorted descending.
*   **Example Response (Status 200 OK)**:
    ```json
    [
      {
        "label": "Justdial",
        "count": 189
      },
      {
        "label": "Sulekha",
        "count": 183
      }
    ]
    ```

---

## Data Collection Approach

The data pipeline utilizes a dual approach:
1.  **Seed Data**: We generated a deterministic dataset of **550** realistic Indian business listings using the `Faker` library. Key fields (`business_name`, `category`, `city`, `source`) are guaranteed to be fully populated, while optional fields (`phone`, `address`) include a simulated 5% null/blank rate to test schema resilience and UI handling.
2.  **Safety-First Web Scraper**: We implemented a proof-of-concept scraper (`scrape_sample.py`) using `requests` and `BeautifulSoup`. The scraper evaluates target `robots.txt` rules using `urllib.robotparser`. If access is disallowed (as is the case with most production directories like YellowPages), the script logs the rule violation and exits gracefully instead of violating policies or getting blocked.
3.  **Production Migration Path**: In production, the system can seamlessly transition to the official **Google Places API** by utilizing queries (e.g. `query="gyms in Mumbai"`), resolving paginated results, and caching records inside our MySQL cache layer to avoid redundant API fees.

*For more details, see [docs/scraping_approach.md](file:///c:/Internship/docs/scraping_approach.md).*

---

## Challenges Faced & Solutions

### 1. Compliant Web Scraping
*   **Challenge**: Major directories (YellowPages, Justdial) protect their listing details and block scraper queries in their `robots.txt` user-agent rules.
*   **Solution**: Implemented a checking module in `scrape_sample.py` using `urllib.robotparser` to inspect rules first. If forbidden, it exits gracefully with code `0` rather than attempting a bypass.

### 2. MySQL Idempotent Database Migrations
*   **Challenge**: Re-running the database initialization script (`schema.sql`) failed with duplicate key name errors because MySQL does not natively support `CREATE INDEX IF NOT EXISTS` on standard tables.
*   **Solution**: Modified `schema.sql` to drop the tables prior to creation (`DROP TABLE IF EXISTS listing_master`), ensuring the schema script runs idempotently.

### 3. Vite Compiler Parse Errors
*   **Challenge**: During the bundling phase, the Vite bundler failed with parse errors on inline comments using `#` inside `CategoryChart.jsx` and `SourceChart.jsx` arrays.
*   **Solution**: Refactored the React files to use standard JavaScript comments (`//`) instead of Python comments (`#`).

---

## Dashboard Screenshots

*Placeholder for dashboard screenshot - Desktop view*
<!-- TODO: Insert Desktop Screenshot Here -->

*Placeholder for dashboard screenshot - Mobile stacked view*
<!-- TODO: Insert Mobile Screenshot Here -->
