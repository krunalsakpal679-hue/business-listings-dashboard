# Scraping Approach & Data Strategy

This document outlines the data strategy for the Business Listings Dashboard, detailing the usage of mock seeding data, the web scraping proof-of-concept, and the production transition plan.

---

## 1. Rationale for Mock Data as Primary Source

For the development phase of the assignment, a mock data generation script (`generate_mock_data.py`) was selected as the primary source of seed listings rather than active production scrapers due to several reasons:

1.  **Safety and Compliance**: Production business directory sites (such as YellowPages, Justdial, Sulekha, and Google Maps) explicitly disallow automated scraping of search results paths in their `robots.txt` rules or require strict terms-of-service compliance. Violating these rules can result in IP blocks, legal notices, or account suspensions.
2.  **Reliability and Execution Speed**: Web scraping is fragile. Site structures, CSS classes, and HTML elements change frequently, which would break the data collection pipeline. Mock data generation provides a deterministic, zero-dependency, and instantly available dataset of 550 rows.
3.  **Completeness of Fields**: Mock data allows us to guarantee that fields crucial for dashboards (e.g. valid categories, normalized cities, realistic phone number formats, and source mappings) are fully populated and structured. This allows for rigorous frontend and backend testing.
4.  **Edge Case Testing**: We introduced explicit 5% null values for `phone` and `address` fields in the mock generator, mirroring real-world incomplete data profiles to test app robustness.

---

## 2. Web Scraping Proof-of-Concept (`scrape_sample.py`)

A proof-of-concept (POC) scraper was implemented in `backend/scripts/scrape_sample.py`. This script demonstrates how safe web scraping would work in a real environment:

*   **Safety Compliance**: It parses the target's `robots.txt` file using Python's `urllib.robotparser.RobotFileParser`. It checks if the target search URL is allowed for user agents.
*   **Graceful Exit**: If a target site disallows scraping (as YellowPages does for the search pathways), the script logs the block reason and exits cleanly with exit code `0` instead of forcing page requests.
*   **Scraping Mechanics (BS4)**: In allowed environments, it makes request calls using `requests` with realistic `User-Agent` headers and parses structured metadata (business name, category, location, address, phone) using `BeautifulSoup` element selectors.
*   **Respectful Rate Limiting**: The script includes a `time.sleep(1.5)` command between item parse routines to avoid spamming the host server.

---

## 3. Production Strategy: Swapping for Google Places API

In a production environment, web scraping would be replaced with official, robust APIs. The primary candidate is the **Google Places API** (specifically the Place Search or Text Search endpoint).

### Architecture for Swapping to API
1.  **API Requests**: Run text queries matching categories and cities (e.g. `query="restaurants in Mumbai"`).
2.  **API Keys & Security**: Securely store Google API keys in a backend `.env` configuration.
3.  **Data Ingestion**: Create a backend script that requests the API, reads pagination tokens (`next_page_token`), loops until it collects sufficient results, and maps the responses to our database schema.
4.  **API Mapping**:
    *   `business_name` $\rightarrow$ `name`
    *   `category` $\rightarrow$ Map from Google Places types (e.g. `restaurant` $\rightarrow$ `restaurants`)
    *   `city` $\rightarrow$ Parse from `formatted_address` or `address_components`
    *   `address` $\rightarrow$ `formatted_address`
    *   `phone` $\rightarrow$ Fetch via Place Details API using the `place_id` (fields: `formatted_phone_number`)
    *   `source` $\rightarrow$ Hardcode to `Google Places API`
5.  **Caching Layer**: Store results in our MySQL database to cache data, preventing redundant, expensive API calls to Google Places.
