class InvestmentProfile:
    # Investment current investment attributes
    AI_output = None
    AI_evaluated_portfolio = None
    currency = None
    currency_symbol = None
    investment_amount = None
    file_uploaded = False
    uploaded_file = None   
    current_value = None

    # Investment profile attributes
    goal = None
    risk_tolerance = None
    experience = None
    emergency_fund = None
    debt_status = None
    income_stability = None
    access_need = None

    previous_recommended_portfolio = None
    latest_recommendation_portfolio = None
    more_recommendation = False
    @classmethod
    def save_responses(cls, goal, risk_tolerance, experience, emergency_fund, debt_status, income_stability, access_need):
        cls.goal = goal
        cls.risk_tolerance = risk_tolerance
        cls.experience = experience
        cls.emergency_fund = emergency_fund
        cls.debt_status = debt_status
        cls.income_stability = income_stability
        cls.access_need = access_need

    @classmethod
    def get_summary(cls):
        return {
            "Goal": cls.goal,
            "Risk Tolerance": cls.risk_tolerance,
            "Experience": cls.experience,
            "Emergency Fund": "Yes" if cls.emergency_fund else "No",
            "Debt Status": cls.debt_status,
            "Income Stability": cls.income_stability,
            "Access Need": cls.access_need
        }
