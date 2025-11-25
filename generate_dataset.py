import pandas as pd
import numpy as np

# Random seed set karo (same data har baar)
np.random.seed(42)

# Kitne patients chahiye
n = 1000

print("Dataset Loading.....")

# Data generate karo
data = {
    'Age': np.random.randint(30, 80, n),
    'Gender': np.random.choice([0, 1], n),  # 0=Female, 1=Male
    'BP': np.random.randint(90, 180, n),
    'Cholesterol': np.random.randint(150, 300, n),
    'HeartRate': np.random.randint(60, 120, n),
    'Smoking': np.random.choice([0, 1], n),  # 0=No, 1=Yes
    'Diabetes': np.random.choice([0, 1], n),  # 0=No, 1=Yes
    'BMI': np.round(np.random.uniform(18, 40, n), 1)
}

df = pd.DataFrame(data)

# Risk calculate karo (simple logic)
risk_score = (
    (df['Age'] > 55) * 1 +
    (df['BP'] > 140) * 1 +
    (df['Cholesterol'] > 240) * 1 +
    (df['Smoking'] == 1) * 2 +
    (df['Diabetes'] == 1) * 1 +
    (df['BMI'] > 30) * 1
)

# Risk level assign karo
df['Risk'] = pd.cut(risk_score, bins=[-1, 2, 4, 10], labels=[0, 1, 2])

# Save karo
df.to_csv('heart_disease_data.csv', index=False)

print("✓ Dataset ready: heart_disease_data.csv")
print(f"Total patients: {len(df)}")
print("\nRisk distribution:")
print(df['Risk'].value_counts().sort_index())