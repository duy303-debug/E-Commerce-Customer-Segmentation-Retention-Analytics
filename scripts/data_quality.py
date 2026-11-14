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

#----------------------------------------------
# CHECK 
#----------------------------------------------
print("\n=============CHECK TABLE CUSTOMERS=================")

#1. Check missing data
print("\nMissing  customers values:",
        df_customers.isna().sum())

#2. Check duplicate data
print("\nDuplicate customer_id:",
        df_customers["customer_id"].duplicated().sum())
#3. Check data types
print("\nColumns data types:",
      df_customers.dtypes)

#4. Check date of birth
dob = pd.to_datetime(
    df_customers["date_of_birth"], errors="coerce"
    )
print("Invalid date_of_birth:", dob.isna().sum())
print("Future date_of_birth:", (dob > pd.Timestamp.today()).sum())

print("\n=============CHECK TABLE PRODUCTS=================")

#1. Check missing data
print("\nMissing products values:", 
        df_products.isna().sum())

#2. Check data types
print("\nColumns data types:",
      df_products.dtypes)

#3. Check cost > price
invalid_cost =  df_products[df_products["unit_cost"]>df_products["unit_price"]]
print("invalid_cost:", invalid_cost)

print("\n=============CHECKING TABLE ORDERS=================")

#1. Check Missing data
print("\nMissing values:",
        df_orders.isna().sum())

#2. Check duplicate rows
print("\nDuplicate rows:",
        df_orders.duplicated().sum())

#3 Check data type
print("\nColumns data types:",
      df_orders.dtypes)

#4. Check order date --> NaT
od = pd.to_datetime(
    df_orders["order_date"], errors="coerce"
    )
print("Invalid order_date:", od.isna().sum())
#5. Check future order date
print("Future order_date:", (od > pd.Timestamp.today()).sum())

print("\n=============CHECKING TABLE ORDER_ITEMS=================")

#1. Check Missing data
print("\nMissing values:",
        df_order_items.isna().sum())

#2. Check duplicate rows
print("\nDuplicate rows:",
        df_order_items.duplicated().sum())

#3 Check data type
print("\nColumns data types:",
      df_order_items.dtypes)

#4. Check quantity < 0
print("\nNumber of rows with quantity <= 0: ", len(df_order_items[df_order_items["quantity"]<=0]))

#5 Check Referential Integrity
valid_order_id=set(df_orders["order_id"])
order_id_exists_in_orders = df_order_items[~df_order_items["order_id"].isin(valid_order_id)]
print(
    "Number of order items with invalid order IDs:",
    len(order_id_exists_in_orders)
)

# 6. Check Referential Integrity - Product IDs
valid_product_ids = set(df_products["product_id"])

product_id_exists_in_products = (
    df_order_items["product_id"].isin(valid_product_ids)
)
invalid_product_items = df_order_items[~product_id_exists_in_products]
print(
    "Number of order items with invalid product IDs:",
    len(invalid_product_items)
)