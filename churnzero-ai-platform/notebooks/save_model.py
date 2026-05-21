import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier

# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("dataset/ChurnZero_dataset_v1.csv")

target_col = "churn"

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
# LABEL ENCODING
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
# SAVE MODEL
# -----------------------------------

joblib.dump(model, "xgboost_churn_model.pkl")

# Save scaler
joblib.dump(scaler, "scaler.pkl")

# Save imputers
joblib.dump(num_imputer, "num_imputer.pkl")

joblib.dump(cat_imputer, "cat_imputer.pkl")

# Save encoders
joblib.dump(label_encoders, "label_encoders.pkl")

print("\nFILES SAVED SUCCESSFULLY")

print("\nSaved Files:")
print("xgboost_churn_model.pkl")
print("scaler.pkl")
print("num_imputer.pkl")
print("cat_imputer.pkl")
print("label_encoders.pkl")