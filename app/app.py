import streamlit as st
import pandas as pd

from prediction import predict_customer
from utils import calculate_risk
from utils import business_recommendation

from database import (
    create_database,
    save_prediction,
    load_predictions,
    delete_all_predictions
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Telecom Customer Retention Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_database()
# ==========================================================
# LOGIN CONFIGURATION
# ==========================================================

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


def initialize_session():
    """Initialize login-related session variables."""

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""


def login_page():
    """Display the application login page."""

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        .login-title {
            text-align: center;
            color: #173F5F;
            font-size: 38px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .login-subtitle {
            text-align: center;
            color: #5A7184;
            font-size: 17px;
            margin-bottom: 30px;
        }

        .login-footer {
            text-align: center;
            color: #718096;
            font-size: 13px;
            margin-top: 25px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    left_space, login_column, right_space = st.columns([1.2, 1, 1.2])

    with login_column:

        st.markdown(
            '<div class="login-title">📡 Customer Retention System</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="login-subtitle">'
            'Secure access to the churn prediction dashboard'
            '</div>',
            unsafe_allow_html=True
        )

        with st.form("login_form"):

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_button:

            if username == VALID_USERNAME and password == VALID_PASSWORD:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login successful.")

                st.rerun()

            elif not username or not password:

                st.warning("Please enter both username and password.")

            else:

                st.error("Incorrect username or password.")

        st.markdown(
            '<div class="login-footer">'
            'Telecom Customer Retention Intelligence'
            '</div>',
            unsafe_allow_html=True
        )


def logout():
    """Log the current user out of the application."""

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()
initialize_session()

if not st.session_state.logged_in:
    login_page()
    st.stop()


# ==========================================================
# CUSTOM STYLE
# ==========================================================

st.markdown("""
<style>

.main{
    background:#F4F8FB;
}

.block-container{
    padding-top:1.4rem;
    padding-bottom:2rem;
    padding-left:2.8rem;
    padding-right:2.8rem;
}

h1,h2,h3{
    color:#173F5F;
}

[data-testid="stMetric"]{
    background:linear-gradient(135deg, #EAF4FF, #D7ECFF);
    border-radius:12px;
    padding:18px;
    border:1px solid #9CC7F0;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
}

[data-testid="stMetricLabel"]{
    color:#173F5F;
    font-weight:600;
}

[data-testid="stMetricValue"]{
    color:#0B5ED7;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📡 Navigation")

    st.success("Customer Retention Analytics")

    st.write(
        f"Logged in as: **{st.session_state.username}**"
    )

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        logout()

    st.markdown("---")

    st.write("### Workflow")

    st.write("① Customer Profile")
    st.write("② Service Portfolio")
    st.write("③ Subscription Details")
    st.write("④ Prediction Dashboard")
    st.write("⑤ Business Recommendation")

    st.markdown("---")

    st.info(
        """
This application predicts the likelihood
of customer churn using a trained
Extreme Gradient Boosting model.
"""
    )

# ==========================================================
# HEADER
# ==========================================================

st.title("📡 Telecom Customer Retention Intelligence")

st.caption(
    "Machine Learning Decision Support System for Customer Churn Prediction"
)

st.divider()

# ==========================================================
# CUSTOMER PROFILE
# ==========================================================

st.header("👤 Customer Profile")

left_profile, right_profile = st.columns(2)

with left_profile:

    customer_id = st.number_input(
     "Customer ID",
     min_value=1,
     value=100001,
     step=1
    )

    
    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        [0, 1],
        help="0 = No | 1 = Yes"
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

with right_profile:

    tenure = st.slider(
        "Customer Tenure (Months)",
        min_value=0,
        max_value=72,
        value=24
    )

    monthly_charges = st.number_input(
        "Monthly Charges ($)",
        min_value=0.0,
        value=72.50,
        step=1.25,
        format="%.2f"
    )

    total_charges = st.number_input(
        "Total Charges ($)",
        min_value=0.0,
        value=1850.00,
        step=25.00,
        format="%.2f"
    )

st.divider()


# ==========================================================
# SERVICE PORTFOLIO
# ==========================================================

st.header("📡 Service Portfolio")

left_service, right_service = st.columns(2)

with left_service:

    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["Fiber optic", "DSL", "No"]
    )

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )

with right_service:

    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    tech_support = st.selectbox(
        "Technical Support",
        ["Yes", "No", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )

st.divider()


# ==========================================================
# SUBSCRIPTION DETAILS
# ==========================================================

st.header("💳 Subscription Details")

left_subscription, right_subscription = st.columns(2)

with left_subscription:

    contract = st.selectbox(
        "Contract Type",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

    paperless = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

with right_subscription:

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Bank transfer (automatic)",
            "Credit card (automatic)",
            "Mailed check"
        ]
    )

st.divider()

# ==========================================================
# PREDICTION ENGINE
# ==========================================================

st.header("🚀 Prediction Engine")

st.write(
    "Click the button below to analyse the customer's likelihood of leaving the company."
)

analyse = st.button(
    "Analyse Customer",
    use_container_width=True
)

if analyse:

    customer = {

        "id": int(customer_id),

        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    prediction, probability = predict_customer(customer)

    risk = calculate_risk(probability)

    recommendation = business_recommendation(risk)
    save_prediction(
        username=st.session_state.username,
        customer=customer,
        prediction=prediction,
        probability=probability,
        risk=risk,
        recommendation=recommendation
    )

    st.success("Prediction saved successfully.")

    st.divider()

    st.subheader("📊 Prediction Dashboard")

    card1, card2, card3 = st.columns(3)

    with card1:

        st.metric(
            "Churn Probability",
            f"{probability*100:.2f}%"
        )

    with card2:

        st.metric(
            "Risk Category",
            risk
        )

    with card3:

        if prediction == 1:
            result = "Likely to Churn"
        else:
            result = "Likely to Stay"

        st.metric(
            "Prediction",
            result
        )

    st.divider()

    st.subheader("Prediction Confidence")

    st.progress(float(probability))

    st.caption(
        f"Model estimated churn probability: {probability:.4f}"
    )

    st.divider()

    st.subheader("👤 Customer Overview")

    overview_left, overview_right = st.columns(2)

    with overview_left:

        st.write(f"**Gender:** {gender}")
        st.write(f"**Partner:** {partner}")
        st.write(f"**Dependents:** {dependents}")
        st.write(f"**Contract:** {contract}")
        st.write(f"**Internet Service:** {internet_service}")

    with overview_right:

        st.write(f"**Tenure:** {tenure} months")
        st.write(f"**Monthly Charges:** ${monthly_charges:.2f}")
        st.write(f"**Total Charges:** ${total_charges:.2f}")
        st.write(f"**Payment Method:** {payment_method}")

    st.divider()

    # ==========================================================
    # BUSINESS RECOMMENDATION
    # ==========================================================

    st.subheader("🎯 Business Recommendation")

    if risk == "HIGH":

        st.error(f"**{recommendation['title']}**")

    elif risk == "MEDIUM":

        st.warning(f"**{recommendation['title']}**")

    else:

        st.success(f"**{recommendation['title']}**")

    st.write(recommendation["message"])

    st.divider()

    # ==========================================================
    # CUSTOMER INFORMATION
    # ==========================================================

    with st.expander("📋 View Customer Information Used for Prediction"):

        display_customer = pd.DataFrame([customer])

        st.dataframe(
            display_customer,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ==========================================================
    # MODEL INFORMATION
    # ==========================================================

    st.subheader("ℹ️ Model Information")

    info_left, info_right = st.columns(2)

    with info_left:

        st.info(
            """
**Prediction Model**

• Algorithm: Extreme Gradient Boosting (XGBoost)

• Task: Binary Classification

• Target Variable: Customer Churn
"""
        )

    with info_right:

        st.info(
            """
**Decision Support**

The prediction is based on the customer's demographic,
service subscription and billing information.

The output assists customer retention planning.
"""
        )

# ==========================================================
# PREDICTION HISTORY
# ==========================================================

st.divider()

st.header("🗄️ Prediction History")

history = load_predictions()

if history.empty:

    st.info("No prediction records have been saved yet.")

else:

    total_predictions = len(history)

    high_risk = len(
        history[history["Risk"] == "HIGH"]
    )

    likely_churn = len(
        history[
            history["Prediction"] == "Likely to Churn"
        ]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Predictions",
            total_predictions
        )

    with col2:
        st.metric(
            "High Risk",
            high_risk
        )

    with col3:
        st.metric(
            "Likely to Churn",
            likely_churn
        )

    st.dataframe(
        history,
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# DATABASE MANAGEMENT
# ==========================================================

with st.expander("⚠️ Database Management"):

    st.warning(
        "This will permanently delete all prediction records."
    )

    confirm = st.checkbox(
        "I understand that this action cannot be undone."
    )

    if st.button(
        "Delete All Records",
        disabled=not confirm,
        use_container_width=True
    ):

        delete_all_predictions()

        st.success("Database cleared successfully.")

        st.rerun()