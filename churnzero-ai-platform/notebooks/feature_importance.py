import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
# TRAIN MODEL
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

model.fit(X_train, y_train)

# -----------------------------------
# FEATURE IMPORTANCE
# -----------------------------------

importance = model.feature_importances_

feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
})

feature_importance_df = feature_importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\n========== TOP 20 IMPORTANT FEATURES ==========\n")

print(feature_importance_df.head(20))

# -----------------------------------
# PLOT
# -----------------------------------

top_features = feature_importance_df.head(15)

plt.figure(figsize=(10,8))

sns.barplot(
    x="Importance",
    y="Feature",
    data=top_features
)

plt.title("Top 15 Important Features")

plt.tight_layout()

plt.show()