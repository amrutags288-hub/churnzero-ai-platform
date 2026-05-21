import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("dataset/ChurnZero_dataset_v1.csv")

# -----------------------------------
# TARGET COLUMN
# -----------------------------------

target_col = "churn"

# -----------------------------------
# FEATURES AND TARGET
# -----------------------------------

X = df.drop(columns=[target_col])

y = df[target_col]

# -----------------------------------
# STORE ORIGINAL DATA
# -----------------------------------

original_df = X.copy()

# -----------------------------------
# COLUMN TYPES
# -----------------------------------

categorical_cols = X.select_dtypes(include="object").columns

numerical_cols = X.select_dtypes(include=np.number).columns

# -----------------------------------
# HANDLE MISSING VALUES
# -----------------------------------

num_imputer = SimpleImputer(strategy="median")

X[numerical_cols] = num_imputer.fit_transform(
    X[numerical_cols]
)

cat_imputer = SimpleImputer(strategy="most_frequent")

X[categorical_cols] = cat_imputer.fit_transform(
    X[categorical_cols]
)

# -----------------------------------
# LABEL ENCODING
# -----------------------------------

for col in categorical_cols:

    le = LabelEncoder()

    X[col] = le.fit_transform(X[col])

# -----------------------------------
# FEATURE SCALING
# -----------------------------------

scaler = StandardScaler()

X[numerical_cols] = scaler.fit_transform(
    X[numerical_cols]
)

# -----------------------------------
# TRAIN TEST SPLIT
# -----------------------------------

X_train, X_valid, y_train, y_valid = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------------
# MODEL
# -----------------------------------

model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric="logloss"
)

# -----------------------------------
# TRAIN MODEL
# -----------------------------------

print("\nTRAINING MODEL...\n")

model.fit(X_train, y_train)

print("MODEL TRAINED SUCCESSFULLY")

# -----------------------------------
# CHURN PROBABILITY
# -----------------------------------

churn_probabilities = model.predict_proba(X_valid)[:, 1]

# -----------------------------------
# CREATE RESULTS DATAFRAME
# -----------------------------------

results = original_df.iloc[X_valid.index].copy()

results["churn_probability"] = churn_probabilities

# -----------------------------------
# RISK LEVEL
# -----------------------------------

def risk_level(prob):

    if prob >= 0.8:
        return "HIGH"

    elif prob >= 0.5:
        return "MEDIUM"

    else:
        return "LOW"

results["risk_level"] = results[
    "churn_probability"
].apply(risk_level)

# -----------------------------------
# RETENTION RECOMMENDATION ENGINE
# -----------------------------------

def generate_recommendation(row):

    recommendations = []

    # Complaint based
    if row.get("unresolved_complaint_count", 0) > 1:
        recommendations.append(
            "Priority complaint resolution"
        )

    # Low engagement
    if row.get("total_digital_logins", 0) < 20:
        recommendations.append(
            "Digital engagement campaign"
        )

    # Balance decline
    if row.get("balance_decline_percentage", 0) > 20:
        recommendations.append(
            "Financial advisory support"
        )

    # Low transaction activity
    if row.get("monthly_transaction_count", 0) < 10:
        recommendations.append(
            "Cashback and rewards offer"
        )

    # Escalations
    if row.get("escalation_count", 0) > 0:
        recommendations.append(
            "Relationship manager intervention"
        )

    # Default fallback
    if len(recommendations) == 0:
        recommendations.append(
            "Personalized loyalty benefits"
        )

    return " | ".join(recommendations)

results["retention_strategy"] = results.apply(
    generate_recommendation,
    axis=1
)

# -----------------------------------
# HIGH RISK CUSTOMERS
# -----------------------------------

high_risk = results[
    results["risk_level"] == "HIGH"
]

# -----------------------------------
# DISPLAY RESULTS
# -----------------------------------

print("\n========== HIGH RISK CUSTOMERS ==========\n")

display_cols = [
    "customer_id",
    "churn_probability",
    "risk_level",
    "retention_strategy"
]

print(
    high_risk[display_cols]
    .head(20)
)

# -----------------------------------
# SAVE RESULTS
# -----------------------------------

high_risk.to_csv(
    "high_risk_customers.csv",
    index=False
)

print("\nFILE SAVED:")
print("high_risk_customers.csv")

print("\nRETENTION ENGINE COMPLETED")