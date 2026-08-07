# Demo Video Script Outline

This script provides a minute-by-minute guide for a 5-minute video demonstration of the Business Listings Dashboard project.

---

## ⏱️ Timeline & Segment Breakdown

### 🎬 0:00 - 1:00 | Project Overview & Data Collection Strategy
*   **Visual**: Show the screen capturing the repository workspace structure and open the `README.md`.
*   **Voiceover**:
    > "Welcome! Today, I'm presenting the Business Listings Dashboard, a full-stack platform built with React, FastAPI, and MySQL. 
    > Let's start with our data collection layer. Because production directories restrict automated access in their robots.txt rules, we implemented a dual approach: a mock generator script utilizing the Faker library to seed 550 realistic Indian business listings, and a safety-first sample web scraper.
    > The sample scraper parses and checks compliance boundaries before querying, which ensures we exit gracefully rather than violating terms.
    > If we open listings_seed.csv or JSON, we see high-integrity rows covering restaurants, gyms, and other categories across 8 Indian cities."

---

### ⚙️ 1:00 - 2:30 | Database Schema & API Swagger Live Demo
*   **Visual**: Switch to MySQL Workbench or CLI, show the `DESCRIBE listing_master;` table and queries. Then, switch to browser showing `http://localhost:8000/docs` (FastAPI Swagger UI).
*   **Voiceover**:
    > "Now, let's look at the database. In `schema.sql`, we define `listing_master` with custom indexes on city, category, and source to optimize query speed.
    > If we test this database via our FastAPI backend Swagger docs, we see four functional endpoints. Let's make a live API call to our bulk insert router by sending 3 test rows.
    > As we execute, it returns a 201 status confirming the bulk write. 
    > Similarly, we can test our GET dashboard aggregation routes for city-wise, category-wise, and source-wise counts, which return clean, sorted JSON listings that feed the frontend charts."

---

### 📊 2:30 - 4:00 | React Dashboard Walkthrough & Aesthetics
*   **Visual**: Switch to browser at `http://localhost:5173/`, hover over cards and interact with charts.
*   **Voiceover**:
    > "Here is our interactive dashboard, featuring a modern dark theme and card-style panels with responsive layout.
    > At the top, overview stats cards dynamically sum and display the database row count—currently 553—along with active sources.
    > Below, three custom Recharts visualizations illustrate the data: a City-wise Bar Chart, a Category-wise share Donut chart, and a Horizontal Bar Chart comparing volumes by source.
    > Hovering over columns reveals responsive, blur-effect tooltips displaying metrics. The layout is fully responsive; if we resize the viewport, elements stack vertically for a comfortable mobile experience."

---

### ⚠️ 4:00 - 5:00 | Graceful Error Handling & Technical Challenges
*   **Visual**: Open terminal, stop the Uvicorn server process, and refresh the dashboard showing the card error overlays. Then, restart the server, click **Retry**, and watch the charts recover.
*   **Voiceover**:
    > "To show the application's resilience, watch what happens if our backend API server goes offline. 
    > If we stop the FastAPI server and reload, the dashboard handles the connection refusal gracefully. Instead of displaying a blank screen or crashing, each chart card displays a clear, styled red error notice with an interactive 'Retry' option.
    > When we start the Uvicorn backend process again and click 'Retry', the dashboard immediately connects to the database, pulls the aggregates, and animations restore the charts with zero layout shift.
    > Key technical challenges we solved include managing MySQL re-runs idempotently, optimizing batch data operations using `executemany` database drivers, and fixing Vite compilation errors to produce a robust deployment."
