import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path(__file__).resolve().parent / "churn_predictions.db"


def get_connection():
    """Create and return a database connection."""

    return sqlite3.connect(DATABASE_PATH)


def create_database():
    """Create the predictions table if it does not already exist."""

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                customer_id INTEGER,
                gender TEXT,
                senior_citizen INTEGER,
                partner TEXT,
                dependents TEXT,
                tenure INTEGER,
                phone_service TEXT,
                multiple_lines TEXT,
                internet_service TEXT,
                online_security TEXT,
                online_backup TEXT,
                device_protection TEXT,
                tech_support TEXT,
                streaming_tv TEXT,
                streaming_movies TEXT,
                contract TEXT,
                paperless_billing TEXT,
                payment_method TEXT,
                monthly_charges REAL,
                total_charges REAL,
                prediction INTEGER,
                prediction_result TEXT,
                churn_probability REAL,
                risk_category TEXT,
                recommendation_title TEXT,
                recommendation_message TEXT,
                prediction_date TEXT
            )
            """
        )

        connection.commit()


def save_prediction(
    username,
    customer,
    prediction,
    probability,
    risk,
    recommendation
):
    """Save a completed churn prediction."""

    prediction_result = (
        "Likely to Churn"
        if prediction == 1
        else "Likely to Stay"
    )

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO predictions (
                username,
                customer_id,
                gender,
                senior_citizen,
                partner,
                dependents,
                tenure,
                phone_service,
                multiple_lines,
                internet_service,
                online_security,
                online_backup,
                device_protection,
                tech_support,
                streaming_tv,
                streaming_movies,
                contract,
                paperless_billing,
                payment_method,
                monthly_charges,
                total_charges,
                prediction,
                prediction_result,
                churn_probability,
                risk_category,
                recommendation_title,
                recommendation_message,
                prediction_date
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                username,
                customer["id"],
                customer["gender"],
                customer["SeniorCitizen"],
                customer["Partner"],
                customer["Dependents"],
                customer["tenure"],
                customer["PhoneService"],
                customer["MultipleLines"],
                customer["InternetService"],
                customer["OnlineSecurity"],
                customer["OnlineBackup"],
                customer["DeviceProtection"],
                customer["TechSupport"],
                customer["StreamingTV"],
                customer["StreamingMovies"],
                customer["Contract"],
                customer["PaperlessBilling"],
                customer["PaymentMethod"],
                customer["MonthlyCharges"],
                customer["TotalCharges"],
                int(prediction),
                prediction_result,
                float(probability),
                risk,
                recommendation["title"],
                recommendation["message"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        connection.commit()


def load_predictions():
    """Load saved predictions from the database."""

    with get_connection() as connection:
        return pd.read_sql_query(
            """
            SELECT
                prediction_id AS "Prediction ID",
                prediction_date AS "Date",
                username AS "User",
                gender AS "Gender",
                tenure AS "Tenure",
                contract AS "Contract",
                internet_service AS "Internet Service",
                monthly_charges AS "Monthly Charges",
                total_charges AS "Total Charges",
                prediction_result AS "Prediction",
                ROUND(churn_probability * 100, 2)
                    AS "Churn Probability (%)",
                risk_category AS "Risk"
            FROM predictions
            ORDER BY prediction_id DESC
            """,
            connection
        )


def delete_all_predictions():
    """Delete all saved prediction records."""

    with get_connection() as connection:
        connection.execute("DELETE FROM predictions")
        connection.commit()