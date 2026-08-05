import os
import joblib
import pandas as pd

# ==========================================================
# LOAD TRAINED MODEL AND PREPROCESSOR
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "xgb_model.pkl")
PREPROCESSOR_PATH = os.path.join(PROJECT_ROOT, "models", "preprocessor.pkl")

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)


# ==========================================================
# CUSTOMER PREDICTION
# ==========================================================

def predict_customer(customer_information):

    customer_df = pd.DataFrame([customer_information])

    transformed_customer = preprocessor.transform(customer_df)

    prediction = model.predict(transformed_customer)[0]

    churn_probability = model.predict_proba(
        transformed_customer
    )[0][1]

    return prediction, churn_probability

def get_model():

    return model