import streamlit as st
import psycopg2

# Replace with your PostgreSQL database credentials
host = "localhost"
user = "postgres"
password = "root"
database_name = "project"

def connect_to_db():
    try:
        conn_string = f"postgresql://{user}:{password}@{host}:5432/{database_name}"
        conn = psycopg2.connect(conn_string)
        return conn
    except psycopg2.OperationalError as error:
        st.error(f"Error connecting to database: {error}")
        return None

def query_data(query):
    conn = connect_to_db()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]  # Fetch column names
            results = cur.fetchall()
            return columns, results
    except (Exception, psycopg2.Error) as error:
        st.error(f"An error occurred while executing the query: {error}")
        return None, None
    finally:
        conn.close()

def main():
    st.title("Data Analysis App")

    # Categories for the first dropdown
    categories = {
        "Given Question": [
            "1. Top 10 Revenue Generating Products",
            "2. Find the top 5 cities with the highest profit margins",
            "3. Calculate the total discount given for each category",
            "4. Find the average sale price per product category",
            "5. Find the region with the highest average sale price",
            "6. Find the total profit per category",
            "7. Identify the top 3 segments with the highest quantity of orders",
            "8. Determine the average discount percentage given per region",
            "9. Find the product category with the highest total profit",
            "10. Calculate the total revenue generated per year"
        ],
        "Other Question": [
            "11. Find the average discount offered on each product.",
            "12. Find the top 3 cities with the highest average profit",
            "13. Find the total sales price per product.",
            "14. Calculate the average sales price for each state.",
            "15. Find the region with the highest number of orders.",
            "16. Find the top 5 states with the highest total profit",
            "17. Find the product that gave the maximum profit",
            "18. Calculate the total number of orders for each city.",
            "19. Find the region with the highest total quantity sold.",
            "20. Find the product with the lowest total profit."
        ],
        # More categories can be added here
    }

    # First dropdown: select category
    selected_category = st.selectbox("Select Category", ["Select any one"] + list(categories.keys()))

    if selected_category != "Select any one":
        # Second dropdown: select query within the chosen category
        subqueries = categories[selected_category]
        selected_query = st.selectbox("Select Query", ["Select a Query"] + subqueries)

        if selected_query != "Select a Query":
            # SQL Queries for each subquery
            query_options = {
                "1. Top 10 Revenue Generating Products": 
                    "SELECT product_id, SUM(sales_price) AS total_revenue FROM mydata2 GROUP BY product_id ORDER BY total_revenue DESC LIMIT 10;",
                "2. Find the top 5 cities with the highest profit margins": 
                    "SELECT d1.city, SUM(d2.profit) / SUM(d2.sales_price) AS profit_margin FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id WHERE d2.sales_price > 0 GROUP BY d1.city ORDER BY profit_margin DESC LIMIT 5;",
                "3. Calculate the total discount given for each category":
                    "SELECT d1.category, SUM(d2.discount) AS total_discount FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.category ORDER BY total_discount DESC;",
                "4. Find the average sale price per product category":
                    "SELECT d1.category, AVG(d2.sales_price) AS average_sale_price FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.category ORDER BY average_sale_price DESC;",
                "5. Find the region with the highest average sale price":
                    "SELECT d1.region, AVG(d2.sales_price) AS average_sale_price FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.region ORDER BY average_sale_price DESC LIMIT 5;",
                "6. Find the total profit per category":
                    "SELECT d1.category, SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.category ORDER BY total_profit DESC;",
                "7. Identify the top 3 segments with the highest quantity of orders":
                    "SELECT d1.segment, SUM(d2.quantity) AS total_quantity FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.segment ORDER BY total_quantity DESC LIMIT 3;",
                "8. Determine the average discount percentage given per region":
                    "SELECT d1.region, AVG(d2.discount_percent) AS average_discount_percentage FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.region ORDER BY average_discount_percentage DESC;",
                "9. Find the product category with the highest total profit":
                    "SELECT d1.category, SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.category ORDER BY total_profit DESC;",
                "10. Calculate the total revenue generated per year":
                    "SELECT EXTRACT(YEAR FROM d1.order_date) AS order_year, SUM(d2.sales_price) AS total_revenue FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY order_year ORDER BY order_year;",
                "11. Find the average discount offered on each product.":
                    "SELECT product_id, AVG(discount) AS average_discount FROM mydata2 GROUP BY product_id ORDER BY average_discount DESC;",
                "12. Find the top 3 cities with the highest average profit":
                    "SELECT d1.city, AVG(d2.profit) AS average_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.city ORDER BY average_profit DESC LIMIT 3;",
                "13. Find the total sales price per product.": 
                    "SELECT d1.city, SUM(d2.sales_price * d2.quantity) AS total_sales FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.city ORDER BY total_sales DESC LIMIT 1;",
                "14. Calculate the average sales price for each state.":
                    "SELECT d1.state, AVG(d2.sales_price) AS average_sales_price FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.state ORDER BY average_sales_price DESC;",
                "15. Find the region with the highest number of orders.":
                    "SELECT d1.region, COUNT(d1.order_id) AS total_orders FROM mydata1 d1 GROUP BY d1.region ORDER BY total_orders DESC LIMIT 1;",
                "16. Find the top 5 states with the highest total profit":
                    "SELECT d1.state, SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.state ORDER BY total_profit DESC LIMIT 5;",
                "17. Find the product that gave the maximum profit":
                    "SELECT d2.product_id, SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d2.product_id ORDER BY total_profit DESC LIMIT 1;",
                "18. Calculate the total number of orders for each city.":
                    "SELECT d1.city, COUNT(d1.order_id) AS total_orders FROM mydata1 d1 GROUP BY d1.city ORDER BY total_orders DESC;",  
                "19. Find the region with the highest total quantity sold.":
                    "SELECT d1.region, SUM(d2.quantity) AS total_quantity FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.region ORDER BY total_quantity DESC LIMIT 1;",
                "20. Find the product with the lowest total profit.":
                    "SELECT d2.product_id, SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d2.product_id ORDER BY total_profit ASC LIMIT 1;"
            }

            # Execute the selected query and display results
            query = query_options[selected_query]
            columns, data = query_data(query)

            if data is not None:
                import pandas as pd
                df = pd.DataFrame(data, columns=columns)
                st.dataframe(df)

if __name__ == "__main__":
    main()
