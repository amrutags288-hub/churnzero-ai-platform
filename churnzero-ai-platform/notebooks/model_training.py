import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    average_precision_score
)

from xgboost import XGBClassifier

# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv("dataset/ChurnZero_dataset_v1.csv")

target_col = "churn"

# -----------------------------------
# FEATURES AND TARGET
# -----------------------------------

X = df.drop(columns=[target_col])

y = df[target_col]

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
# ENCODE CATEGORICAL VARIABLES
# -----------------------------------

label_encoders = {}

for col in categorical_cols:

    le = LabelEncoder()

    X[col] = le.fit_transform(X[col])

    label_encoders[col] = le

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
# XGBOOST MODEL
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
# PREDICTIONS
# -----------------------------------

y_pred = model.predict(X_valid)

y_prob = model.predict_proba(X_valid)[:, 1]

# -----------------------------------
# EVALUATION
# -----------------------------------

print("\n========== F1 SCORE ==========")

f1 = f1_score(y_valid, y_pred)

print(f1)

print("\n========== PR-AUC SCORE ==========")

pr_auc = average_precision_score(
    y_valid,
    y_prob
)

print(pr_auc)

print("\n========== CONFUSION MATRIX ==========")

print(confusion_matrix(y_valid, y_pred))

print("\n========== CLASSIFICATION REPORT ==========")

print(classification_report(y_valid, y_pred))

# -----------------------------------
# BUSINESS COST ANALYSIS
# -----------------------------------

cm = confusion_matrix(y_valid, y_pred)

tn, fp, fn, tp = cm.ravel()

false_negative_cost = fn * 40000

false_positive_cost = fp * 500

total_cost = false_negative_cost + false_positive_cost

print("\n========== BUSINESS COST ==========")

print(f"False Negatives Cost: ₹{false_negative_cost}")

print(f"False Positives Cost: ₹{false_positive_cost}")

print(f"Total Business Cost: ₹{total_cost}")

print("\nMODEL TRAINING COMPLETED")