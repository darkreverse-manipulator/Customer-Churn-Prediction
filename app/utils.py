# ==========================================================
# BUSINESS RISK ANALYSIS
# ==========================================================

def calculate_risk(probability):

    if probability >= 0.80:
        return "HIGH"

    elif probability >= 0.55:
        return "MEDIUM"

    return "LOW"


# ==========================================================
# BUSINESS RECOMMENDATION
# ==========================================================

def business_recommendation(risk):

    if risk == "HIGH":

        return {
            "title": "Immediate Customer Retention",
            "message": """
• Contact customer immediately.

• Offer a loyalty package.

• Assign premium customer support.

• Review current contract.

• Schedule follow-up within 30 days.
"""
        }

    elif risk == "MEDIUM":

        return {
            "title": "Customer Monitoring",
            "message": """
• Send promotional offers.

• Recommend long-term contract.

• Review service satisfaction.

• Monitor future usage.
"""
        }

    return {

        "title": "Stable Customer",

        "message": """
• Continue normal support.

• Recommend additional services.

• Maintain engagement.
"""
    }