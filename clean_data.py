import pandas as pd
import numpy as np

# reading csv.
df = pd.read_csv("payscale_salaries.csv")

# cleaning the dataframe.
df.replace("-", np.nan, inplace=True)
df.dropna(inplace=True)

salary_cols = ["Early Career Pay", "Mid-Career Pay"]
for col in salary_cols:
    df[col] = df[col].str.replace("$", "", regex=False)
    df[col] = df[col].str.replace(",", "", regex=False)
    df[col] = df[col].astype(float)

df["% High Mean"] = df["% High Mean"].str.replace("%", "", regex=False).astype(float)
# saving the dataframe to csv.
df.to_csv("payscale_cleaned.csv", index=False)
print("Cleaned data saved ✅")