import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from datetime import datetime
import platform

# Scraping Books
all_books = []
page = 1
while True:
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    if not books:
        break

    for book in books:
        
        # Title
        title = re.sub(r"\s+", " ", book.h3.a["title"]).strip()

        # Price (fix encoding)
        price = book.find("p", class_="price_color").text.strip()
        price = price.encode("latin1").decode("utf-8")

        # Availability
        availability_tag = book.find("p", class_="instock availability")
        availability = availability_tag.get_text(strip=True)

        # Ratings
        rating_class = book.find("p", class_="star-rating")["class"][1]
        rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}.get(rating_class, 0)

        # Image
        img_tag = book.find("img")
        img_url = "https://books.toscrape.com/" + img_tag["src"].replace("../", "")

        # Append to list
        all_books.append([title, price, availability, rating, img_url, "BooksToScrape"])

    print(f"Page {page} scraped, total books so far: {len(all_books)}")
    page += 1

print("Scraping complete!")
print(f"Total books scraped: {len(all_books)}")

# Platform check for DB path
if platform.system() == "Windows":
    db_path = r"C:\Users\AL HAD\OneDrive\Documents\PYTHON_PROJECT\books.db"
else:
    db_path = "/mnt/c/Users/AL HAD/OneDrive/Documents/PYTHON_PROJECT/books.db"

# Storing Data into SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS books")

# Create table
cursor.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price TEXT,
    availability TEXT,
    rating INTEGER,
    image TEXT,
    source TEXT,
    updated_at TEXT
)
""")

# Current timestamp
update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Insert each book using execute
for book in all_books:
    title, price, availability, rating, image, source = book
    cursor.execute("""
        INSERT INTO books (title, price, availability, rating, image, source, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, price, availability, rating, image, source, update_time))

conn.commit()
conn.close()

print(f"Data saved into books.db successfully! (Updated at {update_time})")