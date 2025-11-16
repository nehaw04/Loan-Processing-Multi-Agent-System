# tools.py
import time
import random

# =============================================================================
# 1. MOCK DATABASES (Simulating your "Servers")
# =============================================================================

# CRM SERVER: Customer Details
MOCK_CRM = {
    "Alex Johnson": {"phone": "555-0199", "city": "New York", "address": "123 Wall St"},
    "Neha R":       {"phone": "987-6543", "city": "Bhopal",   "address": "456 VIT Campus"},
}

# OFFER MART: Pre-approved limits and Schemes
MOCK_OFFERS = {
    "Alex Johnson": {
        "limit": 50000,
        "schemes": [
            {"name": "Corp-Advantage", "rate": 8.5, "tenure": 5},
            {"name": "Flexi-Personal", "rate": 10.2, "tenure": 3}
        ]
    },
    "Neha R": {
        "limit": 100000,
        "schemes": [
            {"name": "Student-Special", "rate": 7.0, "tenure": 4},
            {"name": "Tech-Professional", "rate": 8.0, "tenure": 7}
        ]
    },
}

# CREDIT BUREAU: Credit Scores
MOCK_CREDIT_BUREAU = {
    "Alex Johnson": 720,
    "Neha R":       680, # Slightly low to test edge cases
}

# =============================================================================
# 2. WORKER TOOLS
# =============================================================================

def verify_kyc_data(name: str) -> str:
    """Simulates fetching data from the CRM Server."""
    print(f"\n--- [Tool: CRM Server] Fetching KYC for {name}... ---")
    time.sleep(1)
    
    data = MOCK_CRM.get(name)
    if data:
        return f"KYC VERIFIED. Phone: {data['phone']}, Address: {data['address']}, City: {data['city']}"
    else:
        return "KYC FAILED. User not found in CRM."

def fetch_credit_data(name: str) -> dict:
    """Simulates fetching score from Credit Bureau and Offer from Offer Mart."""
    print(f"\n--- [Tool: Bureau & Offer Mart] Fetching financial data... ---")
    time.sleep(1)
    
    score = MOCK_CREDIT_BUREAU.get(name, 0)
    offer = MOCK_OFFERS.get(name, {"limit": 0, "schemes": []})
    
    return {"score": score, "pre_approved_limit": offer['limit'], "schemes": offer['schemes']}

def underwriting_logic(req_amount: int, income: int, pre_approved_limit: int, credit_score: int, salary_slip_uploaded: bool) -> str:
    """
    THE CORE LOGIC (Strict Rules):
    1. Reject if Score < 700.
    2. Approve if Amount <= Pre-Approved Limit.
    3. If Amount <= 2x Limit: Check Salary Slip & EMI.
    4. Reject if Amount > 2x Limit.
    """
    print(f"\n--- [Tool: Underwriting Engine] Analyzing Eligibility... ---")
    print(f"   Input: Req={req_amount}, Limit={pre_approved_limit}, Score={credit_score}")

    # Rule 1: Credit Score Check
    if credit_score < 700:
        return f"REJECTED. Credit Score ({credit_score}) is below the 700 threshold."

    # Rule 2: Instant Approval
    if req_amount <= pre_approved_limit:
        return "APPROVED INSTANTLY. Amount is within pre-approved limit."

    # Rule 4: Hard Limit Check (> 2x)
    if req_amount > (2 * pre_approved_limit):
        return f"REJECTED. Requested amount ({req_amount}) exceeds 2x the pre-approved limit ({pre_approved_limit})."

    # Rule 3: The "Grey Area" (Requires Salary Slip)
    # Logic: Amount is between 1x and 2x limit.
    if not salary_slip_uploaded:
        return "PENDING_DOCS. Amount exceeds pre-approved limit. Please upload Salary Slip for verification."
    
    # Simulate EMI Calc (Assume 60 months, 10% interest approx)
    # Simple Math: EMI is roughly (Amount * 1.5) / 60 for total interest impact estimation
    estimated_emi = (req_amount * 1.10) / 60 
    half_salary = income / 2
    
    if estimated_emi <= half_salary:
        return f"APPROVED via MANUAL UNDERWRITING. EMI ({int(estimated_emi)}) is within 50% of monthly income."
    else:
        return f"REJECTED. Estimated EMI ({int(estimated_emi)}) exceeds 50% of monthly income."

def generate_sanction_letter_file(name: str, amount: int, scheme: str) -> str:
    """Generates a text file simulating a PDF."""
    print(f"\n--- [Tool: PDF Generator] Creating Sanction Letter... ---")
    content = f"""
    =========================================
    OFFICIAL SANCTION LETTER - EY BANK
    =========================================
    Date: {time.strftime("%Y-%m-%d")}
    To: {name}
    
    Congratulations! Your loan application has been approved.
    
    Product: {scheme}
    Sanctioned Amount: ${amount}
    Status: APPROVED
    
    Authorized Signatory
    EY Techathon Bot
    =========================================
    """
    # Write to a real file
    filename = "Sanction_Letter.txt"
    with open(filename, "w") as f:
        f.write(content)
    
    return f"SUCCESS. Letter generated at '{filename}'."