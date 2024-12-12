import pandas as pd
import numpy as np

df = pd.read_csv("sales_data_ready.csv")
df.head(2)

len(df)  # 9963

df.info()

# Count unique invoixe_number values - 9854
len(pd.unique(df["invoice_number"]))

df["shipped_quantity"].value_counts().get(0, 0)
(df["shipped_quantity"] < 0).sum()

# Check for 0 values in each column

zero_invoice_rows = df[df["vendor_name"] == 0]

if not zero_invoice_rows.empty:
    print("Row indices with zero:", zero_invoice_rows.index.tolist())
else:
    print("No zero values.")

# Check do I have invoices hat contain both shipped_quantity values of 0 and
# values greater than 0 within the same invoice.
# I have 30 such invoices in my dataset


def contains_zero_and_positive(group):
    return (group == 0).any() and (group > 0).any()


mixed_invoice_mask = df.groupby("invoice_number")["shipped_quantity"].transform(
    contains_zero_and_positive
)

df[mixed_invoice_mask].drop_duplicates("invoice_number")

# Check do rows where 'shipped_quantity' is 0 are the same where 'unit_price'
# is 0 as well.

shipped_zero_indices = df[df["shipped_quantity"] == 0].index
unit_price_zero_indices = df[df["unit_price"] == 0].index
shipped_zero_indices.equals(unit_price_zero_indices)

# Check for strange 'invoice_number' values and export all these strange
# values into separate CSV file.

invalid_invoice_numbers = df[df["invoice_number"].apply(len) != 7][
    "invoice_number"
].tolist()

len(invalid_invoice_numbers)

strange_invoice_num__df = pd.DataFrame(
    invalid_invoice_numbers, columns=["invoice_number"]
)
strange_invoice_num__df.to_csv("strange_invoice_numbers.csv", index=False)

# Transform 'invoice_date' and 'order_date' values into datetime data type and
# saving file in Excel format.

df["invoice_date"] = pd.to_datetime(df["invoice_date"])
df["order_date"] = pd.to_datetime(df["order_date"])

df.to_csv("ready_data.csv", index=False)
