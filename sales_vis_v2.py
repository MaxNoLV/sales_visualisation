import pandas as pd
import numpy as np

df = pd.read_csv("sales_data_ready.csv")
df.head(2)

df["shipped_quantity"].value_counts().get(0, 0)
(df["shipped_quantity"] < 0).sum()


description_map = (
    df.loc[df["unit_price"].notna() & (df["unit_price"] != 0)]
    .drop_duplicates("item_id")
    .set_index("item_id")["unit_price"]
    .to_dict()
)

df.loc[
    df["unit_price"].isnull(),
    "item_id",
] = df["item_id"].map(description_map)
