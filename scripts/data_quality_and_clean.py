import pandas as pd
import os

#------------------------------------------
# CONFIG
#------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PRE_DIR = os.path.join(PROJECT_ROOT, "data", "preprocessed")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PRE_DIR, exist_ok=True)

TODAY = pd.Timestamp.today()

#------------------------------------------
# LOAD DATA
#------------------------------------------


df_customers = pd.read_csv(os.path.join(RAW_DIR, "customers.csv"), dtype={"phone": str})

df_products = pd.read_csv(os.path.join(RAW_DIR, "products.csv"))

df_orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))

df_order_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))

#==============================================
# PART 1: DATA QUALITY CHECK (on raw data)
#==============================================
print("\n##############################################")
print("# PART 1: DATA QUALITY CHECK (RAW DATA)")
print("##############################################")

print("\n=============CHECK TABLE CUSTOMERS=================")

#1. Check missing data
print("\nMissing customers values:\n",
      df_customers.isna().sum())

#2. Check duplicate data
print("\nDuplicate customer_id:",
      df_customers["customer_id"].duplicated().sum())

#3. Check data types
print("\nColumns data types:\n",
      df_customers.dtypes)

#4. Check date of birth
dob = pd.to_datetime(
    df_customers["date_of_birth"], errors="coerce"
)
print("\nInvalid date_of_birth:", dob.isna().sum())
print("Future date_of_birth:", (dob > TODAY).sum())

#5. Check blank strings (empty or only spaces)
for col in ["phone", "gender", "city"]:
    blank_count = df_customers[col].astype("string").str.strip().eq("").sum()
    print(f"Blank values in {col}:", blank_count)

print("\n=============CHECK TABLE PRODUCTS=================")

#1. Check missing data
print("\nMissing products values:\n",
      df_products.isna().sum())

#2. Check duplicate product_id
print("\nDuplicate product_id:",
      df_products["product_id"].duplicated().sum())

#3. Check data types
print("\nColumns data types:\n",
      df_products.dtypes)

#4. Check price / cost not numeric, negative
unit_price_num = pd.to_numeric(df_products["unit_price"], errors="coerce")
unit_cost_num = pd.to_numeric(df_products["unit_cost"], errors="coerce")
print("\nNon-numeric unit_price (NaN after convert):", unit_price_num.isna().sum())
print("Non-numeric unit_cost (NaN after convert):", unit_cost_num.isna().sum())
print("Negative unit_price:", (unit_price_num < 0).sum())
print("Negative unit_cost:", (unit_cost_num < 0).sum())

#5. Check cost > price
invalid_cost = df_products[unit_cost_num > unit_price_num]
print("\nRows with unit_cost > unit_price:", len(invalid_cost))
print(invalid_cost)

print("\n=============CHECKING TABLE ORDERS=================")

#1. Check Missing data
print("\nMissing values:\n",
      df_orders.isna().sum())

#2. Check duplicate rows
print("\nDuplicate rows:",
      df_orders.duplicated().sum())

#3. Check duplicate order_id (khac noi dung van tinh la trung)
print("Duplicate order_id:",
      df_orders["order_id"].duplicated().sum())

#4. Check data type
print("\nColumns data types:\n",
      df_orders.dtypes)

#5. Check order date --> NaT
od = pd.to_datetime(
    df_orders["order_date"], errors="coerce"
)
print("\nInvalid order_date:", od.isna().sum())

#6. Check future order date
print("Future order_date:", (od > TODAY).sum())

#7. Check Referential Integrity - Customer IDs
valid_customer_id = set(df_customers["customer_id"])
invalid_customer_orders = df_orders[~df_orders["customer_id"].isin(valid_customer_id)]
print("Number of orders with invalid customer IDs:", len(invalid_customer_orders))

print("\n=============CHECKING TABLE ORDER_ITEMS=================")

#1. Check Missing data
print("\nMissing values:\n",
      df_order_items.isna().sum())

#2. Check duplicate rows
print("\nDuplicate rows:",
      df_order_items.duplicated().sum())

#3. Check data type
print("\nColumns data types:\n",
      df_order_items.dtypes)

#4. Check non-numeric / negative values
oi_price = pd.to_numeric(df_order_items["unit_price"], errors="coerce")
oi_cost = pd.to_numeric(df_order_items["cost"], errors="coerce")
oi_qty = pd.to_numeric(df_order_items["quantity"], errors="coerce")
print("\nNon-numeric unit_price:", oi_price.isna().sum())
print("Non-numeric cost:", oi_cost.isna().sum())
print("Non-numeric quantity:", oi_qty.isna().sum())
print("Negative unit_price:", (oi_price < 0).sum())
print("Negative cost:", (oi_cost < 0).sum())

#5. Check quantity <= 0
print("Number of rows with quantity <= 0:", (oi_qty <= 0).sum())

#6. Check Referential Integrity - Order IDs
valid_order_id = set(df_orders["order_id"])
order_id_exists_in_orders = df_order_items[~df_order_items["order_id"].isin(valid_order_id)]
print(
    "Number of order items with invalid order IDs:",
    len(order_id_exists_in_orders)
)

#7. Check Referential Integrity - Product IDs
valid_product_ids = set(df_products["product_id"])

product_id_exists_in_products = (
    df_order_items["product_id"].isin(valid_product_ids)
)
invalid_product_items = df_order_items[~product_id_exists_in_products]
print(
    "Number of order items with invalid product IDs:",
    len(invalid_product_items)
)

#==============================================
# PART 2: DATA CLEANING
#==============================================
print("\n##############################################")
print("# PART 2: DATA CLEANING")
print("##############################################")

#------------------------------------------
# CLEAN CUSTOMERS
#------------------------------------------
print("\n[1/4] Cleaning the customer table")

#1. Drop duplicate
before_customer = len(df_customers)
df_customers = df_customers.drop_duplicates(subset=["customer_id"], keep="first")
after_customer = len(df_customers)
print(f"Removed {before_customer - after_customer:,} duplicate rows")

#2. Missing data (gom ca chuoi rong / toan khoang trang)
text_cols = ["phone", "gender", "city"]
df_customers[text_cols] = (
    df_customers[text_cols]
    .replace(r"^\s*$", pd.NA, regex=True)
    .fillna("N/A")
)

#3. Fix date of birth
df_customers["date_of_birth"] = pd.to_datetime(
    df_customers["date_of_birth"], errors="coerce"
)

#4. Future date of birth --> NaT 
future_dob = df_customers["date_of_birth"] > TODAY
print(f"Set {future_dob.sum():,} future date_of_birth to NaT")
df_customers.loc[future_dob, "date_of_birth"] = pd.NaT

#------------------------------------------
# CLEAN PRODUCTS
#------------------------------------------
print("\n[2/4] Cleaning the Product table")

#1. Drop duplicate
before_product = len(df_products)
df_products = df_products.drop_duplicates(subset=["product_id"], keep="first")
after_product = len(df_products)
print(f"Removed {before_product - after_product:,} duplicate rows")

#2. Fix data type
df_products["unit_price"] = pd.to_numeric(df_products["unit_price"], errors="coerce")
df_products["unit_cost"] = pd.to_numeric(df_products["unit_cost"], errors="coerce")

#3. Remove rows with missing price / cost
before = len(df_products)
df_products = df_products.dropna(subset=["unit_price", "unit_cost"])
print(f"Removed {before - len(df_products):,} rows with missing unit_price/unit_cost")

#4. Remove rows with negative price / cost
before = len(df_products)
df_products = df_products[
    (df_products["unit_price"] >= 0) & (df_products["unit_cost"] >= 0)
]
print(f"Removed {before - len(df_products):,} rows with negative unit_price/unit_cost")

#5. Remove rows with unit_cost > unit_price
before = len(df_products)
df_products = df_products[
    df_products["unit_cost"] <= df_products["unit_price"]
]
print(f"Removed {before - len(df_products):,} rows with unit_cost > unit_price")

#------------------------------------------
# CLEAN ORDERS
#------------------------------------------
print("\n[3/4] Cleaning the Order table")

#1. Drop duplicate rows
before_order = len(df_orders)
df_orders = df_orders.drop_duplicates()
after_order = len(df_orders)
print(f"Removed {before_order - after_order:,} duplicate rows")

#2. Drop duplicate order_id (cung order_id nhung khac noi dung)
before = len(df_orders)
df_orders = df_orders.drop_duplicates(subset=["order_id"], keep="first")
print(f"Removed {before - len(df_orders):,} duplicate order_id")

#3. Fix data type order_date
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"], errors="coerce")

#4. Remove rows with invalid order_date (NaT)
before = len(df_orders)
df_orders = df_orders.dropna(subset=["order_date"])
print(f"Removed {before - len(df_orders):,} rows with invalid order_date")

#5. Remove rows with future order_date
before = len(df_orders)
df_orders = df_orders[df_orders["order_date"] <= TODAY]
print(f"Removed {before - len(df_orders):,} rows with future order_date")

#6. Remove rows with invalid customer IDs
valid_customer_ids = set(df_customers["customer_id"])

before = len(df_orders)
df_orders = df_orders[
    df_orders["customer_id"].isin(valid_customer_ids)
]
print(f"Removed {before - len(df_orders):,} rows with invalid customer IDs")

#------------------------------------------
# CLEAN ORDER ITEMS
#------------------------------------------
print("\n[4/4] Cleaning the Order item table")

#1. Remove duplicate rows
before_order_item = len(df_order_items)
df_order_items = df_order_items.drop_duplicates()
after_order_item = len(df_order_items)
print(f"Removed {before_order_item - after_order_item:,} duplicate rows")

#2. Fix data type
df_order_items["unit_price"] = pd.to_numeric(df_order_items["unit_price"], errors="coerce")
df_order_items["cost"] = pd.to_numeric(df_order_items["cost"], errors="coerce")
df_order_items["quantity"] = pd.to_numeric(df_order_items["quantity"], errors="coerce")

#3. Remove rows with missing price / cost / quantity
before = len(df_order_items)
df_order_items = df_order_items.dropna(subset=["unit_price", "cost", "quantity"])
print(f"Removed {before - len(df_order_items):,} rows with missing unit_price/cost/quantity")

#4. Remove rows with negative price / cost
before = len(df_order_items)
df_order_items = df_order_items[
    (df_order_items["unit_price"] >= 0) & (df_order_items["cost"] >= 0)
]
print(f"Removed {before - len(df_order_items):,} rows with negative unit_price/cost")

#5. Remove rows with quantity <= 0
before = len(df_order_items)
df_order_items = df_order_items[
    df_order_items["quantity"] > 0
]
print(f"Removed {before - len(df_order_items):,} rows with quantity <= 0")

#6. Remove rows with invalid order IDs
valid_order_ids = set(df_orders["order_id"])

before = len(df_order_items)
df_order_items = df_order_items[
    df_order_items["order_id"].isin(valid_order_ids)
]
print(f"Removed {before - len(df_order_items):,} rows with invalid order IDs")

#7. Remove rows with invalid product IDs
valid_product_ids = set(df_products["product_id"])

before = len(df_order_items)
df_order_items = df_order_items[
    df_order_items["product_id"].isin(valid_product_ids)
]
print(f"Removed {before - len(df_order_items):,} rows with invalid product IDs")

print("Rows after cleaning:", len(df_order_items))

#==============================================
# PART 3: VALIDATE CLEAN DATA
#==============================================
print("\n##############################################")
print("# PART 3: VALIDATE CLEAN DATA")
print("##############################################\n")

checks = {
    "customers: duplicate customer_id": df_customers["customer_id"].duplicated().sum(),
    "customers: missing phone/gender/city": df_customers[text_cols].isna().sum().sum(),
    "customers: future date_of_birth": (df_customers["date_of_birth"] > TODAY).sum(),
    "products: duplicate product_id": df_products["product_id"].duplicated().sum(),
    "products: missing price/cost": df_products[["unit_price", "unit_cost"]].isna().sum().sum(),
    "products: cost > price": (df_products["unit_cost"] > df_products["unit_price"]).sum(),
    "orders: duplicate order_id": df_orders["order_id"].duplicated().sum(),
    "orders: invalid order_date": df_orders["order_date"].isna().sum(),
    "orders: future order_date": (df_orders["order_date"] > TODAY).sum(),
    "orders: invalid customer_id": (~df_orders["customer_id"].isin(set(df_customers["customer_id"]))).sum(),
    "order_items: duplicate rows": df_order_items.duplicated().sum(),
    "order_items: missing price/cost/quantity": df_order_items[["unit_price", "cost", "quantity"]].isna().sum().sum(),
    "order_items: quantity <= 0": (df_order_items["quantity"] <= 0).sum(),
    "order_items: invalid order_id": (~df_order_items["order_id"].isin(set(df_orders["order_id"]))).sum(),
    "order_items: invalid product_id": (~df_order_items["product_id"].isin(set(df_products["product_id"]))).sum(),
}

all_ok = True
for name, value in checks.items():
    status = "OK  " if value == 0 else "FAIL"
    if value != 0:
        all_ok = False
    print(f"[{status}] {name}: {value}")

assert all_ok, "Clean data van con loi, kiem tra lai ket qua o tren truoc khi luu!"

#==============================================
# PART 4: SAVE CLEAN DATA
#==============================================
print("\n##############################################")
print("# PART 4: SAVE CLEAN DATA")
print("##############################################\n")

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
