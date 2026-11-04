"""The home page. Run the whole app from the your-code folder:

    streamlit run Home.py
"""

import streamlit as st

from sakila import query       # query("SELECT ...") returns a DataFrame, cached

st.set_page_config(page_title="Sakila DVD Rentals", page_icon="🎬", layout="wide")

# TODO 1: a title (st.title) and an image of your choice (st.image, with a URL or a file).
st.title("🎬 Sakila DVD Rentals")
st.image(
    "https://images.unsplash.com/photo-1738708387940-ff9b5f673c29?w=1200&q=60&auto=format&fit=crop",
    caption="Photo by Denise Jans on Unsplash",
)

# TODO 2: one sentence for the store managers: what this dashboard is for.
st.write(
    "This dashboard shows the managers of both Sakila stores what customers rent, where and when, "
    "and helps them find films similar to the one a customer describes."
)

# TODO 3: four st.metric numbers in four st.columns: the number of films, customers and rentals,
#         and the total revenue (the sum of payment.amount). One SQL query can return all four.
totals = query("""
    SELECT (SELECT COUNT(*)      FROM film)     AS films,
           (SELECT COUNT(*)      FROM customer) AS customers,
           (SELECT COUNT(*)      FROM rental)   AS rentals,
           (SELECT SUM(amount)   FROM payment)  AS revenue
""").iloc[0]

films_col, customers_col, rentals_col, revenue_col = st.columns(4)
films_col.metric("Films", f"{int(totals['films']):,}")
customers_col.metric("Customers", f"{int(totals['customers']):,}")
rentals_col.metric("Rentals", f"{int(totals['rentals']):,}")
revenue_col.metric("Revenue", f"${totals['revenue']:,.2f}")