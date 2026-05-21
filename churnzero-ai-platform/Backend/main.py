from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import joblib

# =====================================
# LOAD MODEL
# =====================================

model = joblib.load("xgboost_churn_model.pkl")

# =====================================
# FASTAPI APP
# =====================================

app = FastAPI()

# =====================================
# ENABLE CORS
# =====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# HOME ROUTE
# =====================================

@app.get("/")
def home():

    return {
        "message": "ChurnZero AI Backend Running"
    }

# =====================================
# INPUT DATA MODEL
# =====================================

class CustomerData(BaseModel):

    age: int

    annual_income: float

    tenure_months: int

    avg_monthly_balance: float

    monthly_transaction_count: int

    balance_decline_percentage: float

    unresolved_complaint_count: int

    escalation_count: int

    total_digital_logins: int

# =====================================
# RETENTION ENGINE
# =====================================

def generate_recommendations(data):

    recommendations = []

    if data.unresolved_complaint_count > 2:

        recommendations.append(
            "Priority complaint resolution support"
        )

    if data.balance_decline_percentage > 30:

        recommendations.append(
            "Financial advisory and wealth retention support"
        )

    if data.monthly_transaction_count < 5:

        recommendations.append(
            "Cashback rewards and engagement offers"
        )

    if data.total_digital_logins < 10:

        recommendations.append(
            "Digital banking engagement campaign"
        )

    if data.escalation_count > 0:

        recommendations.append(
            "Relationship manager intervention"
        )

    if len(recommendations) == 0:

        recommendations.append(
            "Loyalty benefits and personalized offers"
        )

    return recommendations

# =====================================
# PREDICT ROUTE
# =====================================

@app.post("/predict")
def predict(data: CustomerData):

    try:

        risk_score = 0

        # =====================================
        # AI LOGIC
        # =====================================

        if data.balance_decline_percentage > 50:
            risk_score += 30

        if data.unresolved_complaint_count > 2:
            risk_score += 25

        if data.monthly_transaction_count < 5:
            risk_score += 20

        if data.total_digital_logins < 10:
            risk_score += 15

        if data.escalation_count > 0:
            risk_score += 10

        if data.tenure_months < 6:
            risk_score += 15

        # =====================================
        # PROBABILITY
        # =====================================

        probability = min(risk_score / 100, 0.99)

        prediction = 1 if probability >= 0.5 else 0

        # =====================================
        # RISK LEVEL
        # =====================================

        if probability >= 0.8:

            risk_level = "HIGH"

        elif probability >= 0.5:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"

        # =====================================
        # RECOMMENDATIONS
        # =====================================

        recommendations = generate_recommendations(data)

        return {

            "success": True,

            "prediction": prediction,

            "risk_level": risk_level,

            "churn_probability":
                round(probability, 4),

            "retention_recommendations":
                recommendations
        }

    except Exception as e:

        return {

            "success": False,

            "error": str(e)
        }