# Load and Clean Superstore Data, and Upload to MySQL

import pandas as pd
import mysql.connector

# Load Dataset
df = pd.read_csv("Superstore.csv", encoding="ISO-8859-1")

# Data Cleaning
df.dropna(inplace=True)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df.fillna(0, inplace=True)

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="********",#enter your workbench login credentials
    database="sales"
)
cursor = conn.cursor()

# Create table 
cursor.execute("""
CREATE TABLE IF NOT EXISTS superstore_sales (
    order_id VARCHAR(20),
    order_date DATE,
    ship_date DATE,
    customer_name VARCHAR(100),
    segment VARCHAR(50),
    region VARCHAR(50),
    product_id VARCHAR(20),
    product_name VARCHAR(255),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    sales DECIMAL(10,2),
    quantity INT,
    discount DECIMAL(5,2),
    profit DECIMAL(10,2)
);
""")

# Clear existing data|| avoid inserting again if we run multiple times
cursor.execute("TRUNCATE TABLE superstore_sales")
# Insert data
for _, row in df.iterrows():
    values = (
        row['Order ID'], row['Order Date'], row['Ship Date'], row['Customer Name'],
        row['Segment'], row['Region'], row['Product ID'], row['Product Name'],
        row['Category'], row['Sub-Category'], row['Sales'], row['Quantity'],
        row['Discount'], row['Profit']
    )

    cursor.execute("""
        INSERT INTO superstore_sales (
            order_id, order_date, ship_date, customer_name, segment, region, 
            product_id, product_name, category, sub_category, sales, quantity, discount, profit
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, values)

conn.commit()
conn.close()
print("Data loaded and inserted into MySQL successfully.")
