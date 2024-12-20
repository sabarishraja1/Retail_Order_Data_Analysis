create table mydata (order_id INT PRIMARY KEY,
					order_date DATE,
					ship_mode VARCHAR(20),
					segment VARCHAR(20),
					country VARCHAR(20), 
					city VARCHAR(20),
					state VARCHAR(20),
					postal_code INT,
					region VARCHAR(20),
					category VARCHAR(20),
					sub_category VARCHAR(20),
					product_id VARCHAR(20),
					cost_price INT,
					list_price INT,
					quantity INT,
					discount_percent INT,
					discount DECIMAL(7, 2), 
					sales_price DECIMAL(7, 2),
					profit DECIMAL(7, 2)
)





copy mydata from 'D:\guvi\progicts\class2_pro\New folder\my_data.csv' delimiter ',' csv header;

create table mydata1 (order_id INT PRIMARY KEY,
					order_date DATE,
					ship_mode VARCHAR(20),
					segment VARCHAR(20),
					country VARCHAR(20), 
					city VARCHAR(20),
					state VARCHAR(20),
					postal_code INT,
					region VARCHAR(20),
					category VARCHAR(20)
					)


copy mydata1 from 'D:\guvi\progicts\class2_pro\New folder\my_data1.csv' delimiter ',' csv header;


CREATE TABLE mydata2 (order_id INT PRIMARY KEY,
    				sub_category VARCHAR(20),
					product_id VARCHAR(20),
					cost_price INT,
					list_price INT,
					quantity INT,
					discount_percent INT,
					discount DECIMAL(7, 2), 
					sales_price DECIMAL(7, 2),
					profit DECIMAL(7, 2)
)
  



copy mydata2  from 'D:\guvi\progicts\class2_pro\New folder\my_data2.csv' delimiter ',' csv header;





1. Top 10 Revenue Generating Products:

SELECT product_id SUM(sales_price) AS total_revenue 
FROM mydata2
GROUP BY product_id 
ORDER BY total_revenue DESC
LIMIT 10;
2. Find the top 5 cities with the highest profit margins: 

SELECT d1.city SUM(d2.profit) / SUM(d2.sales_price) AS profit_margin
FROM mydata1 d1 
JOIN mydata2 d2 ON d1.order_id = d2.order_id 
WHERE d2.sales_price > 0 
GROUP BY d1.city
ORDER BY profit_margin DESC 
LIMIT 5;
3. Calculate the total discount given for each category:

 SELECT d1.category SUM(d2.discount) AS total_discount 
 FROM mydata1 d1 
 JOIN mydata2 d2 ON d1.order_id = d2.order_id
 GROUP BY d1.category
 ORDER BY total_discount DESC;
 
 4. Find the average sale price per product category:
 SELECT d1.category AVG(d2.sales_price) AS average_sale_price 
 FROM mydata1 d1
 JOIN mydata2 d2 ON d1.order_id = d2.order_id
 GROUP BY d1.category
 ORDER BY average_sale_price DESC;
 
 5. Find the region with the highest average sale price:
SELECT d1.region AVG(d2.sales_price) AS average_sale_price
FROM mydata1 d1 
JOIN mydata2 d2 ON d1.order_id = d2.order_id 
GROUP BY d1.region
ORDER BY average_sale_price DESC 
LIMIT 5;

6. Find the total profit per category:
SELECT d1.category (d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.category ORDER BY total_profit DESC;
 7. Identify the top 3 segments with the highest quantity of orders:
SELECT d1.segment sum(d2.quantity) AS total_quantity FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.segment ORDER BY total_quantity DESC LIMIT 3;
 8. Determine the average discount percentage given per region:
SELECT d1.region AVG(d2.discount_percent) AS average_discount_percentage FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.region ORDER BY average_discount_percentage DESC;
 9. Find the product category with the highest total profit:
SELECT d1.category sum(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.category ORDER BY total_profit DESC;
10. Calculate the total revenue generated per year:
SELECT EXTRACT(YEAR FROM d1.order_date) AS order_year  1 (d2.sales_price) AS total_revenue FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY order_year ORDER BY order_year;
 11. Find the average discount offered on each product.:
SELECT product_id AVG(discount) AS average_discount FROM mydata2 GROUP BY product_id ORDER BY average_discount DESC;
  12. Find the top 3 cities with the highest average profit:
SELECT d1.city AVG(d2.profit) AS average_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.city ORDER BY average_profit DESC LIMIT 3;
13. Find the total sales price per product.: 
SELECT d1.city SUM(d2.sales_price * d2.quantity) AS total_sales FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.city ORDER BY total_sales DESC LIMIT 1;
 14. Calculate the average sales price for each state.:
SELECT d1.state AVG(d2.sales_price) AS average_sales_price FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.state ORDER BY average_sales_price DESC;
 15. Find the region with the highest number of orders.:
SELECT d1.region COUNT(d1.order_id) AS total_orders FROM mydata1 d1 GROUP BY d1.region ORDER BY total_orders DESC LIMIT 1;
 16. Find the top 5 states with the highest total profit:
SELECT d1.state SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.state ORDER BY total_profit DESC LIMIT 5;
 17. Find the product that gave the maximum profit:
SELECT d2.product_id SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d2.product_id ORDER BY total_profit DESC LIMIT 1;
 18. Calculate the total number of orders for each city.:
SELECT d1.city COUNT(d1.order_id) AS total_orders FROM mydata1 d1 GROUP BY d1.city ORDER BY total_orders DESC;  
 19. Find the region with the highest total quantity sold.:
SELECT d1.region SUM(d2.quantity) AS total_quantity FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d1.region ORDER BY total_quantity DESC LIMIT 1;
 20. Find the product with the lowest total profit.:
SELECT d2.product_id SUM(d2.profit) AS total_profit FROM mydata1 d1 JOIN mydata2 d2 ON d1.order_id = d2.order_id GROUP BY d2.product_id ORDER BY total_profit ASC LIMIT 1;
     
