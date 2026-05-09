"""
Sample Dataset Generator for Credit Card Fraud Detection
"""
import pandas as pd
import numpy as np

# Generate a synthetic dataset with 1000 transactions
np.random.seed(42)
n_samples = 1000

data = {
    'Transaction_Amount': np.random.uniform(5.0, 5000.0, n_samples),
    'Distance_From_Home': np.random.uniform(0.1, 1000.0, n_samples),
    'Distance_From_Last_Transaction': np.random.uniform(0.1, 500.0, n_samples),
    'Ratio_To_Median_Purchase_Price': np.random.uniform(0.5, 10.0, n_samples),
    'Used_Chip': np.random.choice([0, 1], n_samples),
    'Used_Pin_Number': np.random.choice([0, 1], n_samples),
    'Online_Order': np.random.choice([0, 1], n_samples),
}

df = pd.DataFrame(data)

# Create a simple rule to simulate fraud: 
# If it's online, amount is high, and distance is high, it's more likely fraud.
fraud_probability = (
    (df['Transaction_Amount'] > 1000).astype(int) + 
    (df['Distance_From_Home'] > 100).astype(int) + 
    (df['Online_Order'] == 1).astype(int)
)

# Assign 'Is_Fraud' based on the combined conditions
df['Is_Fraud'] = (fraud_probability >= 2).astype(int)

# Introduce some missing values randomly to test our missing value handler
for col in ['Transaction_Amount', 'Distance_From_Home']:
    missing_indices = np.random.choice(df.index, size=10, replace=False)
    df.loc[missing_indices, col] = np.nan

# Save to CSV
df.to_csv('credit_card_data.csv', index=False)
print("Sample dataset 'credit_card_data.csv' created successfully with 1000 rows.")
