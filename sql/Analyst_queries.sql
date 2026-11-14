--KPI
SELECT SUM(oi.unit_price*quantity) AS total_revenue, SUM(quantity*(oi.unit_price-cost)) AS gross_profit,COUNT(DISTINCT o.order_id) AS total_order, SUM(oi.unit_price*quantity)/COUNT(DISTINCT o.order_id) AS AOV
FROM ec.order_items oi
INNER JOIN ec.orders o ON o.order_id=oi.order_id
WHERE order_status='Delivered'

--Top 10 Product by revenue
SELECT TOP 10 product_name,SUM(quantity) units_sold, SUM(oi.unit_price*quantity) AS revenue, SUM(quantity*(oi.unit_price-cost)) AS gross_profit
FROM ec.order_items oi
INNER JOIN ec.products p ON p.product_id=oi.product_id
INNER JOIN ec.orders o ON o.order_id=oi.order_id
WHERE order_status='Delivered'
GROUP BY product_name
ORDER BY revenue DESC;

--Monthly Revenue
SELECT MONTH(o.order_date) AS month, YEAR(o.order_date) AS year, SUM(quantity*unit_price) AS revenue
FROM ec.orders o
INNER JOIN ec.order_items oi ON oi.order_id=o.order_id
WHERE order_status='Delivered'
GROUP BY  YEAR(o.order_date),MONTH(o.order_date)
ORDER BY  YEAR(o.order_date), MONTH(o.order_date);


--MoM
WITH monthly_revenue AS ( SELECT MONTH(o.order_date) AS month, YEAR(o.order_date) AS year, SUM(quantity*unit_price) AS revenue
FROM ec.orders o
INNER JOIN ec.order_items oi ON oi.order_id=o.order_id
WHERE order_status='Delivered'
GROUP BY  YEAR(o.order_date),MONTH(o.order_date)
),
revenue_previous AS ( SELECT month, year, revenue, LAG(revenue,1) OVER(ORDER BY year, month) AS previous_revenue
FROM monthly_revenue)
SELECT month, year, revenue, previous_revenue, 100.0 * (revenue - previous_revenue)/ NULLIF(previous_revenue, 0) AS mom_growth_pct
FROM revenue_previous
ORDER BY year, month;

-- RFM
WITH snapshot AS ( SELECT DATEADD(DAY,1,MAX(order_date)) AS snapshot_date
FROM ec.orders
WHERE order_status='Delivered'
),
customer_rfm AS( SELECT o.customer_id, full_name, DATEDIFF(DAY, MAX(order_date),s.snapshot_date) AS recency_day, COUNT(DISTINCT o.order_id) AS frequency, SUM(unit_price*quantity) AS monetary
FROM ec.customers c
INNER JOIN ec.orders o ON c.customer_id=o.customer_id
INNER JOIN ec.order_items oi ON oi.order_id=o.order_id
CROSS JOIN snapshot s
WHERE order_status='Delivered'
GROUP BY o.customer_id, full_name,s.snapshot_date
),
rfm_score AS (SELECT *, NTILE(5) OVER(ORDER BY recency_day DESC) AS r_score,
					NTILE(5) OVER(ORDER BY frequency) AS f_score,
					NTILE(5) OVER(ORDER BY monetary) AS m_score
FROM customer_rfm
),
rfm_final AS (
			SELECT *, CONCAT(r_score,f_score,m_score) AS rfm_overall
			FROM rfm_score
),
rfm_segment AS (
    SELECT *,
        CASE
            WHEN rfm_overall IN ('555','554','544','545','454','455','445')
                THEN 'Champions'

            WHEN rfm_overall IN ('543','444','435','355','354','345','344','335')
                THEN 'Loyal'

            WHEN rfm_overall IN ('553','551','552','541','542','533','532','531',
                                 '452','451','442','441','431','453','433','432',
                                 '423','353','352','351','342','341','333','323')
                THEN 'Potential Loyalist'

            WHEN rfm_overall IN ('512','511','422','421','412','411','311')
                THEN 'New Customers'

            WHEN rfm_overall IN ('525','524','523','522','521','515','514','513',
                                 '425','424','413','414','415','315','314','313')
                THEN 'Promising'

            WHEN rfm_overall IN ('535','534','443','434','343','334','325','324')
                THEN 'Need Attention'

            WHEN rfm_overall IN ('331','321','312','221','213','231','241','251')
                THEN 'About To Sleep'

            WHEN rfm_overall IN ('255','254','245','244','253','252','243','242',
                                 '235','234','225','224','153','152','145','143',
                                 '142','135','134','133','125','124')
                THEN 'At Risk'

            WHEN rfm_overall IN ('155','154','144','214','215','115','114','113')
                THEN 'Cannot Lose Them'

            WHEN rfm_overall IN ('332','322','231','241','251','233','232','223',
                                 '222','132','123','122','212','211')
                THEN 'Hibernating'

            WHEN rfm_overall IN ('111','112','121','131','141','151')
                THEN 'Lost Customers'

            ELSE 'Others'
        END AS customer_segment
    FROM rfm_final
)
SELECT *
FROM rfm_segment

--Repeat vs New Customer Analysis
WITH order_count AS (SELECT COUNT(DISTINCT o.order_id) AS num_order,
                            customer_id,
                            SUM(quantity* unit_price) AS revenue,
                            SUM(quantity*(unit_price-cost)) AS gross_profit
                    FROM ec.orders o
                    INNER JOIN ec.order_items oi ON o.order_id = oi.order_id
                    WHERE order_status = 'Delivered'
                    GROUP BY customer_id
                    ),
customer_type AS ( SELECT *,
                            CASE WHEN num_order >1 THEN 'repeat customer' ELSE 'new customer' END AS cus_type
                    FROM order_count
                    )
SELECT  cus_type,
        SUM(revenue) AS total_revenue,
        SUM(num_order) AS total_order,
        SUM(gross_profit) AS total_profit
FROM customer_type
GROUP BY cus_type


--COHORT

WITH t1 AS ( SELECT customer_id,DATEFROMPARTS(YEAR(MIN(order_date)),MONTH(MIN(order_date)),1) AS cohort_month
                                 FROM ec.orders
                                 WHERE order_status = 'Delivered'
                                 GROUP BY customer_id
                                ),
t2 AS ( SELECT DISTINCT o.customer_id,
                                       DATEFROMPARTS(YEAR(order_date),MONTH(order_date),1) as purchase_month,
                                       cohort_month
                        FROM ec.orders o
                        JOIN t1 f ON f.customer_id= o.customer_id
                        WHERE order_status = 'Delivered'
                        ),
t3 AS ( SELECT  cohort_month,
                DATEDIFF(MONTH, cohort_month,purchase_month)+1 AS month_number,
                customer_id
        FROM t2
        ),
t4 AS ( SELECT cohort_month, month_number, COUNT(customer_id) AS customers
        FROM t3
        WHERE month_number BETWEEN 0 AND 12
        GROUP BY cohort_month, month_number 
        )
select *
from t4
order by cohort_month

                        

                    











