import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv("dataset/ChurnZero_dataset_v1.csv")

# -----------------------------------
# BASIC INFORMATION
# -----------------------------------

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")

missing_values = df.isnull().sum()

print(missing_values[missing_values > 0])

# -----------------------------------
# TARGET DISTRIBUTION
# -----------------------------------

target_col = "churn"

print("\n========== TARGET DISTRIBUTION ==========")

print(df[target_col].value_counts())

plt.figure(figsize=(6, 4))

sns.countplot(x=df[target_col])

plt.title("Churn Distribution")

plt.show()

# -----------------------------------
# NUMERICAL COLUMNS
# -----------------------------------

numeric_cols = df.select_dtypes(include=np.number).columns

print("\n========== NUMERICAL COLUMNS ==========")

print(numeric_cols)

# -----------------------------------
# CATEGORICAL COLUMNS
# -----------------------------------

categorical_cols = df.select_dtypes(include="object").columns

print("\n========== CATEGORICAL COLUMNS ==========")

print(categorical_cols)

# -----------------------------------
# CORRELATION HEATMAP
# -----------------------------------

plt.figure(figsize=(14, 10))

correlation = df[numeric_cols].corr()

sns.heatmap(
    correlation,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")

plt.show()

# -----------------------------------
# CHURN BY GENDER
# -----------------------------------

if "gender" in df.columns:

    plt.figure(figsize=(6, 4))

    sns.countplot(
        x="gender",
        hue=target_col,
        data=df
    )

    plt.title("Churn by Gender")

    plt.show()

# -----------------------------------
# IMPORTANT FEATURE DISTRIBUTIONS
# -----------------------------------

important_features = [
    "age",
    "annual_income",
    "avg_monthly_balance",
    "tenure_months"
]

for feature in important_features:

    if feature in df.columns:

        plt.figure(figsize=(6, 4))

        sns.histplot(
            df[feature],
            kde=True
        )

        plt.title(f"Distribution of {feature}")

        plt.show()

print("\nEDA COMPLETED SUCCESSFULLY")