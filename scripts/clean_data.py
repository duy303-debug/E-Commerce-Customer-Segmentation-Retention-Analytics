import pandas as pd
import os

#------------------------------------------
# CONFIG
#------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

#------------------------------------------
# LOAD DATA
#------------------------------------------

df_customers = pd.read_csv(os.path.join(RAW_DIR,"customers.csv"))

df_products = pd.read_csv(os.path.join(RAW_DIR,"products.csv"))

df_orders = pd.read_csv(os.path.join(RAW_DIR,"orders.csv"))

df_order_items = pd.read_csv(os.path.join(RAW_DIR,"order_items.csv"))

#------------------------------------------
# CLEAN CUSTOMERS
#------------------------------------------
print("\n[1/4] Cleaning the customer table")
#1. Drop duplicate
before_customer = len(df_customers)
df_customers=df_customers.drop_duplicates(subset=["customer_id"], keep = "first")
after_customer = len(df_customers)
print(f"Removed {before_customer-after_customer:,} duplicate rows")

#2. Missing data
df_customers[["phone","gender","city"]]=df_customers[["phone","gender","city"]].fillna("N/A")

#3 fix date of birth
df_customers["date_of_birth"] = pd.to_datetime(
    df_customers["date_of_birth"], errors="coerce"
    )
#------------------------------------------
# CLEAN PRODUCTS
#------------------------------------------
print("\n[2/4] Cleaning the Product table")

#1 Drop duplicate
before_product = len(df_products)
df_products=df_products.drop_duplicates(subset=["product_id"], keep = "first")
after_product = len(df_products)
print(f"Removed {before_product-after_product:,} duplicate rows")

#2 fix data type
df_products["unit_price"]=pd.to_numeric(df_products["unit_price"], errors="coerce")
df_products["unit_cost"]=pd.to_numeric(df_products["unit_cost"], errors="coerce")

#------------------------------------------
# CLEAN ORDERS
#------------------------------------------
print("\n[3/4] Cleaning the Order table")
#1 Drop duplicate
before_order = len(df_orders)
df_orders=df_orders.drop_duplicates()
after_order = len(df_orders)
print(f"Removed {before_order-after_order:,} duplicate rows")

#2 fix data type order_date
df_orders["order_date"]=pd.to_datetime(df_orders["order_date"], errors="coerce")

#------------------------------------------
# CLEAN ORDER ITEMS
#------------------------------------------
print("\n[4/4] Cleaning the Order item table")


#1 Remove duplicate rows
before_order_item = len(df_order_items)
df_order_items = df_order_items.drop_duplicates()
after_order_item = len(df_order_items)
print(f"Removed {before_order_item-after_order_item :,} duplicate rows")

#2 fix data type
df_order_items["unit_price"]=pd.to_numeric(df_order_items["unit_price"], errors="coerce")
df_order_items["cost"]=pd.to_numeric(df_order_items["cost"], errors="coerce")
df_order_items["quantity"] = pd.to_numeric(df_order_items["quantity"], errors="coerce")


#3 Remove rows with quantity <= 0
df_order_items = df_order_items[
    df_order_items["quantity"] > 0
]

#4 Remove rows with invalid order IDs
valid_order_ids = set(df_orders["order_id"])

df_order_items = df_order_items[
    df_order_items["order_id"].isin(valid_order_ids)
]

print("Rows after cleaning:", len(df_order_items))

#------------------------------------------
# SAVE DATA CLEAN
#------------------------------------------
PRE_DIR = os.path.join(PROJECT_ROOT, "data", "preprocessed")
os.makedirs(PRE_DIR, exist_ok=True)

df_customers.to_csv(
    os.path.join(PRE_DIR, "customers_clean.csv"),
    index=False,
    encoding="utf-8-sig"
)

df_products.to_csv(
    os.path.join(PRE_DIR, "products_clean.csv"),
    index=False,
    encoding="utf-8-sig"
)

df_orders.to_csv(
    os.path.join(PRE_DIR, "orders_clean.csv"),
    index=False,
    encoding="utf-8-sig"
)

df_order_items.to_csv(
    os.path.join(PRE_DIR, "order_items_clean.csv"),
    index=False,
    encoding="utf-8-sig"
)

print(f"Saved {len(df_customers):,} rows to data/preprocessed/customers_clean.csv")
print(f"Saved {len(df_products):,} rows to data/preprocessed/products_clean.csv")
print(f"Saved {len(df_orders):,} rows to data/preprocessed/orders_clean.csv")
print(f"Saved {len(df_order_items):,} rows to data/preprocessed/order_items_clean.csv")