# 🛍️ E-Commerce Customer Segmentation & Retention Analytics

**End-to-End Data Analytics Project using Python, SQL Server & Power BI**

![Python](https://img.shields.io/badge/Python-Pandas-blue)
![SQL Server](https://img.shields.io/badge/SQL%20Server-Database-red)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow)
![RFM](https://img.shields.io/badge/Analytics-RFM-green)
![Cohort](https://img.shields.io/badge/Analytics-Cohort-purple)

---

# 📌 About the Project

This project analyzes transactional data from an **e-commerce store** to understand sales performance, customer purchasing behavior, and customer retention.

The project uses **Python, SQL Server, and Power BI** to transform transactional data into actionable business insights.

A major focus is **RFM Customer Segmentation**, which evaluates customers based on their **Recency, Frequency, and Monetary value** to identify different behavioral groups — from highly engaged and valuable customers to customers showing signs of inactivity or churn.

**Cohort Analysis** is also used to measure customer retention over time by tracking purchasing behavior after customers make their first purchase.

---

# 🛠️ Tech Stack

- 🐍 **Python / Pandas** — Data Quality Checks, Data Cleaning & Preprocessing
- 🗄️ **SQL Server** — Relational Database, Data Storage & Analytical Queries
- 📊 **Power BI** — Interactive Dashboards, Data Modeling & DAX Measures
- 🔌 **PyODBC** — Python–SQL Server Data Loading
- 📁 **CSV** — Raw and Preprocessed Data Storage

## 🧹 Phase 1: Data Quality & Data Cleaning (Python)

- Checked missing values across customer, product, order, and order item tables
- Checked duplicate records and duplicate customer IDs
- Validated data types for numeric and datetime columns
- Checked invalid and future dates
- Checked invalid product costs where `unit_cost > unit_price`
- Checked invalid order item quantities where `quantity <= 0`
- Checked referential integrity between orders and order items
- Checked referential integrity between products and order items
- Removed duplicate records and invalid order items
- Saved cleaned datasets as CSV files for downstream analysis

## 🗄️ Phase 2: Database Loading & SQL Server

- Designed a relational database schema for customers, products, orders, and order items
- Created tables and defined appropriate data types and relationships
- Connected Python to SQL Server using **PyODBC**
- Loaded preprocessed CSV data into SQL Server
- Used transaction handling with `commit` and `rollback` to ensure reliable data loading
- Wrote SQL queries to analyze sales performance and customer purchasing behavior

## 📊 Phase 3: Customer Analytics

- Built the RFM analysis with **CTEs** in multiple steps, using **delivered orders only**
- Calculated **Recency** (days since last purchase, relative to the latest order date in the data), **Frequency** (number of orders), and **Monetary** (total spend) for each customer
- Applied the **`NTILE(5)`** window function to score each metric from 1 to 5 (a more recent purchase gets a higher Recency score)
- Combined the three scores to classify customers into **11 RFM segments**
- Performed **Cohort Analysis**: grouped customers by **first purchase month** and measured the share of each cohort that purchased again in each following month

## 📈 Phase 4: Power BI Dashboard

- Built an interactive dashboard to monitor sales performance and customer behavior
- Analyzed revenue, gross profit, orders, customers, and average order value
- Visualized **RFM Customer Segmentation** and customer distribution
- Built a **Cohort Retention Analysis** to evaluate customer retention over time
- Used **DAX measures** for KPI calculations and analytical metrics
- Transformed analytical results into actionable business insights
---

# 📊 Dashboard Preview

## 1️⃣ Sales Performance Overview

The Sales Performance dashboard provides an overview of the store's overall sales performance.

It focuses on:

- Revenue trends
- Gross profit
- Order performance
- Customer contribution
- Product and category performance

<img width="1791" height="1015" alt="image" src="https://github.com/user-attachments/assets/b639994b-df09-4529-b398-170d7306c23b" />


---
## 2️⃣ Customer Segmentation — RFM Analysis

**RFM (Recency, Frequency, Monetary)** is used to evaluate customers based on their purchasing behavior.

| Metric | Definition |
|---|---|
| **Recency** | How recently a customer made a purchase |
| **Frequency** | How frequently a customer makes purchases |
| **Monetary** | How much a customer spends |

Customers are scored across the three dimensions and classified into **11 behavioral segments**.

### Customer Segments

| Customer Segment | Activity | Actionable Tip |
|---|---|---|
| 🏆 **Champions** | Bought recently, buy often and spend the most. | Reward them. They can be early adopters for new products and help promote the brand. |
| 💎 **Loyal Customers** | Spend good money with us often and are responsive to promotions. | Upsell higher-value products, ask for reviews and continue engaging them. |
| ⭐ **Potential Loyalist** | Recent customers who have spent a good amount and bought more than once. | Offer membership or loyalty programs and recommend relevant products. |
| 🆕 **Recent Customers** | Bought most recently, but not often. | Provide onboarding support, create early success and start building the relationship. |
| 🌱 **Promising** | Recent shoppers who haven't spent much. | Build brand awareness and encourage further purchases with suitable offers. |
| 👀 **Customers Needing Attention** | Above-average recency, frequency and monetary values, but may not have purchased very recently. | Use limited-time offers, recommend products based on past purchases and re-engage them. |
| 😴 **About To Sleep** | Below-average recency, frequency and monetary values. They may become inactive without reactivation. | Share valuable resources, recommend popular products or discounted renewals and reconnect with them. |
| ⚠️ **At Risk** | Spent significant money and purchased often, but their last purchase was a long time ago. | Send personalized re-engagement campaigns, offer renewals and provide helpful resources. |
| 🚨 **Can't Lose Them** | Made their biggest purchases and purchased often, but haven't returned for a long time. | Win them back with renewals or new products and prevent them from moving to competitors. |
| 💤 **Hibernating** | Last purchase was a long time ago, with low spending and a low number of orders. | Offer relevant products and special discounts to rebuild engagement and brand value. |
| ❌ **Lost** | Lowest Recency, Frequency and Monetary scores. | Attempt a final re-engagement campaign; otherwise, deprioritize further marketing efforts. |

This segmentation helps the business understand **customer value, engagement, and purchasing behavior**, while providing actionable strategies for different customer groups.

<img width="1796" height="1012" alt="image" src="https://github.com/user-attachments/assets/bb1a1999-9a27-4e11-afa5-c1b286edadbb" />


---
## 3️⃣ Cohort Retention Analysis

**Cohort Analysis** is used to measure customer retention over time.

Customers are grouped based on the **month of their first purchase**, then tracked across subsequent months to measure repeat purchasing behavior.

The analysis helps identify:

- Customer retention over time
- Repeat purchasing behavior
- Differences in retention between customer cohorts

<img width="1802" height="1012" alt="image" src="https://github.com/user-attachments/assets/9b510861-e7ac-4fe9-b4f0-763da77cf9b3" />
<img width="1792" height="1005" alt="image" src="https://github.com/user-attachments/assets/c1849526-9bff-4fff-9a0a-9567e4bd85a6" />


---

# 🔍 Key Insights

- **Strong year-end sales:** Revenue increased sharply in November and December, reaching **$2.5M total revenue** and **$1.01M gross profit**.

- **High delivery rate:** **88.7% of orders were delivered**, indicating generally strong order fulfillment performance.

- **Large potential for customer retention:** **Potential Loyalists (19.97%)** and **Champions (16.81%)** represent a significant portion of the customer base.

- **Significant inactive customer base:** **Lost, Hibernating, At Risk, and Can't Lose Them** customers account for a substantial share of customers, creating a clear reactivation opportunity.

- **Low purchase frequency:** The average customer makes only **1.93 purchases**, indicating that many customers are still low-frequency buyers.

- **Sharp retention decline:** For the 2025 cohort, retention drops from **100% in Month 1 to 8.55% in Month 2 and 5.84% in Month 3**, highlighting challenges in converting first-time buyers into repeat customers.

# 🎯 Recommended Actions

- **Increase repeat purchases:** Use post-purchase campaigns, personalized recommendations, cross-selling, and second-purchase incentives.

- **Strengthen loyalty:** Reward **Champions, Loyal Customers, and Potential Loyalists** with exclusive offers, loyalty rewards, and early access to new products.

- **Reactivate inactive customers:** Target **At Risk, Can't Lose Them, About To Sleep, and Hibernating** customers with personalized re-engagement campaigns.

- **Prioritize high-value customers:** Focus win-back campaigns on inactive customers with historically high spending or purchase frequency.

- **Improve early retention:** Focus retention efforts during the **first 1–3 months** after the first purchase, when customer drop-off is highest.

- **Leverage seasonal demand:** Prepare inventory and promotional campaigns ahead of the strong **November–December** sales period to maximize revenue and profit.
---
# 📁 Project Structure

```text
E-Commerce-Customer-Segmentation-Retention-Analytics/
│
├── dashboard/
│   └── dashboard.pbix
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   ├── order_items.csv
│   │   └── products.csv
│   │
│   └── preprocessed/
│       ├── customers_clean.csv
│       ├── orders_clean.csv
│       ├── order_items_clean.csv
│       └── products_clean.csv
│
├── scripts/
│   ├── data_quality_and_clean.py
│   └── load_to_sql.py
│
├── sql/
│   ├── create_database.sql
│   └── Analyst_queries.sql
│
└── README.md
