# E-COMMERCE DATA ANALYSIS DASHBOARD
                                                                                           
A Python-based web scraping and dashboard project that collects book data from Books to Scrapeand displays it interactively in a Streamlit dashboard with real-time auto-refresh and filtering options.

## Project Overview:
This project scrapes book details from an online e-commerce bookstore and stores the data in a SQLite database. A Streamlit dashboard then visualizes the data, highlighting top-rated (5★) books and allowing users to filter by price range. The dashboard also auto-refreshes every minute to display the latest data.

## Key Features:
- Web scraping using Requests and BeautifulSoup,
- Handles price, availability, ratings, and images,
- Stores scraped data in SQLite database with timestamps.

## Interactive Streamlit dashboard with:
- Auto-refresh every 1 minute,
- Budget filter for 5★ books,
- Top 10 book images display,
- Complete list of 5★ books sorted by price,
- Responsive UI with custom CSS styling.

## Technologies Used:
- Python  – Core programming language,
- Requests – For HTTP requests,
- BeautifulSoup – For web scraping and HTML parsing,
- SQLite – Lightweight relational database for storing scraped data,
- Streamlit – For creating interactive dashboards,
- pandas – Data analysis,
- streamlit-autorefresh – For automatic dashboard refresh.
