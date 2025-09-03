from streamlit_autorefresh import st_autorefresh
import pandas as pd
import streamlit as st
import sqlite3

# Refresh every 1 minute (60,000 ms)
st_autorefresh(interval=60000, key="dbrefresh")

# Page config
st.set_page_config(page_title="E-Commerce Books Dashboard", layout="wide")

# --- Custom CSS for styling ---
st.markdown(
    """
    <style>
        /* Set background to white */
        .stApp {
            background-color: white;
        }
        /* Make all headings green */
        h1, h2, h3, h4, h5, h6 {
            color: green !important;
        }
        /* Make Streamlit subheaders and markdown titles blue */
        .stMarkdown, .stDataFrame {
            color: green !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Title
st.markdown(
    "<h1 style='text-align: center;'>E-Commerce Books Dashboard</h1>",
    unsafe_allow_html=True
)

# Database path
db_path = r"/mnt/c/Users/AL HAD/OneDrive/Documents/PYTHON_PROJECT/books.db"

# Query all 5★ books
conn = sqlite3.connect(db_path)
query_all = """
SELECT title, price, availability, rating, image, updated_at
FROM books
WHERE rating = 5
ORDER BY CAST(SUBSTR(price, 2) AS REAL) ASC
"""
df_all = pd.read_sql_query(query_all, conn)
conn.close()

# --- Budget Filter ---
if df_all.empty:
    st.warning("No 5★ books found in the database.")
else:
    min_price = float(df_all["price"].str.replace("£", "").min())
    max_price = float(df_all["price"].str.replace("£", "").max())

    st.subheader("💰 Filter by Budget")
    budget_min, budget_max = st.slider(
        "Budget Range",   # proper label
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=1.0,  # slider value change in steps of 1
        label_visibility="collapsed"  # hides it in UI
    )

    # Filter books by budget
    df_filtered = df_all[
        (df_all["price"].str.replace("£", "").astype(float) >= budget_min) &
        (df_all["price"].str.replace("£", "").astype(float) <= budget_max)
    ]

    # Show Top 10 Images within budget
    if not df_filtered.empty:
        df_top10 = df_filtered.head(10)

        st.subheader(f"📚 Top 10 5★ Books (within £{budget_min:.2f} - £{budget_max:.2f})")
        cols = st.columns(5, gap="large")  # 5 per row with space between

        for i, row in df_top10.iterrows():
            stars = "⭐" * row["rating"]  # convert rating to stars
            with cols[i % 5]:
                st.image(row["image"], width="stretch")
                st.markdown(
                    f"<div style='text-align: center; font-size:14px; margin-bottom:50px;'>"
                    f"<b>{row['title']}</b><br>"
                    f"{stars}<br>"
                    f"💰 {row['price']}<br>"
                    f"📦 {row['availability']}"
                    f"</div>",
                    unsafe_allow_html=True
                )
    else:
        st.warning("⚠️ No books found in this budget range.")

    # Last updated time
    last_updated = df_all['updated_at'].max()
    st.subheader(f"📅 Database last updated at: {last_updated}")
    
    # Show Table (all 5★ books)
    st.subheader("📊 All 5★ Books (Sorted by Price)")
    st.dataframe(df_all.drop(columns=["image", "updated_at"]), width="stretch")