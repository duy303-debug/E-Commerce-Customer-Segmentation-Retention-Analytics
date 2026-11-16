import pyodbc
import pandas as pd
import os

#------------------------------------------
# CONFIG
#------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PRE_DIR = os.path.join(PROJECT_ROOT, "data", "preprocessed")

# ------------------------------------------
# CONNECT TO SQL SERVER
# ------------------------------------------

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=ecommerce;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

cursor = conn.cursor()
print("Connected successfully!")

#------------------------------------------
# LOAD DATA
#------------------------------------------

df_customers = pd.read_csv(os.path.join(PRE_DIR,"customers_clean.csv"))

df_products = pd.read_csv(os.path.join(PRE_DIR,"products_clean.csv"))

df_orders = pd.read_csv(os.path.join(PRE_DIR,"orders_clean.csv"))

df_order_items = pd.read_csv(os.path.join(PRE_DIR,"order_items_clean.csv"))


# ------------------------------------------
# LOAD TABLE FUNCTION
# ------------------------------------------

def load_table(cursor, df, table_name):
    column_names = ", ".join(f"{col}" for col in df.columns)
    placeholders = ", ".join("?" for _ in df.columns)
    sql = f"INSERT INTO ec.{table_name} ({column_names}) VALUES ({placeholders})"

    cursor.fast_executemany = True
    cursor.executemany(sql,df.values.tolist())
    
    print(f"Loaded {len(df)} rows into {table_name}")

# ------------------------------------------
# EXECUTE LOAD
# ------------------------------------------

try:
    load_table(cursor, df_customers, "customers")
    load_table(cursor, df_products, "products")
    load_table(cursor, df_orders, "orders")
    load_table(cursor, df_order_items, "order_items")
    
    conn.commit()

except Exception:
    conn.rollback()
    raise

finally:
    cursor.close()
    conn.close()