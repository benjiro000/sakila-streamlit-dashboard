import pandas as pd
import streamlit as st

from sakila import query

st.set_page_config(page_title="Explore", page_icon="📊", layout="wide")
st.title("📊 Explore the rentals")

# TODO 4: a line chart of the daily rentals of each store in 2005.
#   - rental has rental_date; inventory links each rental (inventory_id) to a store (store_id).
#   - In SQLite, DATE(rental_date) gives the day and STRFTIME('%Y', rental_date) the year.
#   - st.line_chart draws one line per column: pivot the result so that each store is a column.
st.subheader("Daily rentals of each store in 2005")

daily = query("""
    SELECT DATE(r.rental_date) AS day, i.store_id AS store, COUNT(*) AS rentals
    FROM rental AS r
    JOIN inventory AS i ON i.inventory_id = r.inventory_id
    WHERE STRFTIME('%Y', r.rental_date) = '2005'
    GROUP BY day, store
""")
daily["day"] = pd.to_datetime(daily["day"])              # real dates, so the x axis is a time axis
daily["store"] = "Store " + daily["store"].astype(str)   # "Store 1" / "Store 2" as the line names
daily_by_store = daily.pivot(index="day", columns="store", values="rentals")   # one column per store

st.line_chart(daily_by_store)
st.caption(
    f"The sample database has gaps: there are rentals on only {len(daily_by_store)} days between "
    f"{daily_by_store.index.min():%d %B} and {daily_by_store.index.max():%d %B %Y}. "
    "The other days are missing from the data, not quiet days."
)

# TODO 5: a bar chart of the total revenue of each store (payment -> rental -> inventory).
st.subheader("Total revenue of each store")

revenue = query("""
    SELECT i.store_id AS store, SUM(p.amount) AS revenue
    FROM payment AS p
    JOIN rental AS r ON r.rental_id = p.rental_id
    JOIN inventory AS i ON i.inventory_id = r.inventory_id
    GROUP BY i.store_id
""")
revenue["store"] = "Store " + revenue["store"].astype(str)

st.bar_chart(revenue, x="store", y="revenue")

# TODO 6: the top 5 most rented films of each store in 2005, one st.dataframe per store, side by side.
st.subheader("Top 5 most rented films of each store in 2005")

top_films = query("""
    SELECT i.store_id AS store, f.title AS title, COUNT(*) AS rentals
    FROM rental AS r
    JOIN inventory AS i ON i.inventory_id = r.inventory_id
    JOIN film AS f ON f.film_id = i.film_id
    WHERE STRFTIME('%Y', r.rental_date) = '2005'
    GROUP BY i.store_id, f.film_id
    ORDER BY rentals DESC, f.title
""")

store_1_column, store_2_column = st.columns(2)

with store_1_column:
    st.markdown("**Store 1**")
    st.dataframe(top_films[top_films["store"] == 1].head(5)[["title", "rentals"]], hide_index=True)

with store_2_column:
    st.markdown("**Store 2**")
    st.dataframe(top_films[top_films["store"] == 2].head(5)[["title", "rentals"]], hide_index=True)