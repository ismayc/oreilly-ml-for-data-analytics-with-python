import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('telco-customer-churn_ORIGINAL.csv')

# Add in 6% of missing values to MonthlyCharges column
np.random.seed(2025)
missing_indices = np.random.choice(df.index, size=int(len(df) * 0.06), replace=False)
df.loc[missing_indices, 'MonthlyCharges'] = np.nan

# Encode service columns as binary
service_cols = [
    'PhoneService', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'
]

for col in service_cols:
    df[col] = df[col].map({'Yes': 1, 'No': 0, 'No internet service': 0, 'No phone service': 0}).astype(int)

df['ServiceCount'] = df[service_cols].sum(axis=1)

# Add Internet score
df['InternetScore'] = df['InternetService'].map({'Fiber optic': 40, 'DSL': 20, 'No': 0})

# Stronger functional link: tie engagement score directly to MonthlyCharges logic
# Higher charges → almost always due to more services, tenure, and Internet type
df['AvgServiceUsageScore'] = (
    df['MonthlyCharges'] * 0.05  # **direct linear dependence**
    + df['ServiceCount'] * 2     # services still matter slightly
    + df['InternetScore'] * 0.3  # Internet type adds a small weight
    + np.random.normal(0, 4, len(df))  # tiny noise
).clip(0, 100)

# Add in 6% of missing values to MonthlyCharges column (plus 3% to AvgServiceUsageScore)
missing_indices = np.random.choice(df.index, size=int(len(df) * 0.03), replace=False)
df.loc[missing_indices, 'AvgServiceUsageScore'] = np.nan

# Move 'Churn' column to the end
churn_col = df.pop('Churn')  # removes 'Churn' and stores it temporarily
df['Churn'] = churn_col      # re-inserts it at the end

# Write the modified DataFrame to a new CSV file
df.to_csv('telco-customer-churn.csv', index=False)
