import pandas as pd
import numpy as np

np.random.seed(42)

# ---------------------------------------------------------
# 1. Create monthly dates
# ---------------------------------------------------------

dates = pd.date_range(
    start="2021-01-01",
    end="2026-08-01",
    freq="MS"
)

n = len(dates)

# ---------------------------------------------------------
# 2. Create seasonal pattern
# ---------------------------------------------------------

month = dates.month

seasonality = np.where(
    month.isin([1, 2, 3]),
    1.05,
    np.where(
        month.isin([4, 5, 6]),
        0.98,
        np.where(
            month.isin([7, 8, 9]),
            1.02,
            1.08
        )
    )
)

# ---------------------------------------------------------
# 3. Premium generation
# ---------------------------------------------------------

trend = np.linspace(85, 155, n)

noise = np.random.normal(0, 4, n)

premium = trend * seasonality + noise

# Add a few realistic slow-down periods
premium[28:34] -= 8
premium[48:52] -= 12
premium[62:66] -= 7

premium = np.maximum(premium, 50)

# ---------------------------------------------------------
# 4. Number of policies
# ---------------------------------------------------------

policy_trend = np.linspace(7000, 12500, n)

policy_noise = np.random.normal(0, 250, n)

policies = (
    policy_trend
    + policy_noise
    + (premium - premium.mean()) * 12
)

policies = np.maximum(policies, 4000).astype(int)

# ---------------------------------------------------------
# 5. Customers
# ---------------------------------------------------------

customer_noise = np.random.normal(0, 180, n)

customers = (
    policies * 0.82
    + customer_noise
)

customers = np.maximum(customers, 3000).astype(int)

# ---------------------------------------------------------
# 6. Claims
# ---------------------------------------------------------

claims_ratio = np.random.normal(
    0.58,
    0.045,
    n
)

# Create a few high-claims periods
claims_ratio[35:40] += 0.08
claims_ratio[55:60] += 0.06

claims_ratio = np.clip(
    claims_ratio,
    0.45,
    0.78
)

claims = premium * claims_ratio

# ---------------------------------------------------------
# 7. Build dataframe
# ---------------------------------------------------------

df = pd.DataFrame({
    "Date": dates,
    "Premium_Million": premium.round(2),
    "Claims_Million": claims.round(2),
    "Policies": policies,
    "Customers": customers
})

# ---------------------------------------------------------
# 8. Add calculated business KPIs
# ---------------------------------------------------------

df["Premium_Growth"] = (
    df["Premium_Million"]
    .pct_change()
    .fillna(0)
)

df["Policy_Growth"] = (
    df["Policies"]
    .pct_change()
    .fillna(0)
)

df["Customer_Growth"] = (
    df["Customers"]
    .pct_change()
    .fillna(0)
)

df["Claims_Ratio"] = (
    df["Claims_Million"]
    / df["Premium_Million"]
)

df["Premium_Per_Policy"] = (
    df["Premium_Million"] * 1_000_000
    / df["Policies"]
)

# ---------------------------------------------------------
# 9. Save dataset
# ---------------------------------------------------------

output_path = "data/raw/insurance_business.csv"

df.to_csv(
    output_path,
    index=False
)

print("Dataset created successfully.")
print(f"Rows: {len(df)}")
print(f"Saved to: {output_path}")
print()
print(df.head())