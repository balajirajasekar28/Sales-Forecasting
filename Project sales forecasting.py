from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


# 1 Database Connection using SQLAlchemy
engine = create_engine("mysql+pymysql://root:root@localhost/project_sales_forecasting")

# Read directly using pandas
query = "SELECT * FROM BI_sales_dashboard;"
df = pd.read_sql(query, engine)

# 2 Basic Data Overview

print("\n--- Data Preview ---")
print(df.head())

print("\n--- Data Info ---")
print(df.info())

print("\n--- Missing Values ---")
print(df.isnull().sum())

# 3 Data Cleaning

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.fillna(0, inplace=True)

# Convert date column
df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")


# 4️⃣ Exploratory Data Analysis (EDA)

# Total sales by category
category_sales = df.groupby("category")["total_amount"].sum().sort_values(ascending=False)
plt.figure(figsize=(7,4))
category_sales.plot(kind="bar", color="skyblue")
plt.title("Total Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales (Rs)")
plt.show()

#  Monthly sales trend
df["month"] = df["sale_date"].dt.to_period("M")
monthly_sales = df.groupby("month")["total_amount"].sum()
plt.figure(figsize=(8,4))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales (Rs)")
plt.show()

# City-wise total sales
plt.figure(figsize=(8,5))
sns.barplot(
    x="city",
    y="total_amount",
    data=df,
    estimator=sum,
    errorbar=None,     # replaces deprecated 'ci=None'
    hue="city",
    palette="viridis",
    legend=False
)
plt.title("City-wise Total Sales")
plt.xlabel("City")
plt.ylabel("Total Sales (Rs)")
plt.show()

# 5 Simple Prediction Model (Optional)


# Predict total sales based on quantity sold
df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")

X = df[["quantity_sold"]]
y = df["total_amount"]

model = LinearRegression()
model.fit(X, y)

# Predict sales for a given quantity
new_data = pd.DataFrame([[5]], columns=["quantity_sold"])
predicted_sales = model.predict(new_data)
print(f"\nPredicted Sales for 5 Units: Rs {predicted_sales[0]:.2f}")


# 6 Save Cleaned Data

df.to_csv("Sales_Cleaned_Data.csv", index=False)
print("\n Data saved successfully as 'Sales_Cleaned_Data.csv'")
