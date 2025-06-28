
# 📊 Superstore Sales Analysis & Dashboard using SQL and Python

This project analyzes a real-world Superstore dataset using SQL and visualizes insights through an interactive Streamlit dashboard built with Python. It covers advanced SQL concepts and is ideal for demonstrating practical data engineering and analytics skills.

## 🔧 Technologies Used
- 🐍 Python (Pandas, Streamlit, Plotly)
- 🐬 MySQL
- 📊 SQL (CTE, Window Functions, CASE, Subqueries)
- 📁 Dataset: [Superstore Dataset (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

## 📂 Project Structure

| File | Description |
|------|-------------|
| `load.py` | Loads and cleans the Superstore dataset, then inserts it into a MySQL database |
| `dashboard.py` | Streamlit dashboard connected to MySQL, visualizing sales insights |
| `Superstore.csv` | Original dataset (download from Kaggle) |

## 📌 Key Features
- ✅ **ETL Pipeline**: Clean and import CSV to MySQL
- 📈 **Interactive Dashboard**: KPIs, revenue, segmentation, top products
- 🧠 **Advanced SQL Queries**:
  - CTEs for category-level aggregation
  - Window functions for ranking within regions
  - CASE statements for profit classification
  - Subqueries for top product analysis
- 🔐 **Authentication**: Basic username-password login for dashboard access

## 🚀 How to Run

1. Clone this repo and place `Superstore.csv` in the root folder.
2. Set up MySQL locally and create a `SalesDB` database.
3. Run the data loader:

    ```bash
    python load.py
    ```

4. Launch the dashboard:

    ```bash
    streamlit run dashboard.py
    ```

5. **Login Credentials:**  
   - Username: `analyst` | Password: `analyst123`  
   - Username: `admin` | Password: `admin123`


## 📌 Learning Outcomes

- End-to-end data pipeline from raw CSV to a production-ready dashboard
- Hands-on with SQL logic used in real business reporting
- Real-time analytics with auto-refreshing dashboard components

---

## 🙌 Contributing

Feel free to fork this repo or submit issues if you'd like to extend the project!
