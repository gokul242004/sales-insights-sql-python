#Streamlit Dashboard for Superstore Sales Data with Authentication

import pandas as pd
import mysql.connector
import streamlit as st
import plotly.express as px
import streamlit_authenticator as stauth

# --------------------------
# USER AUTHENTICATION SETUP
# --------------------------
credentials = {
    "usernames": {
        "admin": {
            "name": "Admin User",
            "password": stauth.Hasher(["admin123"]).generate()[0]
        },
        "analyst": {
            "name": "Analyst",
            "password": stauth.Hasher(["analyst123"]).generate()[0]
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    cookie_name='superstore_dashboard',
    key='abcdef',
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Logout button top-right
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        authenticator.logout('Logout', 'main')

    st.success(f'Welcome {name} 👋')
    
    # --------------------------
    # MYSQL CONNECTION
    # --------------------------
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="******",  # enter your database password
        database="sales"
    )

    # --------------------------
    # STREAMLIT DASHBOARD
    # --------------------------
    st.set_page_config(page_title="Superstore Dashboard", layout="wide")
    st.title("📦 Superstore Sales Dashboard")

    # KPI Metrics
    kpi_query = """
    SELECT COUNT(DISTINCT order_id) AS Total_Orders,
           SUM(sales) AS Total_Sales,
           SUM(profit) AS Total_Profit
    FROM superstore_sales;
    """
    kpi_df = pd.read_sql(kpi_query, conn)
    st.subheader("🔢 KPI Metrics")
    st.dataframe(kpi_df)

    # Segment Revenue
    segment_query = """
    SELECT segment, SUM(sales) AS revenue
    FROM superstore_sales
    GROUP BY segment;
    """
    segment_df = pd.read_sql(segment_query, conn)
    st.subheader("💼 Revenue by Segment")
    st.plotly_chart(px.bar(segment_df, x="segment", y="revenue", title="Segment-wise Revenue"))

    # Region Performance (Window Function)
    window_query = """
    SELECT order_id, region, sales,
      RANK() OVER (PARTITION BY region ORDER BY sales DESC) AS region_rank
    FROM superstore_sales;
    """
    window_df = pd.read_sql(window_query, conn)
    st.subheader("🌍 Region Performance (Ranked)")
    st.dataframe(window_df.head(20))

    # Profit Classification (CASE)
    case_query = """
    SELECT order_id,
      CASE 
        WHEN profit > 100 THEN 'High Profit'
        WHEN profit BETWEEN 0 AND 100 THEN 'Low Profit'
        ELSE 'Loss'
      END AS profit_band
    FROM superstore_sales;
    """
    case_df = pd.read_sql(case_query, conn)
    st.subheader("📈 Profit Classification")
    st.dataframe(case_df.head(20))

    # Top Products (Subquery)
    subquery = """
    SELECT product_name, revenue FROM (
        SELECT product_name, SUM(sales) AS revenue
        FROM superstore_sales
        GROUP BY product_name
    ) AS ranked_products
    ORDER BY revenue DESC LIMIT 5;
    """
    top_products_df = pd.read_sql(subquery, conn)
    st.subheader("🏆 Top 5 Products by Sales")
    st.plotly_chart(px.bar(top_products_df, x="product_name", y="revenue", title="Top Products by Revenue"))

    # CTE Example: Total sales by category with filtering
    cte_query = """
    WITH category_sales AS (
        SELECT category, SUM(sales) AS total_sales
        FROM superstore_sales
        GROUP BY category
    )
    SELECT * FROM category_sales WHERE total_sales > 50000;
    """
    cte_df = pd.read_sql(cte_query, conn)
    st.subheader("📦 High-Performing Categories (CTE)")
    st.dataframe(cte_df)

    conn.close()

elif authentication_status is False:
    st.error("Incorrect username or password")
elif authentication_status is None:
    st.warning("Please enter your username and password")




