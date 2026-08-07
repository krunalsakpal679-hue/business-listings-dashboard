# Business Listings Dashboard

A full-stack business listings dashboard.

## Tech Stack
- **Frontend**: React.js (Vite, Javascript)
- **Backend**: FastAPI (Python)
- **Database**: MySQL

## Folder Structure
```text
/backend
  /app
    /routers
    /models
    main.py
    database.py
    schemas.py
  requirements.txt
  .env.example
/frontend
/database
/docs
README.md
.gitignore
```

## Features
- **Data Seeding**: Seeding of 550 mock Indian business listings across 8 cities and 8 categories.
- **FastAPI API Layer**: Bulk insert endpoint and grouped analytics for city-wise, category-wise, and source-wise listings.
- **Interactive UI**: Elegant dark mode dashboard showing metrics summary cards and responsive Recharts representations (Bar/Pie/Horizontal Bar charts) with error handling and retry mechanisms.
