import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv("dataset/ChurnZero_dataset_v1.csv")

print("\nDATASET SHAPE:")
print(df.shape)

# -----------------------------------
# TARGET COLUMN
# -----------------------------------

target_col = "churn"

# -----------------------------------
# SEPARATE FEATURES AND TARGET
# -----------------------------------

X = df.drop(columns=[target_col])

y = df[target_col]

# -----------------------------------
# IDENTIFY COLUMN TYPES
# -----------------------------------

categorical_cols = X.select_dtypes(include="object").columns

numerical_cols = X.select_dtypes(include=np.number).columns

print("\nCATEGORICAL COLUMNS:")
print(categorical_cols)

print("\nNUMERICAL COLUMNS:")
print(numerical_cols)

# -----------------------------------
# HANDLE MISSING VALUES
# -----------------------------------

# Numerical missing values
num_imputer = SimpleImputer(strategy="median")

X[numerical_cols] = num_imputer.fit_transform(
    X[numerical_cols]
)

# Categorical missing values
cat_imputer = SimpleImputer(strategy="most_frequent")

X[categorical_cols] = cat_imputer.fit_transform(
    X[categorical_cols]
)

print("\nMISSING VALUES HANDLED")

# -----------------------------------
# LABEL ENCODING
# -----------------------------------

label_encoders = {}

for col in categorical_cols:

    le = LabelEncoder()

    X[col] = le.fit_transform(X[col])

    label_encoders[col] = le

print("\nCATEGORICAL VARIABLES ENCODED")

# -----------------------------------
# FEATURE SCALING
# -----------------------------------

scaler = StandardScaler()

X[numerical_cols] = scaler.fit_transform(
    X[numerical_cols]
)

print("\nFEATURE SCALING COMPLETED")

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

print("\nTRAIN SHAPE:")
print(X_train.shape)

print("\nVALIDATION SHAPE:")
print(X_valid.shape)

print("\nPREPROCESSING COMPLETED SUCCESSFULLY")