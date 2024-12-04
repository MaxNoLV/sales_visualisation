import pandas as pd
import numpy as np

# Import data
file_path = "sales_dataset.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

df.columns = df.columns.str.lower()

len(df)

# Checking values ​​from two columns for complete identity
df["order_number"].equals(df["invoice_number"])

df.info()

# As data.info() doesn't always interpret empty strings or whitespace as null
# values I need to check for NaN values using another approach.

empty_or_whitespace_mask = df.map(
    lambda x: x.strip() == "" if isinstance(x, str) else False
)
empty_or_whitespace_count = empty_or_whitespace_mask.sum().sum()
print(
    "Total number of empty or whitespace-only entries in the DataFrame:",
    empty_or_whitespace_count,
)

df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

# Check for full duplicates in a dataset

duplicate_rows = df.duplicated(keep=False)
print("Number of duplicate rows in the Dataaset:", duplicate_rows.sum())

# Dropping unnecessary columns
# Renaming several columns and reordering

columns_to_drop = [
    "order_number",
    "shipment_number",
    "shipping_region_identifier",
    "shipping_region_code",
    "shipping_unit_measure",
    "shipping_pack_quantity",
    "item_unit_quantity",
    "item_section_module",
    "item_sequence",
    "item_stock_status",
    "shipping_region_name",
    "warehouse_identifier",
    "vendor_identifier",
    "vendor_city",
    "vendor_country",
    "vendor_address",
    "company_code",
    "company_number",
    "average_cost_price",
    "upc_number",
    "purchase_order_number",
    "cost_price",
]

df_columns = df.drop(columns_to_drop, axis=1)

df_columns.rename(
    columns={
        "item_number": "item_id",
        "company_identifier": "supplier_id",
        "customer_number": "customer_id",
        "company_name": "supplier_name",
        "invoice_amount": "unit_price",
    },
    inplace=True,
)

new_order = [
    "invoice_number",
    "invoice_date",
    "order_date",
    "order_type",
    "order_quantity",
    "shipped_quantity",
    "sales_amount",
    "unit_price",
    "customer_id",
    "customer_location",
    "customer_department",
    "customer_province",
    "item_id",
    "item_description",
    "item_department",
    "item_section",
    "item_group",
    "warehouse_number",
    "warehouse_name",
    "warehouse_region_name",
    "vendor_number",
    "vendor_name",
    "supplier_id",
    "supplier_name",
]

df_prepared = df_columns.reindex(columns=new_order)


df_prepared["customer_province"].value_counts(dropna=False)
